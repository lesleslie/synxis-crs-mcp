# Python Coding Standards for synxis-crs-mcp

## General Principles

1. **Type Hints**: Use type hints for all function signatures and complex variables
2. **Docstrings**: Google-style docstrings for all modules, classes, and public functions
3. **Error Handling**: Never suppress exceptions - handle them appropriately or let them propagate
4. **Code Style**: Follow PEP 8 with Ruff formatter (line length 88)

## Import Order

1. Standard library imports
2. Third-party imports
3. Local application imports
4. Separate each group with blank line

## Naming Conventions

- **Modules**: `lowercase_with_underscores`
- **Classes**: `CapitalizedWords`
- **Functions/Variables**: `lowercase_with_underscores`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: `_leading_underscore`

## Testing

- Use pytest with asyncio support
- Mark tests appropriately: `unit`, `integration`, `slow`
- Aim for >80% test coverage
- Use descriptive test names that explain what is being tested

## Security

- Run bandit for security checks before committing
- Never hardcode credentials or API keys
- Use environment variables for configuration
