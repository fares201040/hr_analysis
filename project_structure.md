# Project Structure: hr_analysis

This document describes the structure of the hr_analysis project, including the purpose of each main directory and file.

## Root Directory
- `Makefile` — Automation for build, test, lint, and CI/CD tasks.
- `pyproject.toml` — Project metadata and dependencies.
- `README.md` — Project overview, usage, and documentation.
- `run.sh` — Shell script for running the project or setup tasks.
- `version.txt` — Project version information.

## src/
- `hr_analysis/` — Main source code package for the project.
  - `__init__.py` — Marks the directory as a Python package.
  - `cities.json` — JSON file with city-related data (likely for HR analytics).
  - `states_info.py` — Python module for state-related HR data or logic.
- `hr_analysis.egg-info/` — Metadata for Python packaging (auto-generated).

## tests/
- `__init__.py` — Marks the directory as a Python package.
- `conftest.py` — Pytest configuration and fixtures.
- `consts.py` — Constants for tests.
- `fixtures/` — Directory for reusable test fixtures.
  - `example_fixture.py` — Example or template fixture.
- `unit_tests/` — Directory for unit tests.
  - `__init__.py` — Marks the directory as a Python package.
  - `test_states_info.py` — Unit tests for `states_info.py`.

## .github/
- `copilot-instructions.md` — Project-specific instructions for Copilot and contributors.
- `workflows/` — GitHub Actions workflows for CI/CD.
- `instructions/` — Additional coding and process instructions.

---

This structure supports modularity, testing, automation, and future scalability, following best practices for Python and data analytics projects.
