---
description: Patterns for using the GitHub CLI (gh) with multi-line body content and body templates
---

# GitHub CLI (gh) Skill

## Body File Rule

Always use `--body-file` for any `gh` command that accepts a body (`pr create`, `pr edit`, `issue create`, etc.). Never pass body content inline via `--body` — the tool permission rules restrict shell output commands (`echo`, `cat`, `printf`), making inline HEREDOCs unreliable, and `--body` is fragile with multi-line strings and special characters.

Titles are single-line, so `--title "<title>"` is fine. No need for `--title-file`.

## Temp File Convention

- **Location**: Project root directory (not `/tmp`, which is blocked by external directory restrictions)
- **Naming**: `.opencode_tmp_<timestamp>.md` (e.g., `.opencode_tmp_20260513_143022.md`)
- **Generate filename**: `date +.opencode_tmp_%Y%m%d_%H%M%S.md`

## Workflow

1. Write the body content to the temp file using the `Write` tool
2. Run `gh ... --body-file <temp_file>` via the `Bash` tool
3. Delete the temp file via a separate `Bash` call (not chained with `&&`), even if the `gh` command failed

## Templates

### Pull Request

```
Closes #<issue_no>

### Summary of Changes

<Concise, precise bullet points in natural language, kept at a high level of abstraction. Mention specific names (e.g., a function or class) only where it helps clarity. Do not rehash commit messages or list implementation details. Explain WHY changes were made.>
```

If no issue is referenced, omit the `Closes #<issue_no>` line.

### Feature Request

```
### Is your feature request related to a problem?

<description of the problem>

### Desired solution

<description of the desired feature>

### Possible alternatives (optional)

<only include this section if the user mentioned alternative approaches>

### Additional context (optional)

<only include this section if there is relevant extra information>
```

### Bug Report

```
### Describe the bug

<concise description of the bug>

### To Reproduce

Steps to reproduce the behavior:

1. <step 1>
2. <step 2>
3. <step 3>

### Expected behavior

<what should happen instead>

### Additional context (optional)

<only include this section if there is relevant extra information>
```

### Blank Issue

Free-form — no template. Use whatever structure best fits the issue.
