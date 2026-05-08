---
description: Create a bug report
---

Create a bug report GitHub issue based on the description below. If no description was provided, ask the user for one before proceeding.

Bug description: $ARGUMENTS
Body file: !`date +.opencode_tmp_%Y%m%d_%H%M%S.md`

Follow these steps:

1. **Gather details**: If the description is vague, ask the user clarifying questions about:
   - What exactly goes wrong
   - Steps to reproduce
   - What the expected behavior should be
   - Any relevant context (e.g., OS, Python version)
2. **Draft the issue**: Write a clear title and body in this format:

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
3. **Confirm with the user**: Show the draft title and body. Ask the user to approve or request changes.
4. **Create the issue**: Once approved, write the body to the body file and run:
   `gh issue create --label "bug" --title "<title>" --body-file "<body file>"`
5. **Delete the body file**
