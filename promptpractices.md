# Copilot Prompt Practices & Usage Guide

This document explains how to effectively use GitHub Copilot with the enterprise QA automation setup inside this repository.

---

# Method 1 — Copy Command → Paste into Copilot Chat (Most Common)

This is the PRIMARY usage pattern.

## Example

From:

```txt
.github/commands/api-testing.md

Copy:

Generate negative test scenarios for login API.

Paste into:

Copilot Chat
Agent Chat
Inline Chat

Done.

Method 2 — Inline Commands (VERY POWERFUL)

This is how enterprise teams mostly use Copilot.

Step A — Open Existing File

Example:

test_login.py
Step B — Select Code

Highlight:

method
class
block
assertion
fixture
Step C — Open Inline Chat

Right click:

Copilot → Ask Copilot

OR press:

Ctrl + I

(Inline Chat)

Step D — Give Command

Example:

Add schema validation and negative scenarios using framework rules.

OR

Refactor using reusable fixtures and validators.

OR

Optimize assertions and logging.
Inline Command Examples
Example 1 — Improve Assertions

Select:

assert response.status_code == 200

Inline command:

Improve assertion quality using pytest best practices.
Example 2 — Add Negative Tests

Select whole class.

Inline command:

Generate negative and edge test scenarios for this API.
Example 3 — Refactor Duplicates

Select duplicated code.

Inline command:

Refactor into reusable helper methods.
Example 4 — Add Reporting

Select test file.

Inline command:

Add Allure steps and reporting annotations.
Example 5 — Add Retry Logic

Select flaky test.

Inline command:

Add retry handling and stabilization improvements.
Method 3 — Ask Copilot About Whole Repository

No file selection needed.

Open Copilot Chat and ask:

Analyze repository and identify missing enterprise API automation components.

This uses:

.github/instructions.md
.github/context/*
.github/agents/*
existing framework structure
Method 4 — Referencing BRD Requirements

Very useful for enterprise QA workflows.

Example
Generate API validation tests for BR-019 through BR-024.

OR

Generate RBAC validation scenarios for BR-041 to BR-045.
Method 5 — Generate New File

Create empty file:

test_rbac.py

Then ask:

Generate complete RBAC validation suite using framework rules.
Best Daily Workflow
Flow 1 — New Feature

Open Copilot Chat:

Generate login API tests using existing framework structure.
Flow 2 — Improve Existing File

Select code.

Press:

Ctrl + I

Ask:

Refactor using reusable fixtures and centralized validators.
Flow 3 — Review
Review this file against testing-rules.md and security-rules.md.
Flow 4 — Generate Edge Cases
Generate edge and boundary scenarios for this endpoint.
Flow 5 — Add Automation Features
Add request/response logging and Allure integration.
Important Best Practices
DO NOT:
paste giant BRDs every time
repeat framework rules every prompt
explain architecture repeatedly

Because:

.github/context/

already acts as persistent AI context.

Commands Folder Purpose
Old Style	New Style
remember prompts manually	reusable prompt registry
repeat same instructions	governed command library
ad-hoc prompting	enterprise workflows
Pro Tip — Add Example Usage in Command Files

Inside each command file:

## Example Usage

Example:

## Example Usage

Generate negative test scenarios for login API.

Generate schema validation for invoice API.

Generate auth guard tests for user profile endpoint.

This helps teams reuse prompts consistently.

Final Usage Pattern
Most Common Usage
Copy command → Paste into Copilot Chat

AND

Most Powerful Usage
Select code → Ctrl + I → Inline command

This combination is how enterprise Copilot engineering workflows typically operate.



.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip show python-dotenv
pytest --version