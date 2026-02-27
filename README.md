# Project Name

This project follows the 3-layer architecture defined in `agent.md`.

## Structure

- **directives/**: Standard Operating Procedures (SOPs) in Markdown.
- **execution/**: Deterministic Python scripts.
- **.tmp/**: Temporary files (not committed).

## Usage

1. Define a goal in a directive.
2. The agent reads the directive.
3. The agent executes scripts in `execution/`.
