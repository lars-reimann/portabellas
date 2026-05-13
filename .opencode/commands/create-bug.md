---
description: Create a bug report
---

Create a bug report GitHub issue based on the description below. If no description was provided, ask the user for one before proceeding.

Bug description: $ARGUMENTS

Follow these steps:

1. **Gather details**: If the description is vague, ask the user clarifying questions about:
   - What exactly goes wrong
   - Steps to reproduce
   - What the expected behavior should be
   - Any relevant context (e.g., OS, Python version)
2. **Draft the issue**: Write a clear title and body. For the body format, load the `gh-cli` skill and use the bug report template.
3. **Confirm with the user**: Show the draft title and body. Ask the user to approve or request changes.
4. **Create the issue**: Once approved, write the body to a temp file and run:
   `gh issue create --label "bug" --title "<title>" --body-file "<body file>"`
5. **Delete the body file**
