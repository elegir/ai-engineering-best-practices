# Hurl: plain-text HTTP tests, deterministic, CLI-friendly. https://hurl.dev
# Install: winget install hurl  |  brew install hurl  |  cargo install hurl
# Run:     hurl --test --variable base=http://localhost:<<3000>> tests/api/smoke.hurl

# 1. Health
GET {{base}}/<<health>>
HTTP 200

# 2. Auth: login returns a token
POST {{base}}/<<api/auth/login>>
Content-Type: application/json
{
  "email": "<<seed-user@example.com>>",
  "password": "<<seed-password>>"
}
HTTP 200
[Captures]
token: jsonpath "$.token"
[Asserts]
jsonpath "$.token" exists

# 3. Core resource: create
POST {{base}}/<<api/items>>
Authorization: Bearer {{token}}
Content-Type: application/json
{ "name": "Smoke item" }
HTTP 201
[Captures]
item_id: jsonpath "$.id"
[Asserts]
jsonpath "$.name" == "Smoke item"

# 4. Core resource: read back
GET {{base}}/<<api/items>>/{{item_id}}
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$.id" == "{{item_id}}"

# 5. Validation: bad input is rejected with the standard error envelope
POST {{base}}/<<api/items>>
Authorization: Bearer {{token}}
Content-Type: application/json
{ "name": "" }
HTTP 400
[Asserts]
jsonpath "$.error.code" exists
jsonpath "$.error.message" exists

# 6. Auth: unauthenticated is refused
GET {{base}}/<<api/items>>
HTTP 401
