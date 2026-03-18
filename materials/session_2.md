# SESSION 2 — Python Environments, Libraries & UV

**Goal:** Understand Python environment isolation, dependency management, and the modern `uv` toolchain.

---

## 2.1 Why Isolation Matters

### Libraries: Why We Need Them

A Python **library** is reusable code written by someone else that we can import into our own programs instead of building everything from scratch.

Typical examples:

- `requests` for HTTP calls
- `pandas` for data analysis
- `matplotlib` for plotting and visualizations
- `fastapi` for web APIs
- `pytest` for testing

Libraries let us:

- save time by reusing existing solutions
- work at a higher level of abstraction
- rely on community-tested tools
- focus on the specific logic of our own project

Without libraries, even simple tasks such as sending a web request, parsing data files, or writing tests would require much more code and effort.

### The Problem Without Isolation

Different projects often need different Python versions and different library versions.

```
System Python
├── Python 3.8     ← Project A requires this
├── Python 3.13    ← Project B requires this   (CONFLICT)
├── requests 2.28  ← Project A needs this
└── requests 2.31  ← Project B needs this      (CONFLICT)
```

If both projects depend on the same global Python setup, one project can break the other. This is part of the broader problem of **dependency hell**.

### The Solution: Virtual Environments

A virtual environment is an isolated copy of the Python interpreter and a private set of installed packages. Projects do not share packages.

```
projects/
├── project_a/
│   └── .venv/          ← isolated: requests 2.28 only
└── project_b/
    └── .venv/          ← isolated: requests 2.31 only
```

---

## 2.2 Traditional Virtual Environments (`venv`)

### First: `pip` Installs Libraries

Python itself does not include most of the libraries we use in real projects. To add them, we use `pip`, the standard Python package installer.

- A **library** is reusable code written by someone else
- `pip` downloads and installs that library from PyPI (the Python Package Index)
- Examples: `requests` for HTTP, `pandas` for data analysis, `fastapi` for web APIs

```bash
# Install a library
pip install requests

# Install a specific version or version range
pip install "pandas==2.1.4"
pip install "fastapi>=0.100"
```

The problem is that if you run `pip install` globally, every project shares the same installed packages. That brings us back to dependency conflicts.

### Then: Create an Isolated Environment

```bash
# Create a virtual environment in the current directory
python -m venv .venv

# Activate it
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows PowerShell

# Confirm you are inside the venv
which python                     # → .../project/.venv/bin/python
python --version
```

Once the environment is activated, `pip` installs packages inside `.venv` instead of into the global Python installation.

```bash
# Install libraries inside the active virtual environment
pip install requests
```

### Freezing and Restoring Dependencies

```bash
# Save exact versions of everything installed
pip freeze > requirements.txt

# Restore in another environment
pip install -r requirements.txt
```

### The Problem with `pip freeze`

`requirements.txt` records _all_ packages including transitive dependencies — packages your packages depend on. This creates noise and can cause conflicts when versions change upstream.

```
# requirements.txt from `pip freeze` — hard to maintain
certifi==2026.2.25
charset-normalizer==3.4.6
idna==3.11
requests==2.32.5     ← the one you actually care about
urllib3==2.6.3
```

---

## 2.3 Modern Dependency Management

### `pyproject.toml` — The Modern Standard

Python Enhancement Proposals 517/518 (2015) introduced `pyproject.toml` as the single configuration file for Python projects. It replaces `setup.py`, `setup.cfg`, and `requirements.txt` for most use cases.

Key advantages:

- You declare _intent_ (e.g. `fastapi>=0.100`), not locked versions
- A lock file records the exact resolved versions separately
- Dev dependencies are separate from runtime dependencies

---

## 2.4 UV — The Modern Python Toolchain (since 2024)

### What is UV?

UV (by Astral, the team behind Ruff) is a single tool written in Rust that replaces:

| Old tool                                | UV equivalent                 |
| --------------------------------------- | ----------------------------- |
| `pip`                                   | `uv pip`                      |
| `pip-tools`                             | `uv pip compile`              |
| `virtualenv` / `venv`                   | `uv venv`                     |
| `pyenv`                                 | `uv python install`           |
| `poetry` / `hatch` (project management) | `uv init`, `uv add`, `uv run` |

### Why UV?

- **Speed:** 10–100× faster than pip for installs and dependency resolution
- **Single binary:** no separate tool per task
- **Deterministic:** lock file guarantees identical environments everywhere
- **Python version management:** install and switch Python versions without pyenv

### Installing UV

https://docs.astral.sh/uv/getting-started/installation/#installation-methods

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify
uv --version
```

---

## 2.5 UV Workflow

### Starting a New Project

```bash
# Create project with pyproject.toml, .venv, and lock file
uv init my-project
cd my-project

# Tree view of what was created
my-project/
├── .venv/               ← automatically created
├── pyproject.toml       ← project metadata and dependencies
├── uv.lock              ← exact resolved versions (commit this)
├── .python-version      ← pinned Python version
└── hello.py
```

### Managing Python Versions

```bash
# List available Python versions
uv python list

# Install a specific version
uv python install 3.13

# Pin the project to a version
uv python pin 3.13
```

### Adding Dependencies

```bash
# Add a runtime dependency
uv add pandas numpy matplotlib

# Add a dev-only dependency
uv add --dev jupyter pytest ipykernel

# Remove a dependency
uv remove requests
```

### Running Code

```bash
# Run a script inside the project environment (no manual activation needed)
uv run python main.py

# Run a tool (installs temporarily if not present)
uv run pytest
```

### Syncing an Existing Project

```bash
# Clone a repo, then:
uv sync                   # installs exact versions from uv.lock
uv sync --dev             # includes dev dependencies
```

### The Lock File

`uv.lock` is automatically generated and updated. It records the exact version of every package in the dependency tree.

```
# Fragment of uv.lock
[[package]]
name = "fastapi"
version = "0.111.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
  { name = "pydantic", version = "2.7.1" },
  { name = "starlette", version = "0.37.2" },
]
```

**Always commit `uv.lock` to version control.** This ensures every developer and every CI run uses identical package versions.

### Comparison: UV vs Traditional Workflow

| Task              | Traditional                               | UV                       |
| ----------------- | ----------------------------------------- | ------------------------ |
| Create env        | `python -m venv .venv` + activate         | `uv init` or `uv sync`   |
| Install package   | `pip install X` + update requirements     | `uv add X`               |
| Install from lock | `pip install -r requirements.txt`         | `uv sync`                |
| Run script        | `source .venv/bin/activate && python ...` | `uv run python ...`      |
| Install Python    | install from python.org / pyenv           | `uv python install 3.14` |
| Speed (100 pkgs)  | ~30–60 seconds                            | ~2-5 seconds             |

---

## 2.6 Jupyter Notebook

### What is a Jupyter Notebook?

A Jupyter Notebook is an interactive document made of cells. Each cell can contain:

- Python code
- text explanations in Markdown
- equations
- tables, charts, and images

It is especially useful when you want to mix code, results, and explanations in the same document.

### Why use it?

Jupyter is widely used in data science, machine learning, teaching, and exploratory analysis because it makes experimentation faster.

Typical use cases:

- test code step by step
- inspect datasets interactively
- generate plots immediately
- document an analysis as you work
- share a reproducible workflow with others

For production applications, regular Python modules and scripts are usually better. Notebooks are best for exploration, prototyping, and teaching.

### How to set it up with UV

#### Open a Jupyter Notebook in your browser

Inside your project:

```bash
# Add notebook tools as development dependencies
uv add --dev jupyter ipykernel

# Start Jupyter Notebook
uv run jupyter notebook
```

This opens Jupyter in your browser and uses the project's virtual environment.

Then open a notebook file such as `sales_todo.ipynb` and select the correct kernel.

#### Use a Jupyter Notebook with VS Code

Another option is to open notebooks with VS Code. In that case, you do not need to install `jupyter`; you only need to add `ipykernel` as a development dependency:

```bash
uv add --dev ipykernel
```

When prompted to select a kernel, choose `Python Environments` and select the virtual environment you created earlier, for example `.venv/bin/python` on macOS and Linux, or `.venv\Scripts\python` on Windows.

### Typical workflow

```bash
# Clone the project
git clone https://github.com/your_username/your_project.git

# Install dependencies from the project lock file
uv sync --dev

# Launch Jupyter / Open with VS Code
uv run jupyter notebook
```

This ensures your notebook uses the same locked dependencies as the rest of the project.

---

## 2.7 Project Structure Example

```
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .venv/                  ← never committed
├── pyproject.toml          ← committed
├── uv.lock                 ← committed
├── .python-version         ← committed
├── .env.example            ← committed (no real secrets)
├── .env                    ← never committed
├── .gitignore
└── README.md
```
