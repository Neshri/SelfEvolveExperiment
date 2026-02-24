# Project Context Map

## 🏛️ System Architecture
The `main` function in `agent_graph_main.py` initiates by locating `_main.py` in the target folder, then instantiates a `CrawlerAgent` with the identified file and goal. This agent delegates execution to `agent_core.py`, where `CrawlerAgent.run` orchestrates project structure analysis by synthesizing maps, generating reports, and coordinating with `report_renderer.py` and `map_synthesizer.py`. The `ProjectSummarizer` in `agent_util.py` computes module processing order, which feeds into `dependency_analyst.py` for dependency extraction and `task_executor.py` for complex task resolution.

Data flows through `semantic_gatekeeper.py` to validate JSON outputs against schema constraints, ensuring grounding in source code via `semantic_gatekeeper.execute_with_feedback`. The `TaskExecutor` in `task_executor.py` iteratively refines results using `llm_util.py` and `summary_models.py`, while `module_contextualizer.py` and `component_analyst.py` collaborate to generate contextualized module summaries. `map_critic.py` and `memory_core.py` ensure consistency by critiquing synthesized maps and persisting memory states across iterations.

Accuracy is enforced through `semantic_gatekeeper.py`'s structured extraction of JSON outputs, error handling in `TaskExecutor.solve_complex_task`, and cyclic validation between `ProjectSummarizer` and `DependencyAnalyst`. `memory_core.py` tracks state transitions, while `semantic_gatekeeper.py` retries failed validations with increased model precision. Complex dependencies are resolved via `graph_analyzer.py` and `module_classifier.py`, ensuring all transformations adhere to defined schema constraints.

---

**Total Modules:** 17

## 🚀 Entry Points

## 📦 Module: `agent_graph_main.py`
**Role:** The module `agent_graph_main.py` orchestrates searching for '_main.py' file in target folder, initializes CrawlerAgent with found file and goal, runs the agent, and returns completion status. [1]

### 🚨 Alerts
- TODO **TODO**: Implement the rest of the function `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 main`**: Searches for `'_main.py'` in `target_folder`, initializes `CrawlerAgent` with found file and `goal`, executes agent, and returns completion status. [2]

### 🔗 Uses (Upstream)
- **`agent_core.py`**: Orchestrates analysis and synthesis of project structure by initializing CrawlerAgent, managing memory states, synthesizing maps, generating reports, and cleaning memories. [3]

---
## ⚙️ Services

## 📦 Module: `agent_core.py`
**Role:** The module `agent_core.py` orchestrates analysis and synthesis of project structure by defining goals, processing memory states, synthesizing maps, generating reports, and rendering context.

**Impact Analysis:** Changes to this module will affect: agent_graph_main.py [1]

### 🚨 Alerts
- TODO **TODO**: Implement the agent's logic here `(Ref: Comment)`

### 🧩 Interface & Logic
- **`🔌 class CrawlerAgent`**: Initializes an instance of CrawlerAgent with specified goal and target root, sets up ChromaMemory for memory storage, and logs initialization details. [2]
- **`🔌 🔌 CrawlerAgent.run`**: Runs the CrawlerAgent, retrieves project map and processing order, synthesizes system summary, renders report, cleans memories for 5 turns, and returns analysis complete response. [3]

### 🔗 Uses (Upstream)
- **`report_renderer.py`**: Generates project architecture documentation and verification evidence by iterating over modules to determine archetypes, dependencies, and public API. [4]
- **`map_synthesizer.py`**: Orchestrates technical synthesis of system architecture by identifying anchor components, generating supporting cast list based on processing order, and running grounded synthesis to produce a cohesive narrative. [5]
- **`agent_util.py`**: Orchestrates integration of external agents into system workflows, ensuring coordinated execution across diverse functionalities. [6]
- **`summary_models.py`**: Defines and manages structured context for the module, encapsulating role, dependencies, dependents, public API, alerts, and claims using classes like Claim, GroundedText, Alert, and ModuleContext. [7]
- **`llm_util.py`**: Formats user input and truncates text for model processing. [8]
- **`task_executor.py`**: Orchestrates task execution and analysis, managing complex workflows through semantic gatekeeping and context refinement to ensure coherent response generation. [9]
- **`agent_config.py`**: Configures default model and context limit settings for the agent. [10]
- **`semantic_gatekeeper.py`**: Validates and critiques user-provided JSON output, ensuring grounding and structure through semantic analysis. [11]
- **`memory_core.py`**: Stores and retrieves memory documents in the Chroma database to support context-aware decision-making and knowledge retention within the agent system. [12]

### 👥 Used By (Downstream)
- **`agent_graph_main.py`**

---
## 📦 Module: `agent_util.py`
**Role:** The module `agent_util.py` analyzes and orchestrates the integration of external agents into system workflows, ensuring interaction and coordinated execution across diverse functionalities.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 ProjectGraph`**: Assigns the data structure `Dict[str, Any]` to the variable `ProjectGraph`. [2]
- **`🔌 class ProjectSummarizer`**: Initializes attributes and computes processing order for modules based on provided graph and maximum cycles. [3]
- **`🔌 project_pulse`**: Analyzes the project from the given file path, generates a dependency graph using GraphAnalyzer, summarizes the project graph into module contexts and processing order, and returns them. [4]
- **`🔌 🔌 ProjectSummarizer.generate_contexts`**: Iterates through cycles to generate module contexts by creating or updating them based on dependencies, critiques, and source code. [5]
- **`🔒 _create_module_context`**: Creates module context by contextualizing module using ModuleContextualizer, setting file path if not present, and returning the populated ModuleContext. [6]

### 🔗 Uses (Upstream)
- **`report_renderer.py`**: Generates and organizes markdown documentation for project architecture, role-based access controls, dependencies, public APIs, alerts, and verification claims by iterating over modules and their attributes. [7]
- **`summary_models.py`**: Defines structured context management for modules using classes like Claim, GroundedText, Alert, and ModuleContext to encapsulate role, dependencies, dependents, public API, alerts, and claims. [8]
- **`module_contextualizer.py`**: Analyzes module context to generate alerts and perform systemic synthesis based on critique instruction, enabling informed decision-making and risk assessment. [9]
- **`graph_analyzer.py`**: Analyzes code structure and dependencies to extract entities such as functions, classes, imports, and relationships for documentation or validation purposes. [10]
- **`semantic_gatekeeper.py`**: Validates and critiques user-provided JSON output to ensure structural integrity, semantic grounding, and stylistic adherence via structured parsing. [11]
- **`map_critic.py`**: Validates module documentation by identifying and correcting lazy definitions, missing constants, and vague dependencies within `agent_util.py`. [12]

### 👥 Used By (Downstream)
- **`agent_core.py`**

---
## 📦 Module: `component_analyst.py`
**Role:** The module `component_analyst.py` annotates and summarizes code components by defining their roles, mechanisms, and dependencies based on parsed source code.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ComponentAnalyst`**: Analyzes code structure and context to generate summaries of component roles, mechanisms, and dependencies within the specified module. [2]
- **`🔌 class SkeletonTransformer`**: Transforms AST nodes by removing docstrings and replacing bodies with `Pass()` if specified. [3]
- **`🔌 🔌 ComponentAnalyst.analyze_components`**: Analyzes the given module, functions, classes, and their interactions to produce summaries of each component's role and behavior in the context provided. [4]
- **`🔌 🔌 ComponentAnalyst.generate_module_skeleton`**: Parses source code into an AST, applies SkeletonTransformer to generate skeleton structure, and returns the modified source code as a string. [5]
- **`🔌 🔌 SkeletonTransformer.visit_AsyncFunctionDef`**: Removes docstring from node and replaces body with `ast.Pass()` if `strip_bodies` is True, then recursively visits children. [6]
- **`🔌 🔌 SkeletonTransformer.visit_ClassDef`**: Removes docstring from node, sets body to [ast.Pass()] if empty, then visits children. [7]
- **`🔌 🔌 SkeletonTransformer.visit_FunctionDef`**: Removes docstring from function definition node and replaces body with `Pass()` if strip_bodies is True, then visits generic. [8]

### 🔗 Uses (Upstream)
- **`task_executor.py`**: Orchestrates task execution, analysis, and refinement by coordinating semantic gatekeeping, context parsing, and iterative response generation. [9]
- **`semantic_gatekeeper.py`**: Validates and critiques user-provided JSON output against specified keys, ensuring grounding and structured content. [10]
- **`summary_models.py`**: Manages structured context for modules by encapsulating role, dependencies, dependents, public API, alerts, and claims using classes like Claim and ModuleContext. [11]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

---
## 📦 Module: `dependency_analyst.py`
**Role:** The module `dependency_analyst.py` analyzes dependency relationships within source code to extract actionable insights about module interactions, facilitating automated refactoring and compliance checks.

**Impact Analysis:** Changes to this module will affect: module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class DependencyAnalyst`**: Initializes the class by assigning provided gatekeeper and task_executor to instance variables. [2]
- **`🔌 🔌 DependencyAnalyst.analyze_dependencies`**: Analyzes upstream context, symbols used, and provides guidance for using imported dependency in specified module. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Aggregates and manages structured context related to module roles, dependencies, dependents, public API, alerts, and claims. [4]
- **`semantic_gatekeeper.py`**: Validates and critiques user-provided JSON output against specified keys, ensuring semantic grounding and returning structured results or error messages. [5]
- **`task_executor.py`**: Orchestrates complex task execution and analysis by parsing context, applying semantic gatekeeping, and refining responses through iterative loops. [6]
- **`module_classifier.py`**: Determines module archetype based on name, source code analysis, and dependency information. [7]

### 👥 Used By (Downstream)
- **`module_contextualizer.py`**

---
## 📦 Module: `map_critic.py`
**Role:** The module `map_critic.py` analyze specific module documentation to identify lazy definitions, missing constants, and vague dependencies, returning a single instruction for improvement if any issues are found.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapCritic`**: Initializes an instance by setting the `gatekeeper` attribute. [2]
- **`🔌 🔌 MapCritic.critique`**: Analyzes each module in the project map content, retrieves critiques for up to three modules, and returns them as tuples of module name and critique instruction. [3]

### 🔗 Uses (Upstream)
- **`semantic_gatekeeper.py`**: Validates and critiques user-provided JSON output for grounding, structure, and content quality to ensure high-quality data integration in the system. [4]

### 👥 Used By (Downstream)
- **`agent_util.py`**

---
## 📦 Module: `map_synthesizer.py`
**Role:** The module `map_synthesizer.py` orchestrates technical synthesis of system architecture by identifying anchor components, generating supporting cast list based on processing order, and running grounded synthesis to produce a cohesive narrative.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class MapSynthesizer`**: Initializes task executor in constructor, identifies top anchor paths by scoring based on archetype and dependencies, runs grounded synthesis combining components to form architecture narrative. [2]
- **`🔌 🔌 MapSynthesizer.synthesize`**: Identifies anchor components, describes their roles and interfaces, generates supporting cast list based on processing order, and runs grounded synthesis. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Encapsulates module context, dependencies, dependents, public API, alerts, and claims to define structured roles and relationships. [4]
- **`task_executor.py`**: Coordinates complex task execution and analysis by initiating the goal loop, managing context data, and handling errors through semantic gatekeeping and iterative refinement of responses. [5]

### 👥 Used By (Downstream)
- **`agent_core.py`**

---
## 📦 Module: `report_renderer.py`
**Role:** The module `report_renderer.py` generates markdown documentation for project architecture and verification evidence based on module context data, organizing modules by archetype and detailing role, alerts, public API, dependencies, and claims.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ReportRenderer`**: Initializes attributes including context_map, output_file, verification_file, system_summary, claim_map, and ref_counter; renders project context map and verification proof by iterating over modules; generates markdown sections for module documentation with role, alerts, public API, key dependencies, downstream dependents, and verification claims. [2]
- **`🔌 🔌 ReportRenderer.render`**: Generates project context map and verification proof by iterating over modules, determining archetypes and dependents, organizing paths into presentation order, and writing to output and verification files. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Organizes and manages structured context of the module, including roles, dependencies, dependents, public API, alerts, and claims. [4]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**

---
## 📦 Module: `semantic_gatekeeper.py`
**Role:** The module `semantic_gatekeeper.py` executes and critiques user-provided JSON output against specified keys, validates grounding, and returns structured results or error messages

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_critic.py, module_contextualizer.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 BANNED_ADJECTIVES`**: Defines global constant `BANNED_ADJECTIVES`. [2]
- **`🔌 class SemanticGatekeeper`**: Validates, critiques, and parses user-provided JSON data through semantic analysis, grounding verification, content scrutiny, and structured extraction. [3]
- **`🔌 🔌 SemanticGatekeeper.execute_with_feedback`**: The function executes the provided prompt, parses and validates its output as JSON against the specified key, critiques style and grounding if required, retries up to three times with increasing model precision, and returns the parsed JSON value or an error message. [4]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Defines global constants DEFAULT_MODEL and SMART_MODEL to specify model configurations for semantic processing and gatekeeping tasks in semantic_gatekeeper.py. [5]
- **`llm_util.py`**: Truncates and formats input for model processing. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_critic.py`**
- **`module_contextualizer.py`**
- **`task_executor.py`**

---
## 📦 Module: `task_executor.py`
**Role:** The module `task_executor.py` orchestrates complex task execution and analysis through semantic gatekeeping, context parsing, and iterative refinement of generated responses.

**Impact Analysis:** Changes to this module will affect: agent_core.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class TaskExecutor`**: Initializes an instance of the class, setting the provided `gatekeeper` as an attribute and assigning `max_retries` to 5. [2]
- **`🔌 🔌 TaskExecutor.solve_complex_task`**: Commences task execution, logs start message, truncates context data, runs goal loop, returns result or error message if exception occurs. [3]

### 🔗 Uses (Upstream)
- **`agent_config.py`**: Defines constants for model selection to customize task execution behavior in the executor. [4]
- **`semantic_gatekeeper.py`**: Orchestrates validation and critique of user-provided JSON output by parsing, grounding, and semantic analysis within task execution flow. [5]
- **`llm_util.py`**: Formats user input by truncating long text to specified maximum characters, ensuring context fits within token limits. [6]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**

---
## 🛠️ Utilities

## 📦 Module: `llm_util.py`
**Role:** The module `llm_util.py` defines and formats utility functions for processing user input or messages using specified models and truncating long text inputs to specified maximum characters.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 chat_llm`**: Processes user input or messages using the specified model and returns the generated content. [2]
- **`🔌 truncate_context`**: Truncates long text input to specified maximum characters, displaying the first half of the text, an ellipsis indicating truncation, and the last half of the text. [3]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**
- **`task_executor.py`**

---
## 📦 Data Models

## 📦 Module: `graph_analyzer.py`
**Role:** The module `graph_analyzer.py` analyzes code structure, imports, assignments, annotations, function definitions, class definitions, and interactions to extract entities such as functions, classes, variables, import modules, cross-module relationships, default signatures, private status indicators, and line numbers.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class CodeEntityVisitor`**: Analyzes code structure, imports, assignments, annotations, function definitions, class definitions, and interactions to extract entities such as functions, classes, variables, import modules, cross-module relationships, default signatures, private status indicators, and line numbers. [2]
- **`🔌 class GraphAnalyzer`**: Initializes the GraphAnalyzer instance by resolving paths, collecting Python files in the project directory, and setting up an empty graph and visited sets. [3]
- **`🔌 🔌 CodeEntityVisitor.leave_ClassDef`**: Removes the current class definition context and header from the stack when leaving a ClassDef node. [4]
- **`🔌 🔌 CodeEntityVisitor.leave_FunctionDef`**: Removes the current context from the stack and pops the header stack when leaving a function definition node, ensuring proper scope management and cleanup of processed headers. [5]
- **`🔌 🔌 CodeEntityVisitor.leave_SimpleStatementLine`**: Sets `current_statement` to None when leaving `SimpleStatementLine` node. [6]
- **`🔌 🔌 CodeEntityVisitor.visit_AnnAssign`**: Analyzes annotated assignment nodes, extracting the target name, source code string, and inferred signature from annotation to populate `globals` list with metadata. [7]
- **`🔌 🔌 CodeEntityVisitor.visit_Assign`**: Collects global variable assignments from the current context, recording their names, source code snippets, default signatures, private status indicators, line numbers, and end line positions. [8]
- **`🔌 🔌 CodeEntityVisitor.visit_Call`**: Analyzes function calls, records interactions for named functions. [9]
- **`🔌 🔌 CodeEntityVisitor.visit_ClassDef`**: Analyzes class definition, extracts source code, docstring, base classes, and stores entity details in the `entities` dictionary. [10]
- **`🔌 🔌 CodeEntityVisitor.visit_FunctionDef`**: Visits each function definition node, collects metadata such as signature, header, docstring, source code, and stores it in `entities['functions']`, while also checking if the function is unimplemented or private and determining if it's a method based on its context. [11]
- **`🔌 🔌 CodeEntityVisitor.visit_Import`**: Collects external module names from imported nodes and adds them to the `external_imports` set. [12]
- **`🔌 🔌 CodeEntityVisitor.visit_ImportFrom`**: Analyzes and records external imports, relative import paths, resolves module names from qualified names, checks for corresponding Python files in the project, and updates import mappings accordingly. [13]
- **`🔌 🔌 CodeEntityVisitor.visit_Name`**: Records the context interaction and node value, storing them in the record interaction mechanism for further analysis or reporting. [14]
- **`🔌 🔌 CodeEntityVisitor.visit_SimpleStatementLine`**: Updates the current statement to the given node. [15]
- **`🔌 🔌 GraphAnalyzer.analyze`**: Builds the dependency graph using depth-first search, populates dependents for each node, and returns the final graph. [16]

### 👥 Used By (Downstream)
- **`agent_util.py`**

---
## 📦 Module: `memory_core.py`
**Role:** The module `memory_core.py` defines an interface for managing and querying memory documents in a Chroma database collection.

**Impact Analysis:** Changes to this module will affect: agent_core.py [1]

### 🧩 Interface & Logic
- **`🔌 class ChromaMemory`**: Manages memory storage, retrieval, and updating in ChromaDB, initializing client and collection, adding memories with embeddings and metadata, querying for matches, adjusting helpfulness scores, and cleaning up old or low-scored entries. [2]
- **`🔌 class MemoryInterface`**: Defines interface signature for memory queries. [3]
- **`🔌 🔌 ChromaMemory.add_memory`**: Creates and adds a memory document to the Chroma database collection, including a unique ID, embedding vector, and metadata about turn added and helpfulness. [4]
- **`🔌 🔌 ChromaMemory.cleanup_memories`**: Deletes memory records with low helpfulness or those not used in the last 50 turns from the ChromaDB collection. [5]
- **`🔌 🔌 ChromaMemory.query_memory`**: Queries the memory collection for matching documents based on the provided query, updates the metadata of each matched document with the current turn number, and returns the results including IDs, documents, metadatas, and distances. [6]
- **`🔌 🔌 ChromaMemory.update_helpfulness`**: Updates the helpfulness score of a specified memory in the Chroma database by retrieving its metadata, modifying the `helpfulness` field, and saving the updated metadata back to the collection. [7]
- **`🔌 🔌 MemoryInterface.query_memory`**: Defines interface signature (Abstract). [8]

### 👥 Used By (Downstream)
- **`agent_core.py`**

---
## 📦 Module: `module_classifier.py`
**Role:** The module `module_classifier.py` classifies modules into archetypes such as ENTRY_POINT, DATA_MODEL, CONFIGURATION, or SERVICE based on module name, source code analysis, and dependency information.

**Impact Analysis:** Changes to this module will affect: dependency_analyst.py, module_contextualizer.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleArchetype`**: Data container for ModuleArchetype records. [2]
- **`🔌 class ModuleClassifier`**: Initializes the ModuleClassifier with `module_name` and `graph_data` attributes to classify modules into archetypes like ENTRY_POINT, DATA_MODEL, CONFIGURATION, or SERVICE based on name, source code, and dependencies. [3]
- **`🔌 🔌 ModuleClassifier.classify`**: Classifies module based on name, source code, and dependencies into archetypes such as ENTRY_POINT, DATA_MODEL, CONFIGURATION, SERVICE. [4]

### 👥 Used By (Downstream)
- **`dependency_analyst.py`**
- **`module_contextualizer.py`**

---
## 📦 Module: `module_contextualizer.py`
**Role:** The module `module_contextualizer.py` analyzes module context, performs component and dependency analysis, populates alerts, and applies systemic synthesis based on critique instruction.

**Impact Analysis:** Changes to this module will affect: agent_util.py [1]

### 🧩 Interface & Logic
- **`🔌 class ModuleContextualizer`**: Summarizes module capabilities, alerts, upstream state and logic, downstream usage, external imports, source code evidence, and role description based on archetype. [2]
- **`🔌 🔌 ModuleContextualizer.contextualize_module`**: Analyzes module context, performs component and dependency analysis, populates alerts, and applies systemic synthesis based on critique instruction. [3]

### 🔗 Uses (Upstream)
- **`summary_models.py`**: Encapsulates module's role, dependencies, dependents, public API, alerts, and claims for structural context management. [4]
- **`component_analyst.py`**: Analyzes and summarizes code components to generate component role summaries within the specified module context. [5]
- **`dependency_analyst.py`**: Analyzes dependency relationships to extract actionable insights for automated refactoring and compliance checks. [6]
- **`module_classifier.py`**: Determines archetype of module to inform contextual processing in module_contextualizer.py. [7]
- **`task_executor.py`**: Orchesters complex task execution and analysis by parsing context, applying semantic gatekeeping, and iteratively refining responses. [8]
- **`semantic_gatekeeper.py`**: Validates and critiques user-provided JSON output against specified keys, ensuring grounding and structured content. [9]

### 👥 Used By (Downstream)
- **`agent_util.py`**

---
## 📦 Module: `summary_models.py`
**Role:** The module `summary_models.py` defines and manages the structured context of a module using classes such as Claim, GroundedText, Alert, and ModuleContext to encapsulate its role, dependencies, dependents, public API, alerts, and claims.

**Impact Analysis:** Changes to this module will affect: agent_core.py, agent_util.py, component_analyst.py, dependency_analyst.py, map_synthesizer.py, module_contextualizer.py, report_renderer.py [1]

### 🧩 Interface & Logic
- **`🔌 class Alert`**: Data container for Alert records. [2]
- **`🔌 class Claim`**: Computes SHA1 hash of concatenated string representation. [3]
- **`🔌 class GroundedText`**: Data container for GroundedText records. [4]
- **`🔌 class ModuleContext`**: Manages context for a module, initializing attributes such as file path, archetype, role, dependencies, dependents, public API, alerts, and claims. [5]
- **`🔌 🔌 Claim.id`**: Computes SHA1 hash of concatenated string representation [6]
- **`🔌 🔌 ModuleContext.add_alert`**: Adds an alert to the alerts list. [7]
- **`🔌 🔌 ModuleContext.add_dependency_context`**: Adds dependency context to `key_dependencies` dictionary. [8]
- **`🔌 🔌 ModuleContext.add_dependent_context`**: Adds dependent context for a module path by combining explanation and supporting claims into full text, then storing it in `key_dependents` dictionary with associated claim IDs. [9]
- **`🔌 🔌 ModuleContext.add_public_api_entry`**: Adds an entry to the public API dictionary mapping entity name to GroundedText containing description and supporting claim IDs. [10]
- **`🔌 🔌 ModuleContext.set_module_role`**: Updates the module's role by appending provided text and claim placeholders, storing supporting claims' IDs. [11]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`agent_util.py`**
- **`component_analyst.py`**
- **`dependency_analyst.py`**
- **`map_synthesizer.py`**
- **`module_contextualizer.py`**
- **`report_renderer.py`**

---
## 🔧 Configuration

## 📦 Module: `agent_config.py`
**Role:** Defines configuration constants.

**Impact Analysis:** Changes to this module will affect: agent_core.py, semantic_gatekeeper.py, task_executor.py [1]

### 🧩 Interface & Logic
- **`🔌 CONTEXT_LIMIT`**: Defines global constant `CONTEXT_LIMIT`. [2]
- **`🔌 DEFAULT_MODEL`**: Defines global constant `DEFAULT_MODEL`. [3]
- **`🔌 SMART_MODEL`**: Defines global constant `SMART_MODEL`. [4]

### 👥 Used By (Downstream)
- **`agent_core.py`**
- **`semantic_gatekeeper.py`**
- **`task_executor.py`**

---