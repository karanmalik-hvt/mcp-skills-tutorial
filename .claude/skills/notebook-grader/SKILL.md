---
name: notebook-grader
description: >
  Grade student Jupyter notebook submissions by checking exercise completion,
  assertion results, and TODO markers. Use when an instructor asks to check,
  grade, or review a student's notebook submission. Also use when asked to
  generate a completion report or check how many exercises are done.
  Do NOT use for editing notebooks or helping students solve exercises.
license: Proprietary
metadata:
  author: hexaview-ai-team
  version: "1.0"
  skill-type: automation
---

# Notebook Grader

## When to use this skill
Activate when:
- An instructor asks to "grade", "check", or "review" a student notebook
- Someone asks "how many exercises are completed?"
- Someone asks for a "completion report" or "submission status"
- Checking a batch of student submissions from GitHub Classroom

Do NOT use when a student asks for help solving an exercise — use hints instead.

## Grading workflow

### Phase 1: Parse the notebook
1. Read the .ipynb file as JSON
2. Identify exercise cells by looking for `# EXERCISE` markers in code cells
3. Count total exercises found

### Phase 2: Check each exercise
For each exercise cell, check:

4. **TODO status**: Search for `# TODO` or `raise NotImplementedError` in the cell
   - If found → exercise is NOT completed
   - If absent → student has written code (may or may not be correct)

5. **Code presence**: Check if the cell has meaningful code beyond the skeleton
   - Look for lines that aren't comments, blank, or the original skeleton
   - A cell with only `pass` or `None` is not completed

6. **Assertion cells**: Find the test/assertion cells that follow each exercise
   - Look for `assert` statements or `print("All assertions passed")`
   - If present, note which assertions the student needs to pass

### Phase 3: Run the grading script (optional)
7. If thorough grading is requested, run:
   ```
   python .claude/skills/notebook-grader/scripts/grade_notebook.py <notebook_path>
   ```
8. The script outputs a JSON report with per-exercise status

### Phase 4: Generate report
9. Produce the completion report using the template below

## Output format

ALWAYS use this exact structure:

```
## Notebook Grading Report

**File:** [notebook path]
**Student:** [from git blame or filename if available]
**Date:** [current date]

### Exercise Completion

| # | Exercise | Status | Notes |
|---|----------|--------|-------|
| 1 | [title]  | DONE / TODO / PARTIAL | [details] |
| 2 | [title]  | DONE / TODO / PARTIAL | [details] |
| ... | ... | ... | ... |

### Summary
- **Completed:** X / Y exercises
- **Partial:** X exercises (code written but TODOs remain)
- **Not started:** X exercises
- **Completion rate:** XX%

### Notes
[Any observations: common mistakes, hardcoded secrets, missing imports, etc.]
```

## Status definitions
- **DONE** — No TODOs remain, code is present, assertions exist
- **PARTIAL** — Some code written but TODOs or NotImplementedError remain
- **TODO** — Exercise is untouched (still has original skeleton)

## Gotchas
- Exercise numbering in notebooks starts at 1, but cell indices are 0-based
- Some exercises span multiple cells (e.g., Exercise 5 has safe_path + list_directory + read_file)
- The bonus Exercise 8 in the MCP notebook requires an API key — mark as N/A if .env is not configured
- Students may delete TODO comments but leave `pass` or `None` — check for actual implementation
- Assertion cells are separate from exercise cells — they follow immediately after
