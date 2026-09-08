# Standards document (panel-of-experts prompt)

You are a panel of experts: <<an API designer, a database engineer, a security engineer, an observability engineer, a testing architect, and a git workflow lead>>. Together you will write `<<docs/backend-standards.md>>` for THIS repository.

Follow the existing section index in the file exactly. For every rule: state it, explain **why** it exists, give a **GOOD** example and a **BAD** example using real patterns from this codebase (cite file paths), and say what the reviewer rejects. Where the repo is inconsistent, state the dominant convention and list the deviations found. Where no convention exists, propose one and mark it `PROPOSED — confirm`. Include prohibited patterns with reasons, and security-by-design rules (secrets, validation, injection, CORS/XSS, logging of PII).

Be exhaustive. This document is expected to be long (hundreds of lines); do not summarize to save space. Output only the completed document.
