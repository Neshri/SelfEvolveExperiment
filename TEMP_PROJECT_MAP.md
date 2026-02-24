# Project Context Map

**Total Modules:** 1

## 🚀 Entry Points

## 📦 Module: `sandboxer_graph_main.py`
**Role:** The module `sandboxer_graph_main.py` orchestrates copying the specified graph from the evolving graphs directory to the candidates directory and returns the absolute path of the destination. [1]

### 🧩 Interface & Logic
- **`🔌 args`**: Assigns the result of parsing command-line arguments to the global variable `args`. [2]
- **`🔌 main`**: Copies the specified graph from the evolving graphs directory to the candidates directory and returns the absolute path of the destination. [3]
- **`🔌 parser`**: Assigns an argument parser to the variable `parser`. [4]
- **`🔌 path`**: Assigns the result of calling the main function with the value from args.graph to path. [5]

---