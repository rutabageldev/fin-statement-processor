# Ledgerly Statement Parser Project

## Project Overview

This is a Python-based financial statement parser that processes PDF statements and CSV transaction files for various account types (e.g., Citi credit cards). The project uses a modular architecture with parsers, models, and services.

## Key Architecture

- **Main Entry**: `main.py` - CLI interface for parsing statements
- **Parsers**: `services/parsers/` - Account-specific parsing logic
- **Models**: `models/` - Data models for transactions and statements
- **Registry**: `registry/` - Account type registry and configuration
- **Services**: `services/` - Logging and utility services

## Development Environment

- Python 3.12 in Docker container
- Uses pytest for testing
- Black for code formatting
- Development dependencies in `requirements-dev.txt`

## Common Commands

```bash
# Run parser
python main.py --account citi_cc --pdf ./path/to/statement.pdf --csv ./path/to/transactions.csv

# Run tests
pytest

# Format code
black .
```

## Development Notes

- Project runs in containerized environment
- Uses environment variables from `.env` file
- Supports multiple account types through registry pattern
- Processes both PDF statements and CSV transaction files

## File Structure

- `/app/main.py` - Main CLI entry point
- `/app/services/` - Core services and parsers
- `/app/models/` - Data models
- `/app/registry/` - Account registry
- `/app/tests/` - Test files and data
- `/app/samples/` - Sample files
- `/app/output/` - Generated output files

## Coding Conventions

- Use type hints for function parameters and return values
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Include docstrings for classes and functions
- Handle errors gracefully with proper logging
