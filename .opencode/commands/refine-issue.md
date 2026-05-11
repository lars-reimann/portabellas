---
description: Interactively refine an existing GitHub issue
---

Interactively refine an existing GitHub issue, focusing on API design (e.g. function signatures, parameter names, return types). The issue number is provided below. If no issue number was provided, ask the user for one before proceeding.

Issue number: $ARGUMENTS
Body file: !`date +.opencode_tmp_%Y%m%d_%H%M%S.md`

Follow these steps:

1. **Fetch the current issue**: Run `gh issue view <number> --json title,body` to get the current title and body.
2. **Gather context**: Read the issue body carefully. Search the codebase for related existing code — find the classes, methods, and patterns that the proposed feature would interact with. Identify relevant conventions from AGENTS.md (especially the "API Design" section) that apply.
3. **Interactive refinement dialog**: Engage the user in a discussion about the API design. Focus on:
   - Proposed function/method signatures (names, parameters, return types)
   - How the new API fits with existing patterns (method naming, parameter conventions, immutability, etc.)
   - Edge cases and precondition checks
   - Type inference considerations (return `DataTypes.Unknown()` when uncertain)
   - Any ambiguities in the issue that need resolution
   - Whether the issue should be closed (e.g. if it's already addressed, out of scope, or better handled differently)
   - Whether the issue should be split into smaller, more focused issues (e.g. if it covers multiple independent features)
   Propose concrete signatures, suggest closing the issue, or suggest splitting it — and ask the user for feedback. Iterate until the user is satisfied with the outcome.
4. **Update the issue (only on request)**: When the user explicitly asks to update the issue, draft the updated body incorporating the refined API design. Show the full updated body and ask the user to approve or request changes. Once approved, write the body to the body file and run:
   `gh issue edit <number> --body-file "<body file>"`
   **Do not proactively edit the issue.** Only update when the user requests it.
5. Delete the body file.
