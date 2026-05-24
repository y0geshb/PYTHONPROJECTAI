# Test Data Rules

## Principles
- Tests must be independent.
- Tests must not depend on execution order.
- Avoid shared mutable data.

## Data Generation
Use:
- unique identifiers
- timestamp-based data
- factory utilities

## Cleanup
Tests creating data must:
- cleanup after execution
- use teardown fixtures

## Sensitive Data
Never:
- hardcode credentials
- expose PII
- expose tokens

## Environment Isolation
Separate:
- QA
- staging
- production

## Reusability
Use:
- centralized testdata.json
- environment configs