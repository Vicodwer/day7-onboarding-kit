# Part C — Interview Ready

## Q1: What is a Virtual Environment?

A Python virtual environment is an isolated folder containing its own 
Python interpreter and packages, separate from all other projects. 
Developers use them because different projects need different package 
versions — Project A might need numpy 1.24 while Project B needs numpy 2.0. 
Without a venv, installing one breaks the other. 
Think of it like a separate toolbox for each job — a plumber and 
electrician both own a wrench but don't share tools.

---

## Q2: The 5 Issues in the Broken Code

| # | Issue | Fix |
|---|-------|-----|
| 1 | import os, sys, json — multiple imports on one line | Separate into import sys only |
| 2 | def checkVersion() — camelCase name | Rename to check_version() |
| 3 | v.minor>=11 — missing spaces around operator | v.minor >= 11 |
| 4 | temp = 42 — unused variable | Remove it |
| 5 | print( "Version status:" , result ) — spaces inside parentheses | print("Version status:", result) |

### Fixed Code:
import sys

def check_version():
    """Check if Python version is 3.11 or higher."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        return "Good"
    return "Bad"

result = check_version()
print("Version status:", result)

---

## Q3: ModuleNotFoundError — 3 Causes

**Cause 1:** Wrong venv active — numpy installed in different environment
- Diagnostic: `where.exe python`

**Cause 2:** Installed with wrong pip version
- Diagnostic: `pip show numpy`

**Cause 3:** Installation silently failed
- Diagnostic: `pip list | findstr numpy`