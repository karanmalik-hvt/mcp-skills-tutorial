---
name: skill-md-linter
description: >
  Validate SKILL.md files against the official specification. Checks frontmatter
  fields (name format, description quality, required fields) and body structure
  (recommended sections, gotchas, output templates). Use when creating, editing,
  or reviewing SKILL.md files. Also use when a student asks "is my SKILL.md correct?"
  Do NOT use for general Markdown linting or non-skill documentation.
license: Proprietary
metadata:
  author: hexaview-ai-team
  version: "1.0"
  skill-type: automation
---

# SKILL.md Linter

## When to use this skill
Activate when:
- A user creates or edits a SKILL.md file
- A user asks to validate, check, or review a SKILL.md
- A user asks "is my skill correct?" or "does my SKILL.md follow the spec?"
- You see a SKILL.md file with potential issues

Do NOT activate for general Markdown files, README files, or non-skill documentation.

## Validation workflow

Work through this checklist in order. Report all findings at the end.

### Phase 1: Frontmatter validation
1. Check that the file starts with `---` and has a closing `---`
2. Parse the YAML frontmatter between the markers
3. Validate **name** (required):
   - Present and non-empty
   - 1–64 characters
   - Lowercase letters, numbers, and hyphens only
   - No consecutive hyphens (`--`)
   - Cannot start or end with a hyphen
   - Must match the containing folder name
   - Regex: `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`
4. Validate **description** (required):
   - Present and non-empty
   - 1–1,024 characters
   - Should explain WHAT the skill does AND WHEN to use it
   - Warn if missing positive triggers ("Use when", "Activate when")
   - Warn if missing negative triggers ("Do NOT use for")
5. Validate **compatibility** (optional):
   - If present, must be ≤500 characters
6. Validate **metadata** (optional):
   - If present, should be a key-value mapping

### Phase 2: Body structure check
7. Check for recommended sections in the body (after frontmatter):
   - `## When to use this skill` — clarifies activation
   - A workflow/checklist section — numbered steps
   - `## Gotchas` — non-obvious facts
   - An output template or format section — concrete examples
8. Warn if body exceeds ~500 lines (recommend progressive disclosure)
9. Check for `references/` or `scripts/` pointers if body is long

### Phase 3: Description quality scoring
10. Score the description (max 7 points):
    - +2 if has positive triggers ("Use when", "Activate when", "Use for")
    - +2 if has negative triggers ("Do NOT", "Not for")
    - +1 if length is 50–500 characters
    - +1 if contains action verbs (extract, generate, deploy, review, etc.)
    - +1 if contains specific keywords (.pdf, API, Python, SQL, etc.)
11. Rate: 6-7 Excellent, 4-5 Good, 2-3 Needs work, 0-1 Poor

## Output format

ALWAYS use this exact structure for validation reports:

```
## SKILL.md Validation Report: [skill-name]

### Frontmatter
- [PASS/FAIL] name: [details]
- [PASS/FAIL] description: [details]
- [PASS/WARN/N/A] compatibility: [details]
- [PASS/N/A] metadata: [details]

### Body Structure
- [FOUND/MISSING] "When to use" section
- [FOUND/MISSING] Workflow/checklist section
- [FOUND/MISSING] Gotchas section
- [FOUND/MISSING] Output template

### Description Quality
Score: X/7 — [Rating]
[Feedback items]

### Summary
[VALID/INVALID] — [N] errors, [N] warnings
[List of actions to fix, if any]
```

## Gotchas
- The `name` field MUST match the folder name exactly — `my-skill/SKILL.md` must have `name: my-skill`
- A valid YAML frontmatter that is missing `name` or `description` is still INVALID per the spec
- Descriptions that only say what the skill does but not WHEN to use it will under-trigger — agents won't activate the skill
- Consecutive hyphens in names (`my--skill`) are invalid even though YAML accepts them
- The `---` markers must be on their own lines with no leading whitespace
