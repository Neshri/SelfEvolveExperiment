# Project Verification Proof

This document contains the AST-derived evidence and line ranges for all architectural claims.

## 📦 Verification: `sandboxer_graph_main.py`
### 🆔 Verification Claims

> 🆔 `a8a7c1` [1]: orchestrates copying of specified graph from evolving_graphs_dir to candidates directory and returns its absolute path _(Source: Synthesis (based on [4], [5], [3], [2]))_
> 🆔 `d1b7ff` [2]: Assigns parsed command-line arguments to the variable `args`. _(Source: args)_
>   - **Evidence (L27-27):**
>     ```python
>     args = parser.parse_args()
>     ```
> 🆔 `6b86bd` [3]: Copies the specified graph from the `evolving_graphs_dir` directory to the `candidates` directory, creating it if necessary, and returns the absolute path of the copied destination. _(Source: main)_
>   - **Evidence (L5-22):**
>     ```python
>     def main(graph_folder: str) -> str:
>         """
>         Create a copy of the specified graph and return its path.
>     
>         Args:
>             graph_folder (str): The graph folder to copy.
>     
>         Returns:
>             str: The absolute path of the copied graph folder.
>         """
>         script_dir = os.path.dirname(os.path.abspath(__file__))
>         evolving_graphs_dir = os.path.dirname(script_dir)
>         source_path = os.path.join(evolving_graphs_dir, graph_folder)
>         candidates_dir = os.path.join(evolving_graphs_dir, "candidates")
>         os.makedirs(candidates_dir, exist_ok=True)
>         destination_path = os.path.join(candidates_dir, graph_folder)
>         shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
>         return os.path.abspath(destination_path)
>     ```
> 🆔 `223e4a` [4]: Assigns an ArgumentParser object to the variable `parser`, specifying its description as 'Create a copy of the specified graph and return its path.'. _(Source: parser)_
>   - **Evidence (L25-25):**
>     ```python
>     parser = argparse.ArgumentParser(description="Create a copy of the specified graph and return its path.")
>     ```
> 🆔 `636e6d` [5]: Assigns the result of calling `main(args.graph)` to `path`. _(Source: path)_
>   - **Evidence (L29-29):**
>     ```python
>     path = main(args.graph)
>     ```

---