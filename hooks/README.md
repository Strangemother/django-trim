# Git Hooks

This directory contains useful git hooks for the django-trim project.

## Available Hooks

### pre-push
Ensures Black formatting compliance before pushing to remote.

**Features:**
- Automatically checks if code needs Black formatting
- Offers interactive options:
  1. Auto-format and continue push (uncommitted changes)
  2. Auto-format and abort (recommended - review changes first)
  3. Abort without formatting
- Preserves existing Git LFS hooks

**Installation:**
```bash
./hooks/install.sh
```

Or manually:
```bash
cp hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

## Usage

Once installed, the hook runs automatically on `git push`. If formatting issues are detected:

```
Running Black formatting check...

⚠️  Some files need Black formatting!

Do you want to:
  1) Auto-format and continue push (you'll need to commit again)
  2) Auto-format and abort push (recommended - lets you review changes)
  3) Abort push without formatting

Choice (1/2/3):
```

**Recommendation:** Choose option 2, review the changes, commit them, then push again.

## Bypass Hook

If you need to bypass the hook (not recommended):
```bash
git push --no-verify
```
