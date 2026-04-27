# AGENTS.md

## Setup

- **Package manager**: uv (not pip/poetry). Use `uv sync --all-groups` to install all dependency groups (dev + docs). Use `uv run <cmd>` to execute.
- **Python**: 3.13–3.14 only (`>=3.13,<3.15`).

## Commands

```bash
uv run ruff check --fix    # lint (ALL rules, numpy docstring convention)
uv run ruff format         # format
uv run mypy src tests      # typecheck (strict)
uv run pytest              # run all tests (includes doctests)
uv run pytest tests/portabellas/containers/_column/test_init.py  # single test file
uv run pytest --cov=portabellas  # with coverage
uv run pre-commit run --all-files  # run all pre-commit hooks
```

Run lint → format → typecheck → test before committing:
```bash
uv run ruff check --fix && uv run ruff format && uv run mypy src tests && uv run pytest tests
```

## Development Workflow

- **Never commit directly to `main`**. Always develop on a separate feature branch.
- **Write failing tests first**, then implement just enough to pass (TDD).
- Cover all lines and edge cases with a **minimal** number of tests. Don't duplicate coverage.
- **Small, incremental commits** per logical change — not one giant commit per feature.

### Commit Conventions

- **Conventional commits** for all commit messages (required for semantic-release version bumps):
  - `feat:` new feature → minor version bump
  - `fix:` bug fix → patch version bump
  - `refactor:`, `test:`, `docs:`, `perf:`, `build:`, `ci:` for other changes (no version bump)
  - `feat!:` or `BREAKING CHANGE:` in footer → major version bump
- Scope is optional: `feat(containers): add Column.sort()`.
