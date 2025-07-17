# Copilot Instructions for hr_analysis

## Project Overview
- Generates HR analytics reports and interactive dashboards from CSV data.
- Main code in `src/hr_analysis/`, tests in `tests/`, automation in `Makefile` and `run.sh`.

## Architecture & Data Flow
- **Data Source:** HR data in CSV, with supporting JSON (e.g., `cities.json`).
- **Core Logic:** Python modules in `src/hr_analysis/` (e.g., `states_info.py` for city/state logic).
- **Visualization:** Use `pandas`, `plotly`, `dash`, `seaborn`, `scipy`, `xlwings`.
- **Configuration:** All config in JSON; secrets in `.env` (never hardcode).
- **Extensibility:** Structure supports future API backend (follow modular, API-ready patterns).

## Developer Workflows
- **Install Dev Dependencies:** `make install` (calls `run.sh install`)
- **Run Tests:** `make test` or `run.sh test:ci` (uses pytest, coverage, junit XML)
- **Lint & Format:** `make lint` (local), `make lint-ci` (CI, auto-fixes and commits, then strict check)
- **Build Package:** `make build` (calls `run.sh build`)
- **Clean Artifacts:** `make clean`
- **Serve Coverage Report:** `make serve-coverage-report` (serves HTML on localhost:8000)
- **CI/CD:** 
  - Internal: Makefile + run.sh (see diagrams in `diagrams/`)
  - External: GitHub Actions (`.github/workflows/build-test-publish.yaml`)

## Project-Specific Patterns
- **All new functions/classes require unit tests** (see `tests/unit_tests/`).
- **Document tested code in `README.md`** with references to files and logic.
- **Error Handling:** Use `raise` for errors; logging is centralized later.
- **Pre-commit hooks:** Enforced via `pre-commit` (auto-installed in CI).
- **Cross-platform:** All scripts and code must work on Windows and Linux.

## Integration & Conventions
- **No hardcoded secrets/config:** Use `.env` and JSON config.
- **Imports:** Absolute imports, grouped stdlib/third-party/local.
- **Type Hints:** Required for all functions (see `app.instructions.md`).
- **Docstrings:** PEP 257 for all public code.
- **Testing:** Use `pytest`, mark slow tests with `@pytest.mark.slow`.

## Key Files & Directories
- `src/hr_analysis/`: Main logic and data files.
- `tests/`: All tests, fixtures, and test constants.
- `Makefile`, `run.sh`: All automation, build, test, and CI logic.
- `.github/workflows/`: GitHub Actions for CI/CD.
- `diagrams/`: Mermaid diagrams for CI/CD and logic flows.
- `README.md`, `project_structure.md`: Documentation and structure.

## Git Commit and Commit Message Generation
Be extremely detailed with the file changes and the reason for the change.

## Code Generation
Always generate the endpoints in the `reports_summary.md` and `report_details.md` files, including a reference number that matches the corresponding report number in `report_details.md`. Imports block and any initialization code should be at the top of the file.
The code should be modular, reusable, and follow the project's architecture. Use the existing patterns and structures as a guide for new code. Always ensure that new code is well-documented and tested.

---

Please review and let me know if any section is unclear or missing important project-specific details!

---

*Use this file to specify what you need and how you want the project to be done. Update sections as the project evolves.*