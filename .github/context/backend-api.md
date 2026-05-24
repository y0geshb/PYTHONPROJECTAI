# Backend API Standards

## API Structure
- Use versioned APIs:
  /api/v1/

## Authentication
- Use Bearer token authentication
- Never hardcode tokens
- Load credentials from .env

## Request Rules
- Validate headers
- Validate content-type
- Validate authorization

## Response Rules
Responses must validate:
- status code
- schema
- required fields
- response time

## Error Response Format
Expected:
{
  "success": false,
  "message": "error message",
  "errors": []
}

## API Test Design
Each endpoint should include:
- happy path
- unauthorized test
- invalid payload test
- missing field test
- edge cases

## Performance Expectations
- API response < 3000ms

## Logging
Log:
- request URL
- payload
- response body
- response time