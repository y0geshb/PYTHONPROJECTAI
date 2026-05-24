# Security Guide

## Overview
This document explains security practices for this project and how to clean up any secrets accidentally committed to git history.

---

## Environment Variables
All secrets must be stored in a local `.env` file and **never committed to git**.

- `.env` is listed in `.gitignore` and will not be tracked.
- Use `.env.example` as the template. Copy it to `.env` and fill in real values:
  ```sh
  copy .env.example .env
  ```

---

## Secrets Managed via Environment Variables

| Variable | Purpose |
|----------|---------|
| `API_USER_EMAIL` | QA test user email |
| `API_USER_PASSWORD` | QA test user password |
| `SERH_CAPTCHA_TOKEN` | Captcha token for live tests |
| `SERH_REFRESH_TOKEN` | Refresh token for token tests |
| `SERH_FORGOT_OTP_SESSION_TOKEN` | OTP session token |
| `SERH_RESET_TOKEN` | Password reset token |
| `SERH_UNLOCK_TOKEN` | Account unlock token |
| `MOCK_VALID_EMAIL` | Mock server valid email |
| `MOCK_VALID_PASSWORD` | Mock server valid password |

---

## Removing Secrets from Git History

If a secret was accidentally committed, follow these steps to permanently remove it.

### Option 1: Using `git filter-repo` (Recommended)

1. **Install git-filter-repo:**
   ```sh
   pip install git-filter-repo
   ```

2. **Remove a specific file from history:**
   ```sh
   git filter-repo --path .env --invert-paths
   ```

3. **Replace a secret string everywhere in history:**
   ```sh
   git filter-repo --replace-text <(echo "old-secret==>REMOVED")
   ```
   On Windows PowerShell:
   ```powershell
   "old-secret==>REMOVED" | Out-File replacements.txt -Encoding utf8
   git filter-repo --replace-text replacements.txt
   ```

4. **Force-push the cleaned history:**
   ```sh
   git push origin main --force
   ```

5. **Notify collaborators** to re-clone the repository.

### Option 2: Using BFG Repo Cleaner

1. **Download BFG:** https://rtyley.github.io/bfg-repo-cleaner/

2. **Remove a file from history:**
   ```sh
   java -jar bfg.jar --delete-files .env
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push origin main --force
   ```

---

## Security Best Practices

- Never hardcode passwords, tokens, API keys, or emails in source files.
- Never log received passwords (logs may be stored and readable).
- Rotate any credential that was ever exposed in git history.
- Limit `.env` file permissions to the current user where possible.
- Use `SERH_ENABLE_LIVE_POSITIVE=false` (default) to prevent live credential use in CI.
- Periodically audit your repository with tools like `truffleHog` or `git-secrets`.

---

## Auditing for Secrets

Run the following to check for any remaining secrets in the codebase:
```sh
# Search for common secret patterns
grep -rn "password\s*=\s*['\"]" --include="*.py" .
grep -rn "api_key\s*=\s*['\"]" --include="*.py" .
grep -rn "@kellton.com\|@gmail.com" --include="*.py" .
```

---

## Reporting a Security Issue
If you find a security vulnerability, do not open a public issue. Contact the repository owner directly.
