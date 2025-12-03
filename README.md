# aoc

Tools and helpers to solve Advent of Code puzzles.

## Installation

### From PyPI

```bash
uv add aoc
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/spossner/aoc-lib.git
cd aoc

# Install with dev dependencies
uv sync --extra dev

# Or install as editable in another project
uv add --editable /path/to/aoc-lib
```

## Usage

```python
from aoc import hello

print(hello())
```

## Development

```bash
# Install dev dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Run linter
uv run ruff check .

# Run type checker
uv run mypy src/

# Format code
uv run ruff format .
```

## Publishing to PyPI

```bash
# Build the package
uv build

# Publish (requires PyPI token)
uv publish
```
