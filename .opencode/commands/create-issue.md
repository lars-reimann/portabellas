---
description: Create a blank issue
---

Create a blank GitHub issue based on the description below. If no description was provided, ask the user for one before proceeding.

Issue description: $ARGUMENTS
Body file: !`date +.opencode_tmp_%Y%m%d_%H%M%S.md`

Follow these steps:

1. **Gather details**: If the description is vague, ask the user clarifying questions. Also ask if they want any labels applied (e.g., `documentation`, `good first issue`, `question`).
2. **Draft the issue**: Write a clear title and body. The body format is free-form — use whatever structure best fits the issue.
3. **Confirm with the user**: Show the draft title and body. Ask the user to approve or request changes.
4. **Create the issue**: Once approved, write the body to the body file and run:
   `gh issue create --title "<title>" --body-file "<body file>"`
   No template is used.
5. **Delete the body file**
