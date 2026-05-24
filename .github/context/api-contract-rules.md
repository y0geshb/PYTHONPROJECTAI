# API Contract Validation Rules

Every API automation test must validate:

## Request Validation
- required headers
- content-type
- auth token
- payload schema

## Response Validation
- status code
- schema
- required fields
- field types
- enums
- nullability
- nested objects

## Error Validation
Validate:
- 400
- 401
- 403
- 404
- 409
- 422
- 500

## Contract Stability
Validate:
- no unexpected fields removed
- response compatibility maintained
- backward compatibility preserved

## Integration Validation
Validate:
- SAP integrations
- ADP APIs
- UAE Pass APIs
- CICPA integrations
- notification APIs

## Performance Validation
Validate:
- SLA compliance
- response thresholds
- timeout handling