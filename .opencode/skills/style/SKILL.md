---
name: style
description: Code style: Ruff select = ALL, line length 120, numpy docstrings, mypy strict, circular import handling, optional deps, no-comments rule.
compatibility: opencode
---

## Style & Linting

- **Ruff**: `select = ["ALL"]` (not the default), with various rules overridden in `pyproject.toml`.
- **Line length**: 120 (not ruff default 88).
- **Docstring convention**: numpy.
- **mypy**: strict, but `disallow_any_generics = false`, `disallow_untyped_decorators = false`, `no_warn_return_any = true`.
- **Circular imports**: Late-import inside the method body with a `# circular import  # noqa: PLC0415` comment. Only use late imports for genuinely circular dependencies — verify before adding. Non-circular imports should be at the top of the file.
- **Optional dependencies**: Guard optional dependency imports at the top of the file with `try/except ImportError`, raising an `ImportError` with install instructions. Use `importlib.util.find_spec` to check availability without importing.
- **No comments** in code unless explicitly requested or to explain gotchas (e.g., the `# circular import` comment). No emojis.
