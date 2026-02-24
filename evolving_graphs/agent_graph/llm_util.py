import ollama
import logging
import tiktoken

from typing import Union, List, Dict

def chat_llm(model: str, prompt_or_messages: Union[str, List[Dict]]) -> str:
    """
    Wrapper for the ollama chat LLM. Supports both simple prompts and full message history.

    Args:
        model (str): The model to use.
        prompt_or_messages (Union[str, List[Dict]]): 
            - If str: A single user prompt.
            - If list: A list of message dicts [{'role': '...', 'content': '...'}]

    Returns:
        str: The response content.
    """
    try:
        if isinstance(prompt_or_messages, str):
            messages = [{'role': 'user', 'content': prompt_or_messages}]
        else:
            messages = prompt_or_messages

        # Log the full prompt/messages
        # logging.info(f"LLM Request Messages:\n{messages}")

        response = ollama.chat(model=model, messages=messages)
        content = response['message']['content'].strip()
        
        # Log full response
        # logging.info(f"LLM Response:\n{content}")
        
        return content
    except Exception as e:
        logging.error(f"LLM Error: {e}")
        return f"Error: LLM chat failed: {e}"

def truncate_context(text: str, max_chars: int = 11000) -> str:
    """
    Truncates text to fit within token limits, preserving the start and end.
    Aprox 11000 characters is roughly 3000-4000 tokens for Python code.
    """
    if not text or len(text) <= max_chars:
        return text
    
    half = max_chars // 2
    prefix = text[:half]
    suffix = text[-half:]
    
    return f"{prefix}\n\n... [TRUNCATED FOR CONTEXT LIMITS] ...\n\n{suffix}"