---
description: Create a feature request
---

Create a feature request GitHub issue based on the description below. If no description was provided, ask the user for one before proceeding.

Feature description: $ARGUMENTS
Body file: !`date +.opencode_tmp_%Y%m%d_%H%M%S.md`

Follow these steps:

1. **Gather details**: If the description is vague, ask the user clarifying questions about:
   - What problem this feature would solve
   - What the desired solution looks like
   - Any alternative approaches they've considered
2. **Draft the issue**: Write a clear title and body in this format:
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
3. **Confirm with the user**: Show the draft title and body. Ask the user to approve or request changes.
4. **Create the issue**: Once approved, write the body to the body file and run:
   `gh issue create --label "enhancement" --title "<title>" --body-file "<body file>"`
5. **Delete the body file**
