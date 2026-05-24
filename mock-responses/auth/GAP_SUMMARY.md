# Swagger vs Existing Auth Mocks: Gap Summary

## Key Gaps Found in Previous Mocks

1. Envelope mismatch with Swagger:
- Prior mocks used primitive flat responses and often omitted required Swagger envelope fields.
- Swagger requires:
  - success=true responses: success, message{en,ar}, data
  - success=false responses: success, message{en,ar}, error{code,details,fields}

2. Missing endpoint coverage:
- Previous mocks only existed under login.
- Swagger/Postman flows include multiple additional auth endpoints (refresh, MFA verify, forgot-password flows, unlock, logout, UAE PASS paths).

3. Missing error taxonomy and metadata:
- Previous mocks lacked enterprise error code patterns and structured field-level errors.
- Previous mocks lacked timestamp, traceId, requestId.

4. Scenario coverage gaps:
- No explicit scenario partitioning for forbidden, validation failure, edge-case, or token lifecycle failures.

5. Contract drift vs Postman behaviors:
- Postman contains callback payload fields not defined in Swagger (for example emiratesId in UAE PASS callback POST example).
- Some Postman request examples include fields not present in strict Swagger required sets.

## Unsupported or Underspecified Scenarios in Swagger

1. Timeout responses (504):
- Useful for frontend resiliency and test coverage, but not explicitly documented for most auth endpoints in Swagger.

2. Detailed edge cases:
- Captcha replay, OTP rate-limiting, token reuse, anti-enumeration variants, and already-active unlock conflict are not explicitly modeled as dedicated schemas in Swagger.

3. Rich telemetry fields:
- statusCode/timestamp/traceId/requestId are not explicitly required in Swagger schemas but are commonly expected by frontend observability and enterprise logging.

4. Session metadata extensions:
- Additional session metadata objects (rotation state, session expiry context) are not explicitly part of Swagger but are frontend-useful and backward-compatible.

## Alignment Notes

- All success responses preserve Swagger-required fields and add deterministic metadata.
- All error responses preserve Swagger-required error schema fields and add deterministic metadata.
- No sensitive data is hardcoded; all values are synthetic and stable for TDD.
