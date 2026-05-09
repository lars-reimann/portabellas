---
description: Edit the body of an existing GitHub issue
---

Edit the body of an existing GitHub issue. The issue number and optional edit instructions are provided below. If no issue number was provided, ask the user for one before proceeding.

Arguments: $ARGUMENTS
Body file: !`date +.opencode_tmp_%Y%m%d_%H%M%S.md`

Follow these steps:

1. **Fetch the current issue**: Run `gh issue view <number> --json title,body` to get the current title and body.
2. **Determine the edits**: If edit instructions were provided alongside the issue number, apply them to the existing body. Otherwise, ask the user what changes they want to make.
3. **Show the updated body**: Present the full updated body to the user. Ask them to approve or request changes.
4. **Apply the edit**: Once approved, write the body to the body file and run:
   `gh issue edit <number> --body-file "<body file>"`
5. **Delete the body file**
