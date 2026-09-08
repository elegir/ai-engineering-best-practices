---
title: "Open spec — <feature name>"
type: template
status: current
date: YYYY-MM-DD
tags: [spec, user-story]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Open spec — <Feature name>

> **How to use.** Copy this into the target repo (e.g. `specs/<feature>.md` or the OpenSpec change folder). One story per behavior. Keep stories atomic: if a story needs "and", split it. Acceptance criteria must be testable by a machine where possible — they become the e2e tests. The workshop's homework used this format for **SSO**, starting with *sign-up* and *login*; those two are given as worked examples below.

## Purpose
One paragraph: the user problem, why now, what is out of scope.

## Clarifications resolved
Answers to the "ask the expert" questions (`principles/04-spec-driven-development.md`). Keep them here so the reasoning is not lost.

## Stories

### US-1 — <short name>
**As a** <role>, **I want** <capability>, **so that** <benefit>.

Acceptance criteria:
- Given <state>, when <action>, then <observable result>.
- Given …, when …, then ….

Non-functional: <performance, security, accessibility, logging requirements if any>.
Out of scope: <explicit exclusions>.
Verification: <which test file / e2e path proves this>.

### US-2 — …

## Worked examples (SSO homework)

### US-1 — Sign up with SSO
**As a** new visitor, **I want** to sign up using my Google account, **so that** I can start using the product without creating a password.

Acceptance criteria:
- Given I am on the sign-up page and not logged in, when I click "Continue with Google" and complete Google consent, then an account is created with my Google email as the verified email and I land on the onboarding page.
- Given an account already exists for that email (password-based), when I complete Google consent, then I am **not** given a second account; I see a message offering to link Google to the existing account.
- Given Google consent fails or is cancelled, when I return to the app, then I see a clear error and no account is created.

Non-functional: tokens from the identity provider are never logged; the OAuth state parameter is validated; the flow completes in under 5 seconds on a normal connection.
Verification: `e2e/auth/sso-signup.spec.ts` (Playwright) covering the three criteria with a mocked identity provider.

### US-2 — Log in with SSO
**As a** registered user with a linked Google account, **I want** to log in with Google, **so that** I do not have to remember a password.

Acceptance criteria:
- Given my account has Google linked, when I click "Continue with Google" on the login page and consent succeeds, then I am logged in and redirected to where I was going (or the dashboard).
- Given my account exists but Google is not linked, when I try Google login, then I am asked to log in with my password first and then offered to link Google.
- Given my account is disabled, when I try Google login, then login is refused with the standard disabled-account message.

Verification: `e2e/auth/sso-login.spec.ts`.

## Task list (produced by the planning model, executed one at a time)
- [ ] T1 …
- [ ] T2 …

## Definition of done for this spec
All acceptance criteria have passing e2e tests; unit coverage on new code ≥ 90%; docs updated (`docs/data-model.md`, `docs/api-spec.yml`, `docs/architecture.md` if touched); security scan clean; spec archived/merged per the repo's SDD tool.
