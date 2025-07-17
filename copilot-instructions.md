# Guidelines for AI-Assisted Application Development

This document outlines the core principles to follow when writing, modifying, or refactoring code for this project. The primary goal is to maintain a clean, organized, and predictable codebase that is easy for both humans and other AIs to understand and extend.

## 1. Codebase and File Structure

*   **Principle of Least Disruption:** Always prefer modifying existing files over creating new ones. A new file should only be created if it introduces a completely new, high-level concept (e.g., adding a `sound_manager.py` module). For any new feature, first identify the existing files where the logic belongs.

*   **Respect the Existing Architecture:** Place new code where similar code already exists. Follow the established separation of concerns.
    *   *Example:* UI-related code goes in the UI module, data-handling logic goes in the data module, configuration constants go in `settings.py`. Do not add game logic to the main entry point file if it belongs in a specific class file like `car.py`.

*   **Atomic Commits:** When asked to implement a change, only provide the code for the files that were modified. Do not resubmit the entire codebase for every change.

## 2. Code Implementation and Style

*   **Maintain a Consistent Style:** New code must match the style and formatting (e.g., PEP 8 in Python) of the existing code. This includes naming conventions for variables, functions, and classes (e.g., `snake_case` for functions, `PascalCase` for classes).

*   **DRY (Don't Repeat Yourself):** If you find yourself writing code that is very similar to code elsewhere in the project, stop and suggest a refactor. Create a reusable function or class to handle the duplicated logic.

*   **Functionality First, Then Refactor:** When adding a new feature, prioritize getting it working correctly first within the existing structure. Once confirmed, you can suggest or perform refactoring to improve the integration.

## 3. Documentation and Communication

*   **Document As You Go:** All new functions, classes, and complex code blocks must be documented.
    *   Add clear **docstrings** to functions and classes explaining their purpose, arguments, and what they return.
    *   Add inline **comments** to explain *why* a certain piece of code is necessary, especially if the logic is not obvious.

*   **Context is Key: Explain Your Changes:** Do not just provide a block of code. Before presenting the code, briefly explain *what* you changed, *where* you changed it, and *why* you made that choice.
    *   **Good Example:** "Okay, I will add the nitro boost feature. I will add an `is_boosting` attribute and a `nitro_fuel` variable to the `Car` class in `car.py`. Then, I will modify the `handle_input` section in `main.py` to trigger the boost."
    *   **Bad Example:** "Here is the new code."

*   **Assume Nothing; Ask for Clarification:** If a request is ambiguous or could be interpreted in multiple ways, ask for more details before writing any code.
    *   *Example:* "You asked for a 'power-up.' To implement this correctly, I need to know: should it be a temporary speed boost, a shield, or something else?"

## 4. State and Dependency Management

*   **Acknowledge the Current State:** Before implementing a change, briefly confirm your understanding of the relevant code you are about to modify. This ensures you are working with the latest version.

*   **Manage Dependencies Explicitly:** If a new feature requires a new external library, you must explicitly state the library's name and the reason for adding it. Also, specify that the `requirements.txt` file needs to be updated.