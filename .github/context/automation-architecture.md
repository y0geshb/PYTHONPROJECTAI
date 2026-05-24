# Automation Architecture Rules

## Framework Layers
- tests
- fixtures
- api clients
- request builders
- validators
- utilities
- reporting
- config

## Design Principles
- reusable
- modular
- scalable
- maintainable

## API Layer
All APIs must use:
- centralized client
- reusable request methods
- reusable auth handlers

## Validation Layer
Centralize:
- schema validation
- response validation
- status validation

## Reporting Layer
Support:
- Allure
- HTML reports
- request/response logs

## Logging
Log:
- endpoint
- payload
- response
- response time

Never log:
- passwords
- secrets
- tokens