(The file `c:\Users\Yogesh Bhagangare\Downloads\PythonProjectnew-20260520T124757Z-3-001\PythonProjectAI\mock_server\README.md` exists, but is empty)
# Mock Server

## Overview
The `mock_server` module provides a local mock API server for simulating backend authentication endpoints and responses. It is designed to support frontend and integration testing by mimicking real API behaviors, including various success and error scenarios, without requiring access to live backend services.

## Folder Structure

- `mock_server.py` — Main Flask app entry point. Registers all mock API routes and starts the server.
- `responses/` — Contains static JSON files for mock API responses (e.g., account locked, invalid password, etc.).
	- `auth/` — Auth-related response payloads.
- `routes/` — Contains Flask Blueprints for API endpoint definitions.
	- `auth_stub.py` — Implements `/api/auth/login` and related stubs.
- `utilities/` — Utility modules for the mock server.
	- `response_loader.py` — Loads JSON response files.

## Implemented API Stubs/Mocks

### 1. `POST /api/auth/login`
**Purpose:** Simulates user login with various authentication scenarios.

**Request:**
```json
{
	"email": "user@example.com",
	"password": "string",
	"captchaToken": "string"
}
```

**Responses:**
- **200 OK** (Valid credentials):
	- Returns a success message and MFA token.
- **401 Unauthorized** (Invalid password or email not found):
	- Returns error messages from `responses/auth/invalid_password.json` or `email_not_found.json`.
- **423 Locked** (Account locked):
	- Returns error from `responses/auth/account_locked.json`.
- **400 Bad Request** (Missing/invalid fields, unknown fields, invalid email format, SQL injection attempt):
	- Returns appropriate error message.

**Sample Response Payloads:**
- `login_success.json`:
	```json
	{
		"success": true,
		"message": { "en": "A verification code has been sent to your email" },
		"data": { "mfaRequired": true, "mfaSessionToken": "fake-mfa-session-token" }
	}
	```
- `invalid_password.json`:
	```json
	{
		"success": false,
		"message": { "en": "Invalid password" },
		"error": { "code": "AUTH_401_INVALID_PASSWORD" }
	}
	```
- `account_locked.json`:
	```json
	{
		"success": false,
		"message": { "en": "Account is temporarily locked due to multiple failed attempts" },
		"error": { "code": "AUTH_423_ACCOUNT_LOCKED" }
	}
	```

**Hardcoded/Mock Behaviors:**
- Only the email `kajal.gupta11@gmail.com` and password `Password@123dd4` are considered valid.
- Specific emails trigger special responses:
	- `locked@test.com` → Account locked
	- `notregistered_xyz@example.com` → Email not found
- Captcha token is required but not validated.
- SQL injection and unknown fields are rejected.

## Running the Mock Server Locally

1. **Install dependencies:**
	 Ensure your virtual environment is active and run:
	 ```sh
	 pip install -r requirements.txt
	 ```
2. **Start the server:**
	 ```sh
	 python mock_server/mock_server.py
	 ```
	 The server will run on `http://0.0.0.0:3001` by default.

## Configuration
- **Port:** Default is `3001` (see `mock_server.py`).
- **Environment Variables:**
	- None required for basic operation.
	- Set `API_MODE=mock` for integration with some test scripts.
- **Mock Data Sources:**
	- All responses are loaded from JSON files in `mock_server/responses/auth/`.

## Known Limitations & Pending Work
- Only `/api/auth/login` is implemented. Other endpoints are pending.
- No support for dynamic user creation or password changes.
- No persistent state; all responses are stateless and based on hardcoded logic.
- No authentication/authorization for the mock server itself.

## QA & Extension Notes
- To add new mock APIs:
	1. Create a new Blueprint in `routes/` and register it in `mock_server.py`.
	2. Add corresponding response JSON files in `responses/`.
	3. Follow the structure and error handling patterns in `auth_stub.py`.
- For new error scenarios, add new JSON files and update the stub logic.
- Keep mock behaviors simple and deterministic for reliable testing.
