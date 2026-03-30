#!/usr/bin/env python3
"""
Grade a student's Jupyter notebook submission.

Checks each exercise cell for completion status by looking for:
- TODO markers and NotImplementedError (not completed)
- Actual code implementation (completed or partial)

Usage:
    python grade_notebook.py <notebook_path>
    python grade_notebook.py <notebook_path> --threshold 80
    python grade_notebook.py notebooks/01_MCP_Practice.ipynb --threshold 80

Exit codes:
    0 — pass (completion_rate >= threshold, or no threshold set)
    1 — fail (completion_rate < threshold, or file not found)

Output:
    Human-readable report to stderr, JSON report to stdout.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def extract_exercises(notebook_path: str) -> list[dict]:
    """Parse a notebook and extract exercise information."""
    with open(notebook_path) as f:
        nb = json.load(f)

    exercises = []
    cells = nb.get("cells", [])

    for i, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue

        source = "".join(cell.get("source", []))

        # Look for exercise markers
        match = re.search(r"#\s*EXERCISE\s+(\w+[a-z]?):?\s*(.*)", source, re.IGNORECASE)
        if not match:
            continue

        exercise_id = match.group(1).strip()
        exercise_title = match.group(2).strip() or f"Exercise {exercise_id}"

        # Determine completion status
        has_todo = "# TODO" in source
        has_not_implemented = "NotImplementedError" in source
        has_blank_answer = '= "___"' in source

        # Count non-skeleton lines (not comments, not blank, not imports)
        code_lines = []
        for line in source.split("\n"):
            stripped = line.strip()
            if (stripped
                and not stripped.startswith("#")
                and not stripped.startswith("raise NotImplementedError")
                and "= \"___\"" not in stripped
                and stripped != "pass"):
                code_lines.append(stripped)

        if has_not_implemented or has_blank_answer:
            status = "TODO"
        elif has_todo and len(code_lines) > 3:
            status = "PARTIAL"
        elif has_todo:
            status = "TODO"
        else:
            status = "DONE"

        exercises.append({
            "cell_index": i,
            "exercise_id": exercise_id,
            "title": exercise_title,
            "status": status,
            "has_todo": has_todo,
            "has_not_implemented": has_not_implemented,
            "code_lines": len(code_lines),
        })

    return exercises


def grade_notebook(notebook_path: str) -> dict:
    """Grade a notebook and return a report."""
    path = Path(notebook_path)
    if not path.exists():
        return {"error": f"File not found: {notebook_path}"}

    exercises = extract_exercises(notebook_path)

    done = sum(1 for e in exercises if e["status"] == "DONE")
    partial = sum(1 for e in exercises if e["status"] == "PARTIAL")
    todo = sum(1 for e in exercises if e["status"] == "TODO")
    total = len(exercises)

    return {
        "notebook": str(path.name),
        "path": str(path),
        "total_exercises": total,
        "completed": done,
        "partial": partial,
        "not_started": todo,
        "completion_rate": round(done / total * 100, 1) if total > 0 else 0,
        "exercises": exercises,
    }


def main():
    parser = argparse.ArgumentParser(description="Grade a student notebook submission.")
    parser.add_argument("notebook", help="Path to the .ipynb notebook file")
    parser.add_argument(
        "--threshold", type=float, default=0,
        help="Minimum completion %% to pass (0-100). Exit code 1 if below. Default: 0 (always pass)"
    )
    args = parser.parse_args()

    report = grade_notebook(args.notebook)

    if "error" in report:
        print(f"ERROR: {report['error']}", file=sys.stderr)
        sys.exit(1)

    # Print human-readable summary to stderr
    print(f"\nGrading Report: {report['notebook']}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    for ex in report["exercises"]:
        icon = {"DONE": "[x]", "PARTIAL": "[~]", "TODO": "[ ]"}[ex["status"]]
        print(f"  {icon} Exercise {ex['exercise_id']}: {ex['title']} — {ex['status']}", file=sys.stderr)

    rate = report["completion_rate"]
    threshold = args.threshold
    print(f"\nCompleted: {report['completed']}/{report['total_exercises']} ({rate}%)", file=sys.stderr)

    if threshold > 0:
        passed = rate >= threshold
        status = "PASS" if passed else "FAIL"
        print(f"Threshold: {threshold}%  — {status}", file=sys.stderr)
    else:
        passed = True

    # Print JSON to stdout (for programmatic use)
    report["threshold"] = threshold
    report["passed"] = passed
    print(json.dumps(report, indent=2))

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
