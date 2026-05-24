# Python API Test Automation Framework

## Project Overview
This project is a Python-based REST API test automation framework using pytest and requests. It supports environment-based configuration, reusable fixtures, modular test folders, and a mock server for contract-aligned testing. It is designed for easy onboarding and robust QA automation.

---

## Prerequisites
- Python 3.8+
- Git (for version control and GitHub integration)
- pip
- Optional: Allure for advanced reporting

---

## How to Clone/Download the Project
```sh
git clone https://github.com/y0geshb/PYTHONPROJECTAI.git
cd PythonProjectAI
```

---

## Setup And Running Locally
1. Create a virtual environment:
   ```sh
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - Windows:
     ```sh
     .venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Copy and configure environment variables:
   ```sh
   copy .env.example .env
   ```
   Then edit `.env` with your API endpoints and credentials.

---

## Environment Variables
Edit `.env` in the project root. Example:
```env
API_BASE_URL=https://your-api-base-url.com
API_LOGIN_ENDPOINT=/api/v1/auth/login
API_USER_EMAIL=your-test-email@example.com
API_USER_PASSWORD=your-test-password
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin-password
```

---

## Starting the Mock Server
```sh
python mock_server/mock_server.py
```
Default URL: `http://127.0.0.1:3001`

---

## Running Tests
### Against Mock Server
```powershell
$env:API_MODE="mock"
pytest tests/ -v
pytest tests/auth/test_serh_login.py
```

### Against Real Endpoints
```powershell
$env:ENV="qa"
pytest tests/ -v
```

### Test Selection Examples
| What | Command |
|------|---------|
| All tests | pytest tests/ -v |
| Smoke | pytest tests/smoke/ -v -m smoke |
| Regression | pytest tests/ -v -m regression |
| Positive | pytest tests/ -v -m positive |
| Negative | pytest tests/ -v -m negative |

---

## Generating Reports
### HTML Report
```sh
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Allure Report
```sh
pytest tests/ -v --alluredir=allure-results
allure serve allure-results
```

---

## GitHub Setup And Push Automation
This project includes a utility script to automate uploading to GitHub.

### Script: `setup_github.py`
It automates:
- Git initialization
- `.gitignore` creation if missing
- Commit of all files
- Remote GitHub repository connection
- Push to a configurable branch

### Usage Example
```sh
python setup_github.py --repo-url https://github.com/y0geshb/PYTHONPROJECTAI.git --branch main --message "Initial commit" --git-user-name "y0geshb" --git-user-email "yogesh.bhaganagare@kellton.com"
```

### Using Environment Variables
```powershell
$env:GITHUB_REPO_URL="https://github.com/y0geshb/PYTHONPROJECTAI.git"
$env:GIT_BRANCH="main"
$env:GIT_COMMIT_MSG="Initial commit"
$env:GIT_USER_NAME="y0geshb"
$env:GIT_USER_EMAIL="yogesh.bhaganagare@kellton.com"
python setup_github.py
```

### Error Handling Included
- Missing git installation
- Authentication failures
- Invalid repository URL
- Push and permission issues
- Logs for each major action

---

## Folder Structure Overview
```text
├── .env / .env.example         # Environment configs
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── setup_github.py             # GitHub automation script
├── mock_server/                # Flask mock server
├── tests/                      # All test modules
│   └── auth/                   # Auth-related tests
├── test_data/                  # Test payloads and data
├── reports/                    # Test and coverage reports
├── config/                     # Config loaders and HTTP client
├── resources/                  # Postman/Swagger collections
├── handlers/, contracts/, ...  # App logic modules
```

---

## Troubleshooting
- Git not found: Install Git and ensure it is available in PATH.
- Dependency errors: Re-run `pip install -r requirements.txt` in the active virtual environment.
- `.env` issues: Ensure `.env` exists and contains valid values.
- Mock server not starting: Check for port conflicts or Python errors in `mock_server/mock_server.py`.
- Test failures: Review pytest output, verify API endpoints, and confirm credentials.
- GitHub push/auth errors: Ensure you have repository access and are authenticated.

---

## Example Commands
```sh
# Clone the repo
git clone https://github.com/y0geshb/PYTHONPROJECTAI.git
cd PythonProjectAI

# Setup environment
python -m venv .venv
pip install -r requirements.txt

# Run mock server
python mock_server/mock_server.py

# Run all tests
pytest tests/ -v

# Run a specific test
pytest tests/auth/test_serh_login.py

# Generate HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html

# Automate GitHub push
python setup_github.py --repo-url https://github.com/y0geshb/PYTHONPROJECTAI.git --branch main --message "Initial project commit" --git-user-name "y0geshb" --git-user-email "yogesh.bhaganagare@kellton.com"
```

---

## Need Help?
If you get stuck, check the troubleshooting section above or contact the project maintainer.
