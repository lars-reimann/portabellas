---
description: Start work on a GitHub issue
---

Start work on the GitHub issue below. If the issue number was not provided, ask the user for it before proceeding.

Issue number: $ARGUMENTS
Body file: !`date +.opencode_tmp_%Y%m%d_%H%M%S.md`

Follow these steps:

1. **Fetch the issue**: `gh issue view <number> --json title,body,labels`
2. **Understand the issue**: Read the issue title, body, and labels. Ask clarifying questions if anything is ambiguous.
3. **Create a feature branch**: Use a descriptive name like `feat/<short-description>` or `fix/<short-description>`, based on the issue type. Never commit directly to `main`.
4. **Plan the implementation**: Identify which files need to change, what new files to create, and what tests to write. Use the project conventions documented in AGENTS.md.
5. **Write failing tests first** (TDD): Cover all lines and edge cases with a minimal number of tests.
6. **Implement just enough to pass**: Make the tests green.
7. **Run lint, format, typecheck, and tests**: `uv run ruff check --fix && uv run ruff format && uv run mypy src tests && uv run pytest tests`
8. **Commit with conventional commits**: Use `feat:`, `fix:`, `refactor:`, `test:`, etc. Scope is optional (e.g., `feat(containers): add Column.sort()`).
