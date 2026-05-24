# Framework Rules

## Architecture
- Modular folder structure
- Shared fixtures
- Shared utilities
- Environment-driven configuration

## Fixtures
- Keep fixtures reusable
- Avoid duplicate setup logic

## Naming Conventions
Tests:
test_<feature>_<scenario>

Files:
test_<module>.py

Fixtures:
<feature>_fixture

## Environment
Use:
- .env
- dotenv
- pytest.ini

## Reports
Support:
- HTML reports
- Allure reports