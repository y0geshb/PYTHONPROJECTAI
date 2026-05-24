# API Test Automation Framework

## Project Description
This is a Python-based REST API test automation framework built with pytest and requests.
It uses environment-based configuration, reusable fixtures, and modular test folders.

## Recent Updates (May 22, 2026)

### 1. Auth mock response refactor (contract-aligned)
- Refactored auth mocks to endpoint/scenario structure under `mock-responses/auth/...`.
- Replaced primitive/generic login mock payloads with realistic Swagger/Postman-aligned payloads.
- Added scenario-based responses across auth flows:
	- success
	- validation failure
	- unauthorized
	- forbidden
	- invalid payload
	- timeout
	- server failure
	- edge cases
- Added requested auth flow scenarios:
	- token expiration
	- invalid refresh token
	- locked account
	- invalid OTP
	- expired OTP
	- invalid reset token
- Added deterministic metadata in mocks for demo/TDD use:
	- `statusCode`
	- `timestamp`
	- `traceId`
	- `requestId`

### 2. New deterministic phase-1 traditional stub server
- Added Flask-based stub server for one endpoint only:
	- `POST /api/auth/login`
- Implemented in:
	- `mock_server/server.py`
- Stub source file:
	- `mock_server/stubs/auth/login/success_200.json`
- Behavior:
	- Returns HTTP 200 using file-based stub payload.
	- Validates request body fields `email` and `password`.
	- Returns HTTP 400 with realistic validation response when required fields are missing.

### 3. Added dedicated login stub test
- Added test file:
	- `tests/test_login_stub.py`
- Validates:
	- HTTP status code
	- success flag
	- message localization structure
	- MFA structure (`mfaRequired`, `mfaSessionToken`)
	- trace/request identifiers
	- 400 validation response for missing required fields

### 4. Source of contract alignment
- `resources/swagger/swagger.json`
- `resources/collections/SERH.postman_collection_newly.json`
- `resources/collections/auth.postman_collection.json`

### 5. Validation status
- New login stub implementation and tests verified locally:
	- `pytest tests/test_login_stub.py -v` -> passed.

## Setup Instructions
1. Clone and enter the project: `git clone https://github.com/y0geshb/PYTHONPROJECTAI.git` then `cd PythonProjectAI`
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment (Windows): `venv\Scripts\Activate.ps1`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and update values for your environment

## Configuration
Create a `.env` file in the project root based on `.env.example`:
```
API_BASE_URL=https://your-api-base-url.com
API_LOGIN_ENDPOINT=/api/v1/auth/login
API_USER_EMAIL=your-test-email@example.com
API_USER_PASSWORD=your-test-password
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin-password
```

## Running with Mock Server

### 1. Start the mock server
```powershell
python mock_server/mock_server.py
# Starts on http://127.0.0.1:3010 by default
# Optional: --host 0.0.0.0 --port 5000
```

### 2. Run tests against mock
```powershell
$env:API_MODE="mock"   # PowerShell
pytest tests/ -v
pytest tests/auth/test_serh_login.py
python -m pytest tests/auth/test_serh_login.py
```
> Config is auto-loaded from `config/.env.mocks` when `API_MODE=mock`.

---

## Running with Actual Endpoints

Set your target environment in `.env` or via shell variable:
```powershell
$env:ENV="qa"          # loads config/.env.qa
pytest tests/ -v
```
> Make sure `config/.env.qa` (or `.env.<env>`) has the correct `API_BASE_URL` and credentials.

---

## How to Run Tests

| What | Command |
|------|---------|
| All tests | `pytest tests/ -v` |
| Smoke | `pytest tests/smoke/ -v -m smoke` |
| Regression | `pytest tests/ -v -m regression` |
| Positive | `pytest tests/ -v -m positive` |
| Negative | `pytest tests/ -v -m negative` |

## How to Generate Reports

### HTML report
```powershell
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Allure report
```powershell
pytest tests/ -v --alluredir=allure-results
allure serve allure-results
```
