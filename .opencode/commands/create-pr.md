---
description: Create a PR for the current branch
---

Create a GitHub pull request for the current branch. If additional context was provided, use it when drafting the PR. Otherwise, infer the PR content from the commit history and linked issue.

Additional context: $ARGUMENTS

Follow these steps:

1. **Gather branch info**: Run the following in parallel:
   - `git status` to check for uncommitted changes (warn the user if any exist)
   - `git log main..HEAD --oneline` to see all commits on this branch
   - `git diff main...HEAD` to see the full diff
   - `git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null` to check if the branch tracks a remote
2. **Push if needed**: If the branch has no upstream, push it with `git push -u origin HEAD`.
3. **Draft the PR**: Write a title and body based on the commits and changes. The title should follow the same style as the commit messages (conventional commits). For the body format, load the `gh-cli` skill and use the pull request template.
4. **Confirm with the user**: Show the draft title and body. Ask the user to approve or request changes.
5. **Create the PR**: Once approved, write the body to a temp file and run:
   `gh pr create --title "<title>" --body-file "<body file>"`
6. **Delete the body file**
