# QA Automation Framework Instructions

You are working inside a Python REST API automation framework.

Framework Stack:
- Python
- pytest
- requests
- Allure reporting
- HTML reporting
- dotenv configuration
- reusable fixtures
- modular test architecture

Primary Goals:
1. Generate production-grade API automation tests.
2. Follow existing framework structure.
3. Reuse utilities and fixtures.
4. Avoid duplicate implementations.
5. Maintain high readability and maintainability.
6. Generate minimal delta changes only.
7. Validate API contracts and responses.
8. Follow pytest best practices.

Mandatory Rules:
- Never hardcode secrets or tokens.
- Always use environment variables.
- Reuse fixtures from conftest.py.
- Use helper utilities before creating new code.
- Generate modular tests.
- Maintain marker consistency:
  - smoke
  - regression
  - positive
  - negative
- Follow AAA pattern:
  Arrange
  Act
  Assert

Validation Requirements:
- Validate status code
- Validate response schema
- Validate response time
- Validate error responses
- Validate edge cases
- Validate security scenarios

Output Expectations:
- Explain important implementation decisions.
- Generate concise code.
- Avoid unnecessary refactors.
- Maintain token efficiency.

Required Shared References:
- .github/context/testing-rules.md
- .github/context/backend-api.md
- .github/context/security-rules.md
- .github/context/framework-rules.md
- .github/context/pytest-rules.md
- .github/context/token-optimization-rules.md