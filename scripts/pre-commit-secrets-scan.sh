#!/usr/bin/env bash
# ==============================================================
# Pre-commit hook: Scan for leaked API keys and secrets
# ==============================================================
# This script is installed as a git pre-commit hook.
# It blocks commits that contain potential API keys or secrets.
#
# Install:
#   cp scripts/pre-commit-secrets-scan.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Or run the setup script:
#   python scripts/setup_hooks.py
# ==============================================================

set -e

echo "Running secrets scan..."

# Get list of staged files (excluding deleted files)
STAGED_FILES=$(git diff --cached --name-only --diff-filter=d)

if [ -z "$STAGED_FILES" ]; then
    echo "No staged files to scan."
    exit 0
fi

FOUND_SECRETS=0

# --- Check 1: Block .env files from being committed ---
for file in $STAGED_FILES; do
    if echo "$file" | grep -qE '(^|/)\.env($|\.)'; then
        echo "BLOCKED: .env file staged for commit: $file"
        echo "  -> Remove it: git reset HEAD $file"
        FOUND_SECRETS=1
    fi
done

# --- Check 2: Scan staged file contents for API key patterns ---
PATTERNS=(
    'sk-[a-zA-Z0-9]{20,}'                    # OpenAI API keys
    'sk-proj-[a-zA-Z0-9_-]{20,}'             # OpenAI project keys
    'sk-ant-[a-zA-Z0-9_-]{20,}'              # Anthropic API keys
    'AKIA[0-9A-Z]{16}'                        # AWS Access Key IDs
    'ghp_[a-zA-Z0-9]{36}'                     # GitHub personal access tokens
    'gho_[a-zA-Z0-9]{36}'                     # GitHub OAuth tokens
    'xox[bpors]-[a-zA-Z0-9-]{10,}'           # Slack tokens
    'AIza[0-9A-Za-z_-]{35}'                   # Google API keys
    '-----BEGIN (RSA |EC |DSA )?PRIVATE KEY'  # Private keys
)

for file in $STAGED_FILES; do
    # Skip binary files and the patterns file itself
    if ! git diff --cached --diff-filter=d -- "$file" | head -1 > /dev/null 2>&1; then
        continue
    fi

    # Get the staged content of the file
    STAGED_CONTENT=$(git show ":$file" 2>/dev/null || true)
    if [ -z "$STAGED_CONTENT" ]; then
        continue
    fi

    for pattern in "${PATTERNS[@]}"; do
        MATCHES=$(echo "$STAGED_CONTENT" | grep -nE "$pattern" 2>/dev/null || true)
        if [ -n "$MATCHES" ]; then
            echo ""
            echo "BLOCKED: Potential secret found in $file"
            echo "  Pattern: $pattern"
            echo "  Matches:"
            echo "$MATCHES" | head -5 | while read -r line; do
                echo "    $line"
            done
            FOUND_SECRETS=1
        fi
    done
done

# --- Result ---
if [ $FOUND_SECRETS -ne 0 ]; then
    echo ""
    echo "============================================"
    echo "  COMMIT BLOCKED — Secrets detected!"
    echo "============================================"
    echo ""
    echo "  Fix options:"
    echo "  1. Remove the secret from the file"
    echo "  2. Use environment variables instead (see .env.example)"
    echo "  3. If this is a false positive, commit with: git commit --no-verify"
    echo ""
    exit 1
fi

echo "Secrets scan passed. No issues found."
exit 0
