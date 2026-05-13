---
description: Create a feature request
---

Create a feature request GitHub issue based on the description below. If no description was provided, ask the user for one before proceeding.

Feature description: $ARGUMENTS

Follow these steps:

1. **Gather details**: If the description is vague, ask the user clarifying questions about:
   - What problem this feature would solve
   - What the desired solution looks like
   - Any alternative approaches they've considered
2. **Draft the issue**: Write a clear title and body. For the body format, load the `gh-cli` skill and use the feature request template.
3. **Confirm with the user**: Show the draft title and body. Ask the user to approve or request changes.
4. **Create the issue**: Once approved, write the body to a temp file and run:
   `gh issue create --label "enhancement" --title "<title>" --body-file "<body file>"`
5. **Delete the body file**
