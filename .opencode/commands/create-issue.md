---
description: Create a blank issue
---

Create a blank GitHub issue based on the description below. If no description was provided, ask the user for one before proceeding.

Issue description: $ARGUMENTS

Follow these steps:

1. **Gather details**: If the description is vague, ask the user clarifying questions. Also ask if they want any labels applied (e.g., `documentation`, `good first issue`, `question`).
2. **Draft the issue**: Write a clear title and body. For the body format, load the `gh-cli` skill and use the blank issue template (free-form).
3. **Confirm with the user**: Show the draft title and body. Ask the user to approve or request changes.
4. **Create the issue**: Once approved, write the body to a temp file and run:
   `gh issue create --title "<title>" --body-file "<body file>"`
5. **Delete the body file**
