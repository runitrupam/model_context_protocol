# Understanding UV (Ultraviolet) Package Manager

## What is UV?
UV (Ultraviolet) is a modern Python package installer and resolver written in Rust, designed to be an ultrafast alternative to pip. It gets its name from "Ultraviolet" to represent its speed and efficiency.

## Key Features
- 10-100x faster than traditional pip
- Written in Rust for optimal performance
- Parallel package downloads and installations
- Fully compatible with pip's interface
- Works with existing Python package ecosystem (PyPI)
- Supports both requirements.txt and pyproject.toml

## Setting Up UV with Virtual Environment

1. **Create and Activate Virtual Environment**
```bash
# Create new virtual environment
python3.12 -m venv .venv

# Activate virtual environment (for Mac)
source .venv/bin/activate
```

2. **Install UV**
```bash
pip install uv
```

3. **Install Dependencies**
Either using pyproject.toml:
```bash
uv pip install -e .
```

Or using requirements.txt:
```bash
uv pip install -r requirements.txt
```

4. **Verify Installation**
```bash
uv pip list
```

## Common UV Commands
```bash
uv pip install <package>          # Install a package
uv pip list                       # List installed packages
uv pip freeze                     # Output installed packages in requirements format
uv run --with <package> <script>  # Run script with temporary package installation
```

## UV vs requirements.txt
- With UV and pyproject.toml, you don't strictly need a requirements.txt file
- However, requirements.txt might be useful for:
  - Working with older tools that don't support pyproject.toml
  - Locking dependencies to specific versions
  - Deploying to environments that expect requirements.txt

## UV Special Features
- The `--with` flag allows temporary package installation for single commands
- Example:
  ```bash
  uv run --with mcp[cli] --with psycopg[binary] mcp run server.py
  ```

## Why Use UV?
1. **Performance**: Significantly faster package installation and resolution
2. **Compatibility**: Works seamlessly with existing Python tooling
3. **Modern**: Takes advantage of newer Python packaging standards
4. **Convenience**: Features like temporary package installation with `--with`

## Project-Specific Usage
In this project, UV is used to:
1. Manage dependencies listed in both pyproject.toml and requirements.txt
2. Run MCP servers with temporary dependencies
3. Handle package installation in virtual environments

## FAQ

Q: Do I need requirements.txt if I'm using UV?
A: Not strictly necessary if using pyproject.toml, but it can be useful for compatibility and dependency locking.

Q: Can I use UV in an existing virtualenv?
A: Yes, you can install UV in any existing virtualenv and start using it immediately.

Q: What's the relationship between UV and pip?
A: UV implements pip's interface for familiarity but provides faster performance and additional features.