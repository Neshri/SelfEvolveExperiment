import json
import re
import logging
import ast
from typing import Tuple, Set, Optional, List

from .agent_config import DEFAULT_MODEL, SMART_MODEL
from .llm_util import chat_llm

# --- Semantic Constraints ---
BANNED_ADJECTIVES: Set[str] = {
    "efficient", "efficiently", "optimal", "optimally", "seamless", "seamlessly",
    "robust", "robustly", "comprehensive", "comprehensively", "easy", "easily",
    "powerful", "advanced", "innovative", "cutting-edge", "streamlined", "facilitate",
    "bespoke", "symphony", "meticulous", "pivotal"
}

class SemanticGatekeeper:
    """
    Manages LLM interactions with strict semantic enforcement.
    Acting as the firewall between the raw LLM output and the system state.
    """
    
    def execute_with_feedback(self, initial_prompt: str, json_key: str, forbidden_terms: List[str] = [], verification_source: str = None, log_context: str = "General", expect_json: bool = True, min_words: int = 0, model: str = DEFAULT_MODEL) -> str:
        if expect_json:
            final_prompt = f"{initial_prompt}\n\nIMPORTANT: Return ONLY a valid JSON object with key '{json_key}'. No Markdown. Escape all double quotes inside strings."
        else:
            final_prompt = initial_prompt
        
        messages = [
            {"role": "system", "content": "You are a strict technical analyst. Output valid JSON only."},
            {"role": "user", "content": final_prompt}
        ]
        
        MAX_RETRIES = 3 
        last_attempt_content = "[Analysis Failed]"
        last_warning = ""
        for attempt in range(MAX_RETRIES + 1):
            # Use the bigger model if something goes wrong
            if attempt > 1: model = SMART_MODEL
            raw_response = chat_llm(model, messages)
            
            # --- PHASE 1: PARSE ---
            if expect_json:
                clean_val, json_error = self._parse_json_safe(raw_response, json_key)
            else:
                clean_val, json_error = raw_response.strip(), None
            
            if clean_val is None:
                logging.warning(f"[{log_context}] [Attempt {attempt}] FORMAT FAIL.\nPROMPT: {final_prompt}\nRESPONSE: {raw_response}\nERROR: {json_error}")
                messages.append({"role": "assistant", "content": raw_response})
                messages.append({"role": "user", "content": f"System Alert: Invalid JSON format. Error: {json_error}. \nEnsure you escape double quotes inside the text (e.g. \\\"text\\\"). Return ONLY the object with key '{json_key}'."})
                continue
            
            last_attempt_content = clean_val

            # --- PHASE 2: STYLE CHECK ---
            is_valid_style, style_critique = self._critique_content(clean_val, forbidden_terms, min_words)
            if not is_valid_style:
                logging.warning(f"[{log_context}] [Attempt {attempt}] STYLE FAIL.\nPROMPT: {final_prompt}\nRESPONSE: {raw_response}\nCRITIQUE: {style_critique}")
                messages.append({"role": "assistant", "content": raw_response})
                
                feedback_msg = (
                    f"{style_critique}\n"
                    "CRITICAL INSTRUCTION: Rewrite the text completely. "
                    "Do NOT explain what you changed. "
                    "Do NOT output the forbidden words in your apology. "
                    "Just output the corrected JSON."
                )
                messages.append({"role": "user", "content": feedback_msg})
                continue

            # --- PHASE 3: TRUTH CHECK (The Auditor) ---
            if verification_source:
                confidence, reason = self._verify_grounding(clean_val, verification_source)
                
                if confidence < 3:
                    # Logging Enhancement: Show more context
                    logging.warning(f"[{log_context}] [Attempt {attempt}] LOGIC REJECTION ({confidence}/5).\nCLAIM: {clean_val}\nREASON: {reason}\n")
                    last_warning = f" (⚠️ Verified as inaccurate: {reason})"
                    messages.append({"role": "assistant", "content": raw_response})
                    
                    guidance = ""
                    if "active" in reason.lower() and "passive" in reason.lower():
                        guidance = " HINT: If the code only imports the module but doesn't call its functions, explicitly state 'Passive usage only'."
                    elif "implement" in reason.lower() or "abstract" in reason.lower():
                        guidance = " HINT: If the code is an Abstract Class/Interface, describe it as 'Defining an interface'."

                    messages.append({"role": "user", "content": f"Auditor Critique: The code does NOT support that statement. \nAuditor Finding: {reason}\n\nTask: Rewrite the '{json_key}' value to be strictly accurate to the code snippet provided.{guidance}"})
                    continue

            # Success!
            logging.info(f"[{log_context}] PASSED. Final Value: '{clean_val}'")
            return clean_val
        
        logging.error(f"[{log_context}] FAIL: Exhausted retries. Returning last attempt with warning.")
        return f"{last_attempt_content}{last_warning}"

    def _verify_grounding(self, claim: str, source_code: str) -> Tuple[int, str]:
        verify_prompt = f"""
        Act as a Code Auditor.
        Reference Code:
        \"\"\"
        {source_code}
        \"\"\"
        Claim to Verify: "{claim}"
        Task: Rate confidence (0-5) that the CLAIM is ACCURATE given the CODE.
        
        CRITICAL: 
        - Reject "Marketing Fluff": Claims about "business value", "insights", "efficiency", "real-time", or "user experience" are FALSE unless the code explicitly calculates them.
        - Reject "Implied Intent": Do not credit the module with the *intent* of its consumers. Only what it *actually does*.
        
        Scoring Rubric:
        5 (Accurate): Claim describes the Code perfectly (including accurately identifying passivity/abstractions).
        3 (Plausible): Claim is technically true but uses slightly flowery language.
        1 (False): Claim contradicts the Code OR contains unverifiable marketing fluff (e.g. "actionable insights").
        
        Return JSON: {{ "score": <int>, "reason": "<concise explanation>" }}
        """
        response = chat_llm(DEFAULT_MODEL, verify_prompt)
        try:
            val = self._parse_whole_json(response)
            return int(val.get("score", 3)), val.get("reason", "No reason provided")
        except:
            return 3, "Verification Error"

    def _critique_content(self, text_raw: str, forbidden_terms: List[str], min_words: int) -> Tuple[bool, str]:
        text_lower = text_raw.lower()
        
        # Check Global Banned List
        found_words = []
        for w in BANNED_ADJECTIVES:
            if re.search(r'\b' + re.escape(w) + r'\b', text_lower):
                found_words.append(w)
                
        if found_words: 
            return False, f"Critique: Remove marketing words: {found_words}."
            
        # Check Context-Specific Forbidden Terms
        for term in forbidden_terms:
            if len(term) < 4: continue # Ignore short terms
            if re.search(r'\b' + re.escape(term.lower()) + r'\b', text_lower):
                return False, f"Critique: Forbidden generic verb found: '{term}'. Be more specific."
        
        # Word Count Check
        if min_words > 0:
            # Simple whitespace split
            word_count = len(text_raw.split())
            if word_count < min_words:
                return False, f"Critique: Response too short ({word_count} words). Please describe in at least {min_words} words."

        if len(text_raw) < 2: return False, "Critique: Response too short."
        return True, "Valid"

    def _extract_balanced_json(self, text: str) -> Optional[str]:
        # Robust string-aware bracket balancing
        start = text.find("{")
        if start == -1: return None
        balance = 0
        found_start = False
        in_quote = False
        escape_next = False
        
        for i in range(start, len(text)):
            char = text[i]
            
            if escape_next:
                escape_next = False
                continue
                
            if in_quote:
                if char == '\\':
                    escape_next = True
                elif char == '"':
                    in_quote = False
            else:
                if char == '"':
                    in_quote = True
                elif char == "{":
                    balance += 1
                    found_start = True
                elif char == "}":
                    balance -= 1
            
            if found_start and balance == 0:
                return text[start:i+1]
        return None

    def _parse_json_safe(self, raw: str, key: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Robust JSON extraction that handles Markdown blocks, Python literals, Regex rescue,
        and specifically targets 3B model hallucinations (like trailing quotes).
        """
        try:
            if not raw: return None, "Empty response"
            clean = raw.strip()
            
            # --- AGGRESSIVE NORMALIZATION ---
            # Fix Smart Quotes
            clean = clean.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
            # Fix Triple Quotes (common in 3B models)
            if '"""' in clean:
                clean = clean.replace('"""', '"')
            
            # 1. Attempt Clean Extraction via Bracket Balancing
            balanced_json = self._extract_balanced_json(clean)
            if balanced_json: clean = balanced_json
            else:
                if "```" in clean:
                    match = re.search(r"```(?:json)?(.*?)```", clean, re.DOTALL)
                    if match: clean = match.group(1).strip()
                if not clean.startswith("{"):
                    start = clean.find("{")
                    end = clean.rfind("}") + 1
                    if start != -1 and end != 0: clean = clean[start:end]

            # FIX: Pre-emptive cleanup for common 3B hallucinations
            # Case: Trailing quote -> "value""}
            if clean.endswith('""}'):
                clean = clean[:-3] + '"}'
            # Case: Trailing quote with spaces -> "value" "}
            if re.search(r'"\s*"}$', clean):
                clean = re.sub(r'"\s*"}$', '"}', clean)
            
            # Case: Missing closing quote before closing brace (Common 3B error)
            # Pattern: "key": "value  }  (End of string)
            # We look for: <quote><text><newline/space><brace> at end
            # but NOT <quote><text><quote><brace>
            if re.search(r':\s*"[^"]+\s*}$', clean):
                 # Insert the missing quote before the closing brace
                 clean = re.sub(r'(\s*)}$', r'"\1}', clean)
            
            # Case: Missing closing quote before closing brace (Common 3B error)
            # Pattern: "key": "value  }  (End of string)
            # We look for: <quote><text><newline/space><brace> at end
            # but NOT <quote><text><quote><brace>
            if re.search(r':\s*"[^"]+\s*}$', clean):
                 # Insert the missing quote before the closing brace
                 clean = re.sub(r'(\s*)}$', r'"\1}', clean)
            
            # REMOVED: Dangerous heuristics that look for punctuation followed by brace.
            # They caused corruption of valid JSON containing code snippets (e.g. "funcless)")
            # We now rely on 'strict=False' in json.loads and the 'Deep Rescue' below.

            # Case: General Unclosed Quote before brace/comma
            # Pattern: "key": "value... <newline> }  (Missing quote)
            # We look for a line that started with quote, has content, but ends without quote before the structural char.
            # This is hard to regex perfectly. 
            # Let's try to find: `  "answer": "..... \n  }` 
            # We can try to repair specific known keys if we knew them, but here we don't.
            # Generic approach: Look for `\s*"[^"]+\s*\n\s*[},]`
            
            # Fix: "answer": "text... \n } -> "answer": "text..." \n }
            # Match: " (anything except quote) \n (whitespace) }
            # This handles the nested case: ... \n } \n }
            clean = re.sub(r':\s*"([^"]+?)\s*\n\s*([},])', r': "\1"\n\2', clean, flags=re.DOTALL)
            
            # Also handle the case where it just ends at the very end of string with multiple braces
            # e.g. ... text \n } \n }
            clean = re.sub(r':\s*"([^"]+?)\s*(\}+)$', r': "\1"\2', clean, flags=re.DOTALL)

            # 2. Primary Parse: Strict JSON
            try:
                # strict=False allows control characters like newlines in strings
                data = json.loads(clean, strict=False)
            except json.JSONDecodeError:
                # 3. Secondary Parse: Flatten Newlines and Tabs (Fix for 3B model)
                try:
                    # Tabs are forbidden in JSON strings but common in 3B output
                    flat_text = clean.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
                    data = json.loads(flat_text, strict=False)
                except:
                    # 4. Python Literal (with JSON compat)
                    data = None
                    try:
                        # Fix JSON constants for Python eval
                        literal_text = clean.replace("null", "None").replace("true", "True").replace("false", "False")
                        data = ast.literal_eval(literal_text)
                        if not isinstance(data, dict): data = None
                    except:
                        pass

                # 5. Regex Rescue (Robust)
                if data is None:
                    try:
                        # Fallback: Extract the key's value directly.
                        # Matches: "key" : "value" OR "key": { ... }
                        
                        # Check for Object start first
                        object_start_pattern = fr'"{key}"\s*:\s*{{'
                        obj_match = re.search(object_start_pattern, clean, re.DOTALL)
                        
                        if obj_match:
                            # We found "key": { ...
                            # Use bracket balancing starting from the open brace
                            start_idx = obj_match.end() - 1 # Position of '{'
                            # We can reuse extract_balanced_json logic but starting from specific index? 
                            # self._extract_balanced_json search from text.find('{'). 
                            # Let's just slice and call it.
                            substring = clean[start_idx:]
                            balanced_obj = self._extract_balanced_json(substring)
                            if balanced_obj:
                                try:
                                    # recursive parse of the inner object
                                    inner_data = json.loads(balanced_obj)
                                    data = {key: inner_data}
                                except:
                                    # Try evaluating as python dict
                                    try:
                                        inner_data = ast.literal_eval(balanced_obj)
                                        data = {key: inner_data}
                                    except:
                                        pass
                        
                        # Check for String match if no object found or object parse failed
                        if data is None:
                            string_content_pattern = r'(?:\\.|[^"\\])*'
                            capture_pattern = fr'"{key}"\s*:\s*("(?P<val>{string_content_pattern})")'
                            match = re.search(capture_pattern, clean, re.DOTALL)
                            if match:
                                 raw_val = match.group('val')
                                 if raw_val.startswith('\\"') and raw_val.endswith('\\"'):
                                     raw_val = raw_val[2:-2]
                                 
                                 # Unescape standard json escapes
                                 try:
                                     wrapped = f'"{raw_val}"'
                                     safe_val = json.loads(wrapped)
                                 except:
                                     # Manual fallback
                                     safe_val = raw_val.replace('\\"', '"').replace('\\n', '\n')
                                     
                                 data = {key: safe_val} 
                                 
                        # Deep Rescue for "answer" specifically (common failure point)
                        if data is None and key == "result":
                             # Look for "answer": "..." inside the text, even if outer braces are messed up
                             # Pattern: "answer" ... : ... " <content> " ... [},]
                             # We assume content ends at the last quote before a closing brace/comma
                             answer_pattern = r'"answer"\s*:\s*"(.*)"\s*[},]\s*\}'
                             # This is improper because non-greedy .*? stops at first quote. 
                             # Greedy .* consumes too much.
                             # We use the "Last Resort" logic but apply it to the answer field only.
                             # Find "answer": "
                             start_marker = '"answer"'
                             idx = clean.find(start_marker)
                             if idx != -1:
                                 # Find the first quote after answer
                                 val_start = clean.find('"', idx + len(start_marker))
                                 if val_start != -1:
                                     val_start += 1 # Skip quote
                                     # Find the end: we look for " } or " , or " \n }
                                     # This is risky. Let's look for the LAST quote before the end of the string/block
                                     val_end = clean.rfind('"')
                                     
                                     # Refine: Ensure val_end is after val_start
                                     if val_end > val_start:
                                         # But wait, val_end might be the quote of "result" closing? 
                                         # The structure is { "result": { ... "answer": "..." } }
                                         # So val_end should be the one before } }
                                         # Let's try to extract slightly more intelligently.
                                         
                                         # Extract everything from val_start to val_end
                                         raw_answer = clean[val_start:val_end]
                                         # Verify if raw_answer contains the closing } of the object?
                                         # If raw_answer has " } at the end, we went too far?
                                         # Actually, let's just use the regex from before but applied to "inner" content.
                                         pass 
                                         
                             # New heuristic: "answer": " <capture> " \s* }
                             # We assume the model outputs at least correct ending structure.
                             deep_match = re.search(r'"answer"\s*:\s*"(.*)"\s*}\s*}', clean, re.DOTALL)
                             if deep_match:
                                 raw_ans = deep_match.group(1)
                                 # Sanitize quotes: If we captured greedy, we might have captured "internal" quotes.
                                 # We just escape ALL quotes, then unescape the edges? No.
                                 # We assume standard text doesn't have \" unless escaping.
                                 # We simply replace " with ' blindly to make it valid JSON?
                                 safe_ans = raw_ans.replace('"', "'")
                                 data = {"result": {"status": "ACTIVE", "answer": safe_ans}}
                    except:
                         pass

                # 6. Last Resort: Permissive Match (Assuming simple { "key": "..." } structure)
                if data is None:
                    try:
                        # Capture everything from the first quote after key to the last quote before closing brace
                        # This ignores internal escaping rules entirely.
                        permissive_pattern = fr'"{key}"\s*:\s*"(.*)"\s*}}\s*$'
                        match = re.search(permissive_pattern, clean, re.DOTALL)
                        if match:
                             raw_val = match.group(1)
                             # Sanitize quotes blindly
                             safe_val = raw_val.replace('\\"', '"').replace('"', "'") 
                             data = {key: safe_val}
                    except:
                        pass
                    
                    if data is None: 
                         return None, "JSON Decode Error"

            # Check for error object
            if isinstance(data, dict) and "error" in data and len(data.keys()) == 1:
                return None, f"Model returned error object: {data['error']}"

            # FIX: Crash Prevention
            if data is None:
                return None, "JSON parsing failed (all methods exhausted)"

            # Validate Key Presence
            if key and key not in data:
                 if isinstance(data, dict) and "answer_text" in data and key == "result":
                     data = {"result": data["answer_text"]}
                 else:
                    return None, f"Missing key '{key}'."

            val = data[key]
            
            if isinstance(val, (dict, list, bool, int, float)):
                return json.dumps(val), None
            return str(val).strip(), None

        except Exception as e:
            return None, str(e)

    def _parse_whole_json(self, raw: str) -> dict:
        try:
            balanced = self._extract_balanced_json(raw)
            if balanced: return json.loads(balanced)
            clean = raw.strip()
            if "```" in clean:
                match = re.search(r"```(?:json)?(.*?)```", clean, re.DOTALL)
                if match: clean = match.group(1).strip()
            start = clean.find("{")
            end = clean.rfind("}") + 1
            if start == -1: return {}
            return json.loads(clean[start:end])
        except:
            return {}