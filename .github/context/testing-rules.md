# Testing Rules

## Coverage Gate
- Minimum coverage: 90%
- No skipped tests

## Required Test Types
- Positive scenarios
- Negative scenarios
- Edge cases
- Boundary validations
- Unauthorized scenarios
- Invalid payload validation

## API Validation Rules
Validate:
- status codes
- response schema
- response body
- headers
- response time
- error structure

## Mandatory Assertions
Every test must validate:
- status code
- key response fields
- response structure
- API behavior

## Error Validation
Validate:
- invalid token
- expired token
- missing fields
- invalid request body
- malformed JSON
- unsupported methods

## Reporting
All tests must support:
- HTML reports
- Allure reports
- readable assertion messages

## Test Design
- Use AAA pattern
- Avoid duplicated code
- Use fixtures
- Use parametrization where possible