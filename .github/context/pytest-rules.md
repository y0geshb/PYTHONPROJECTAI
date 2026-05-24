# Pytest Rules

## Use Markers
Required markers:
- smoke
- regression
- positive
- negative

## Use Parametrization
Prefer:
@pytest.mark.parametrize

## Assertions
Use explicit assertions.

Bad:
assert response.status_code == 200

Good:
assert response.status_code == 200, "Expected 200 OK"

## Fixtures
Prefer fixture reuse over duplicate setup.

## Test Independence
Tests must be isolated and runnable independently.