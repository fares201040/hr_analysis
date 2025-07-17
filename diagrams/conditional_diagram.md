# Conditional CI/CD Pipeline Diagrams

This document illustrates the conditional logic and decision points within the CI/CD pipelines of the `hr_analysis` project.

---

## Internal CI/CD (Makefile-based)

```mermaid
graph TD
    A["Developer runs<br>make <target>"] --> B{"Is target valid"}
    B -->|Yes| C["Execute run.sh<br>with function"]
    B -->|No| D["Show help message"]
    C --> E{"Is target lint:ci"}
    E -->|Yes| F["Run 2-pass linting:<br>auto-fix, commit,<br>strict linting"]
    E -->|No| G["Execute standard function<br>e.g. test/build"]
    F --> H{"Did script succeed"}
    G --> H
    H -->|Yes| I["Exit with code 0<br>Success"]
    H -->|No| J["Exit with non-zero code<br>Failure"]
```

- **Initial Check**: The `Makefile` first validates if the provided target exists.
- **`lint:ci` Logic**: This specific target has a unique two-pass mechanism to automatically fix and commit linting errors before a final strict check.
- **Error Handling**: The `run.sh` script is set to `set -e`, meaning it will exit immediately if any command fails, signaling a failure to the developer.

---

## External CI/CD (GitHub Actions)

```mermaid
graph TD
    A["Event triggers workflow<br>Push, PR, Dispatch"] --> B{"Does event match<br>on filters"}
    B -->|Yes| C["Start Workflow Jobs"]
    B -->|No| D["Skip Workflow"]
    C --> E["Jobs run in sequence<br>needs keyword<br>build -> lint, test"]
    E --> F{"Did all jobs succeed"}
    F -->|Yes| G["Continue to publish job"]
    F -->|No| H["Workflow fails<br>notify user"]
    G --> I{"Is event a push<br>to main branch"}
    I -->|Yes| J["Execute publish steps:<br>push tags, deploy to PyPI"]
    I -->|No| K["Skip publish job"]
```

- **Event Filtering**: The workflow only runs if the triggering event matches the conditions defined in the `on` section.
- **Job Dependencies**: The `needs` keyword creates a dependency graph, ensuring jobs run in the correct order. A failure in a dependency (e.g., `build-wheel-and-sdist`) will cause dependent jobs (e.g., `execute-tests`) to be skipped.
- **Conditional Publishing**: The `publish` job has a strict `if` condition, ensuring it only runs after all other jobs have succeeded *and* the trigger was a push to the `main` branch.

---

These diagrams clarify the decision-making processes that govern the CI/CD pipelines.
