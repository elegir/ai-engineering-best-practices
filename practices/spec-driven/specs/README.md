# specs/ — feature specifications

One file per feature or change: `specs/<feature-slug>.md`, written as user stories with acceptance criteria (template: the knowledge base's `templates/open-spec-user-story.md`). Specs are the input to `/plan-ticket` and the reference for `/develop-task` and the e2e tests.

Lifecycle (set in the file's frontmatter `status:`): `draft` → `approved` (Martin) → `implemented` (all criteria have passing tests) → `archived` (moved to `specs/archive/`, or merged into the permanent spec if using OpenSpec).

Rules: a story that needs "and" is two stories; every acceptance criterion names the test that proves it; clarifications from the ask-the-expert step are recorded in the spec, not lost in chat; the constitution (`constitution.md`) overrides any spec.
