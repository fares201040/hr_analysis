# Python Code Instructions

When modifying or creating Python files in this project, follow these rules:

## 1. Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) for code formatting and style.
- Use 4 spaces per indentation level.
- Limit lines to 79 characters.
- Use meaningful variable, function, and class names.

## 2. Type Hints
- Use [PEP 484](https://peps.python.org/pep-0484/) type hints for all function and method signatures.
- Add return type annotations.

## 3. Docstrings & Comments
- Add [PEP 257](https://peps.python.org/pep-0257/) compliant docstrings to all public modules, classes, and functions.
- Use inline comments sparingly and only when necessary to clarify complex logic.

## 4. Imports
- Group imports in the following order: standard library, third-party, local application.
- Use absolute imports where possible.
- Avoid wildcard imports (`from module import *`).

## 5. Error Handling
- Use exceptions for error handling.
- Catch only specific exceptions.
- Add helpful error messages.

## 6. Testing
- Write unit tests for new features and bug fixes.
- Use `pytest` as the testing framework.
- Place tests in a `tests/` directory or alongside the module as appropriate.

## 7. Dependencies
- Add new dependencies to `requirements.txt` or `pyproject.toml` as appropriate.
- Avoid unnecessary dependencies.

## 8. Security
- Do not hardcode secrets, passwords, or API keys.
- Validate and sanitize all external inputs.

## 9. Performance
- Write efficient code; avoid unnecessary computations or memory usage.
- Use list comprehensions and generator expressions where appropriate.

## 10. Version Control
- Write clear, concise commit messages.
- Do not commit generated files or secrets.

---

*Update these instructions as needed to reflect project-specific