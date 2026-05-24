# Token Optimization Rules

Primary Goal:
Minimize prompt and response token usage while preserving accuracy.

Rules:
- Generate delta changes only.
- Never regenerate unchanged code.
- Analyze existing implementation first.
- Modify only impacted sections.
- Reuse existing utilities and fixtures.
- Avoid repeating explanations.
- Prefer concise outputs.
- Use modular generation.
- Reuse existing patterns.
- Avoid duplicate test creation.
- Keep responses structured and compact.

Generation Strategy:
1. Inspect existing implementation
2. Identify impacted modules
3. Generate minimal changes
4. Avoid unnecessary refactors

Code Rules:
- Reuse imports
- Reuse helpers
- Avoid verbose comments
- Avoid generating boilerplate repeatedly