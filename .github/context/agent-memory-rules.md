# Agent Memory Rules

The AI agent must persist the following framework knowledge across all tasks.

## Persistent Architecture Knowledge
- Framework uses pytest + requests.
- Environment-driven configuration via .env.
- Reporting via Allure + HTML reports.
- Shared fixtures via conftest.py.
- Modular reusable utilities.
- API-first automation strategy.

## Persistent Testing Standards
Always include:
- positive tests
- negative tests
- edge cases
- boundary validations
- auth validation
- schema validation

## Persistent Security Rules
Never:
- hardcode credentials
- expose tokens
- log secrets
- bypass auth validation

## Persistent API Rules
Every API test must validate:
- status code
- schema
- response fields
- response time
- auth behavior

## Persistent Framework Rules
Reuse:
- fixtures
- helpers
- request builders
- response validators

Avoid:
- duplicate utilities
- duplicated payloads
- inline configs

## Persistent Reporting Rules
Every automation implementation should support:
- Allure
- HTML reporting
- request/response logging

## Persistent AI Behavior
The AI must:
- analyze existing implementation first
- generate delta changes only
- avoid unnecessary rewrites
- preserve architecture consistency
- preserve naming consistency

## Persistent Review Rules
Before generating output:
- validate imports
- validate fixture reuse
- validate assertions
- validate markers
- validate environment usage