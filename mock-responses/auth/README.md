# Auth Mock Responses

Contract-aligned auth mocks are organized by endpoint path and scenario:

- mock-responses/auth/login/<scenario>.json
- mock-responses/auth/login/mfa/verify/<scenario>.json
- mock-responses/auth/refresh/<scenario>.json
- mock-responses/auth/uae-pass/start/<scenario>.json
- mock-responses/auth/uae-pass/callback/<scenario>.json
- mock-responses/auth/uae-pass/logout/<scenario>.json
- mock-responses/auth/password/forgot-email/<scenario>.json
- mock-responses/auth/password/forgot-otp/initiate/<scenario>.json
- mock-responses/auth/password/forgot-otp/verify/<scenario>.json
- mock-responses/auth/password/reset/<scenario>.json
- mock-responses/auth/account/unlock/<scenario>.json
- mock-responses/auth/logout/<scenario>.json

All payloads are deterministic and include:
- success envelope fields required by Swagger
- localized message fields (en, ar)
- statusCode
- timestamp
- traceId and requestId
- realistic auth/session structures when applicable
