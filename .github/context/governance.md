Act as an Enterprise QA Automation Architect.

Project Context:

* Python pytest API automation framework
* Contract-driven testing architecture
* Prism mock server for TDD
* Swagger/OpenAPI is the source of truth
* Existing Postman collection already available
* Existing generic mock stubs already available
* GitHub Copilot Agent mode enabled with .github governance context

Repository Inputs:

1. Swagger Contract:
   resources/swagger/swagger.json

2. Existing Postman Collection:
   resources/collections/SERH.postman_collection_newly.json

3. Existing Generic Stubs:
   mock-responses/

Objective:
Build a fully contract-driven mock and TDD validation setup.

Tasks:

1. Analyze swagger.json completely.

2. Compare Swagger endpoints against Postman collection.

3. Identify:

   * missing endpoints
   * missing request schemas
   * missing response schemas
   * missing status codes
   * missing negative scenarios
   * missing auth validations
   * mismatched payloads
   * hardcoded values
   * contract inconsistencies

4. Generate/Update Prism-compatible mock responses for:

   * success scenarios
   * validation failures
   * unauthorized access
   * forbidden access
   * invalid payloads
   * edge cases
   * server failures

5. Create reusable mock response files under:
   mock-responses/<module>/

6. Ensure all mocks strictly follow Swagger schemas.

7. Refactor Postman collection:

   * remove hardcoded URLs
   * remove hardcoded credentials
   * add environment variables
   * add token chaining
   * add response assertions
   * add schema validation tests
   * add negative scenarios
   * add auth guard scenarios

8. Generate/update pytest contract validation tests:

   * positive tests
   * negative tests
   * schema validation tests
   * edge cases
   * auth validation
   * response contract assertions

9. Ensure pytest tests support:
   ENV=mock
   ENV=qa
   ENV=staging

10. Validate all generated tests against Prism mock server.

11. Generate reusable validators/helpers for:

* schema validation
* status validation
* error contract validation
* token validation

12. Add centralized test data handling.

13. Ensure:

* no hardcoded URLs
* no hardcoded tokens
* no duplicated payloads
* reusable fixtures only
* enterprise pytest practices
* Allure-ready logging

14. Follow all repository governance rules from:
    .github/instructions.md
    .github/context/
    .github/agents/
    .github/skills/

15. Preserve existing framework structure.

16. Use delta updates only.

17. Do not regenerate unchanged files.

Expected Deliverables:

* Updated Prism-compatible mock structure
* Updated Postman collection
* Environment files
* Contract validation tests
* Reusable validators
* Missing schema coverage
* Negative scenario coverage
* TDD-ready mock execution setup
* Gap analysis summary
* Contract mismatch report

Execution Goal:
Enable complete contract-first API testing using:
Swagger → Prism → Postman → Pytest → Allure

All generated outputs must be execution-ready.
