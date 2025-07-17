# CI/CD Pipeline Diagrams

This document provides diagrams for both the internal and external CI/CD pipelines used in the hr_analysis project.

---

## Internal CI/CD Pipeline (Makefile-based)

```mermaid
graph TD
    A["Developer runs<br>make <target>"] --> B["Makefile executes<br>run.sh <function>"]
    B --> C["run.sh script runs<br>the requested function"]
    C --> D["Local artifacts generated<br>(test reports, build dists)"]
    D --> E["Results displayed<br>in terminal"]
```

-   **Trigger**: Manual execution by the developer.
-   **Environment**: Local developer machine.
-   **Logic**: The `Makefile` acts as a simple command runner, delegating all tasks to the `run.sh` script. This keeps the CI logic centralized.
-   **Use Case**: Quick, iterative development cycles for linting, testing, and building before committing code.

---

## External CI/CD Pipeline (GitHub Actions)

```mermaid
graph TD
    A["Push or PR<br>to main branch"] --> B["GitHub Actions<br>workflow triggered"]
    B --> C["Job:<br>check-version-txt"]
    B --> D["Job:<br>build-wheel-and-sdist"]
    D --> E["Job:<br>lint-format-and-static-code-checks"]
    D --> F["Job:<br>execute-tests"]
    E --> G["Job: publish<br>(if all jobs succeed<br>and event is push to main)"]
    F --> G
    G --> H["Push tags<br>and optionally<br>publish to PyPI"]
```

-   **Trigger**: Automatic on `push` to `main`, `pull_request` to `main`, or `workflow_dispatch`.
-   **Environment**: GitHub-hosted runners (`ubuntu-latest`).
-   **Logic**: A multi-job workflow with dependencies. Artifacts (wheel/sdist) are passed between jobs to ensure that the exact same built package is tested and published.
-   **Use Case**: Automated quality assurance, continuous integration, and continuous deployment/delivery.

---

These diagrams illustrate the flow and responsibilities of both internal and external CI/CD pipelines in the project.
