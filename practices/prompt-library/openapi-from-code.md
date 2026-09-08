# OpenAPI spec from code

You are an expert in API documentation with OpenAPI 3.1.

Objective: produce `docs/api-spec.yml` describing every HTTP route in this repository. Read the route definitions and handlers (`<<src/routes/**>>`) and the validation schemas (`<<src/schemas/**>>`).

It must contain: info and servers; every path and method; parameters; request bodies with schemas derived from the validation code; responses for success and for each error using the envelope defined in `docs/backend-standards.md` §4; security schemes and which routes require them; tags by domain; examples for the core resources.

Rules: valid OpenAPI 3.1 YAML (`components/schemas` for reuse); do not invent routes; mark anything ambiguous with `x-todo:`; save to `docs/api-spec.yml`.

If the framework can generate this automatically (e.g. from decorators), tell me the command and set that up instead of hand-writing the file — a generated spec never goes stale.
