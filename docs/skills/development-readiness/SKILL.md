---
name: development-readiness
description: Apply a professional development-readiness standard before implementing or changing software or product specifications. Use for product development, PRDs and product decisions, coding, frontend and backend changes, bug fixes, refactors, migrations, database or API changes, architecture work, build and CI changes, integrations, deployment preparation, and other implementation-facing work. Establish intent, ownership boundaries, sources of truth, baseline differences, invariants, failure behavior, risks, UI states, executable acceptance criteria, branch discipline, and handoff evidence before mutation, then implement, document, verify, commit, and archive according to project authority.
---

# Development Readiness

Apply this standard before technical implementation. Turn human intent into verifiable engineering constraints without burdening trivial work with unnecessary ceremony.

## Use the authoritative copy

For the Echo project, treat `echo-doc/docs/skills/development-readiness/` as the authoritative shared copy. Treat personal `.codex/skills/development-readiness/` directories as installed replicas. Change the repository copy through review, validation, commit, and remote archival first, then synchronize installed replicas. Do not maintain undocumented professional variants.

## Run the preflight

Before modifying files or external state:

1. Inspect repository instructions, current branch, working-tree state, relevant code, tests, configuration, schemas, and documentation.
2. Classify the request as explanation, diagnosis, change, migration, or release. Do not mutate for explanation or diagnosis unless explicitly authorized.
3. Write a compact task contract containing:
   - **Outcome**: the observable result, not merely the requested mechanism.
   - **Reason**: the problem or risk being addressed.
   - **Scope and authority**: allowed systems, modules, files, data, and external actions.
   - **Sources of truth**: authoritative code, schema, protocol, specification, or configuration.
   - **Invariants and non-goals**: behavior, compatibility, security rules, and user work that must remain unchanged.
   - **Failure behavior**: fail closed, retry, roll back, degrade, or stop; never invent silent fallback.
   - **Acceptance**: executable checks and business-visible outcomes.
4. Distinguish explicitly between confirmed facts, engineering inference, and decisions requiring human or product authority.
5. Ask only when a missing decision materially changes behavior, data, security, cost, compatibility, or external state. Otherwise state a safe assumption and proceed.

Share the contract briefly in commentary when it helps the user verify direction. Keep it internal for obvious, low-risk edits.

## Scale rigor to risk

Use a fast path for localized, reversible changes: identify the target, preserve behavior, edit minimally, and run the nearest test.

Use a full preflight for changes involving any of the following:

- databases, schemas, migrations, destructive operations, or persistent data;
- public APIs, protocols, error codes, authentication, authorization, privacy, or security;
- concurrency, transactions, distributed state, caches, queues, or retries;
- paid or rate-limited external services;
- dependency, build, CI, deployment, release, or branch-policy changes;
- broad refactors or changes crossing multiple ownership boundaries.

For full preflight, include compatibility, rollout, rollback, observability, and ownership.

## Establish the frontend boundary

For client, web, mobile, desktop UI, or frontend-facing API work, separate presentation responsibilities from business authority before implementation.

Treat the frontend as responsible for:

- presenting product information, affordances, status, feedback, and navigation;
- collecting user input with clear validation guidance and preserving unfinished input through recoverable flows;
- orchestrating page, modal, login, upload, retry, and return-path flows;
- managing ephemeral UI state such as selection, focus, expansion, local drafts, loading indicators, and optimistic visuals with an explicit rollback path;
- accessibility, responsive layout, input ergonomics, perceived performance, and user-facing copy;
- translating server DTOs into view models without changing their business meaning.

Treat the backend as authoritative for:

- identity, authentication, authorization, ownership, eligibility, and visibility;
- business status transitions, allowed actions, validation, moderation, consent, and policy decisions;
- durable data, IDs, relationships, timestamps, counters, quotas, time windows, ordering, ranking, and recommendation membership;
- idempotency, concurrency, deduplication, audit trails, and cross-device consistency;
- derived facts that affect money, access, safety, compliance, distribution, or other users.

Do not make local storage, URL state, a mock implementation, hidden UI, disabled buttons, client clocks, or client-calculated counters the business source of truth. The frontend may cache or preview data, but the server result must reconcile it. Do not show a successful write state before the server accepts the write unless the product explicitly permits optimistic behavior and rollback is implemented.

### Run the frontend preflight

Before changing a user-visible flow, identify:

1. **Surface and actor**: page or component, entry points, viewer role, ownership, anonymous/bound state, and device constraints.
2. **Displayed information**: exact server fields, nullability, field-level visibility, ID semantics, formatting ownership, and source timestamps.
3. **Collected information**: field purpose, required/optional status, limits, upload rules, draft lifetime, privacy notice, and whether input must survive login, navigation, retry, or refresh.
4. **Flow states**: initial, loading, refreshing, empty, editing, submitting, success, partial success, validation failure, authentication required, forbidden, conflict, rate-limited, offline, unavailable, deleted/taken down, and retry exhausted.
5. **Allowed actions**: prefer server-returned capabilities or status over reimplementing policy in the client. Hiding an action is presentation, never authorization.
6. **Navigation behavior**: URL/deep link, back stack, refresh restoration, cancel destination, original-flow resumption, and stale-target behavior.
7. **Consistency behavior**: request deduplication, double-submit prevention, stale responses, pagination, optimistic rollback, refetch triggers, and cross-tab/device reconciliation.
8. **Acceptance**: responsive and accessibility checks, component state tests, DTO/contract tests, and end-to-end tests against a real boundary for critical flows.

When a frontend requirement lacks a backend contract, report the minimum missing contract as data, state, action, error, and timing needs. Do not invent server policy in the component. Escalate product choices that change what users see or can do; escalate backend choices that change authority, persistence, consistency, or security.

## Apply the product development standard

Treat implementation-facing product work as development work, not as informal discussion. Apply this section whenever changing a PRD, product decision, user flow, page contract, system topology, API-facing requirement, acceptance rule, or implementation plan.

### Start from the maintained baseline

1. Read the project's compact product baseline first. Read full historical documents only when the changed topic, an unresolved conflict, or evidence requires them.
2. Identify the affected product mainline step, branch systems, core objects, actors, states, and cross-system relationships.
3. Verify current implementation facts from relevant frontend and backend code. A document, field, enum, mock, or unfinished route does not by itself prove a working capability.
4. Separate four statements in the task record:
   - previously confirmed product baseline;
   - current implemented behavior;
   - newly confirmed target behavior;
   - the exact implementation gap.
5. Classify the change as local, cross-system, or foundation-level. For foundation-level changes, trace object identity, lifecycle, visibility, moderation, attribution, notifications, migration, compatibility, analytics, privacy, rollback, and affected clients before approval.

Do not make each developer reconstruct the full product history. Maintain a compact, current skeleton that links to detailed specifications and lets frontend, backend, QA, design, operations, and product recover the relevant context quickly.

### Maintain one current product skeleton

After a product decision is confirmed, update all applicable layers in the same change set:

- the compact product baseline and change synopsis;
- the authoritative decision register;
- the affected domain or page specification;
- API contracts, state machines, data ownership, and error semantics when implementation-facing;
- acceptance scenarios and the role-specific handoff summary;
- implementation audit or gap register when actual code still differs from the target.

Record explicit supersession when a new decision changes an older rule. Preserve historical evidence, but mark which rule is current, why it changed, what remains unchanged, and which systems must migrate. Never leave two apparently active definitions for the same object or flow.

For every confirmed change, produce a concise delta that answers:

```text
Mainline step and affected systems:
Previous confirmed behavior:
Current implemented behavior:
New confirmed behavior:
Changed objects, states, fields, interfaces, and pages:
Preserved invariants and deliberately unchanged areas:
Frontend work:
Backend work:
QA and operational checks:
Migration or compatibility work:
Open decisions and blockers:
```

The delta is the default developer entry point. Link to evidence instead of asking implementers to reread every historical document.

### Keep product, frontend, and backend synchronized

- Define the visible user journey together with server-owned authority. For each page or action, specify actor, entry, displayed data, allowed action, result state, failure state, return path, and authoritative endpoint.
- When product intent lacks an executable contract, mark it as a gap; do not let frontend invent backend state or let backend invent user-visible policy.
- Assign one source of truth for each object, status, transition, permission, counter, time window, and ID. Describe projections and foreign-key relationships explicitly.
- Keep anonymous/bound, self/other, private/public, normal/moderated, online/offline, and success/failure states in the same matrix where they alter behavior.
- Produce implementation plans only for the delta between target and verified code. Label existing capability as reuse, migration, replacement, deprecation, or no change.

### Use branches and archive every confirmed change

Before editing product or implementation artifacts:

1. Inspect repository instructions, current branch, dirty files, remote configuration, and branch policy.
2. Preserve unrelated user work. If the relevant tree already contains overlapping uncommitted changes, resolve ownership before creating a branch or commit.
3. Use a focused branch that follows the repository convention; default to a short `codex/<topic>` branch when no project convention exists.
4. Keep the documentation delta and the implementation it governs traceable. Use one coherent commit when they belong to one change; otherwise use linked commits with the same decision or issue identifier.
5. Run document hygiene, link/reference checks, contract checks, and relevant code tests before committing.
6. Write a commit message and handoff note that name the product decision, affected systems, implementation delta, verification, and remaining gaps.
7. When the user or project has established remote archival as the standing workflow, commit every confirmed change and push the focused branch to its configured remote. Verify the remote branch or commit exists before reporting completion.

Do not claim “recorded,” “finalized,” “submitted,” or “archived” when changes exist only in the working tree. If branch creation, commit, or push is blocked by unrelated changes, missing remote, authentication, protection rules, or network failure, preserve the work, report the exact state, and stop before fabricating success. Do not force-push, rewrite shared history, or bypass review/protection rules unless separately authorized.

Product exploration that has not been confirmed may remain a clearly labeled draft and must not silently enter the authoritative baseline. Once confirmed, it must follow the branch, synchronized-document, commit, and remote archival path above.

## Implement from intent

- Prefer one authoritative implementation over parallel abstractions.
- Encode important rules in types, interfaces, enums, constraints, startup validation, and tests rather than comments alone.
- Keep business policy out of infrastructure and infrastructure details out of domain services.
- Keep backend-owned business decisions out of frontend components. Model server facts with explicit DTOs and model display-only transformations separately.
- Use mocks to exercise UI states, not to prove backend behavior or end-to-end completion. Mark mock-only fields and transitions so they cannot silently become production assumptions.
- Preserve user changes and unrelated dirty-worktree content. Inspect overlap before editing.
- Make the smallest coherent change that achieves the outcome; do not broaden scope because adjacent cleanup is attractive.
- Resolve contradictions by following the declared source of truth. Report unresolved conflicts instead of choosing silently.
- Never weaken production validation merely to make tests pass. Update stale fixtures when the production rule is confirmed.
- Treat migrations and external writes as separate, explicit deliverables with safe ordering and recovery behavior.

## Validate with evidence

Choose checks proportional to risk and run them after implementation:

1. Static and hygiene checks: formatting, compilation, type checks, generated-code consistency, and diff validation.
2. Focused tests for changed behavior, including negative and failure paths.
3. Broader regression tests for affected modules.
4. Integration tests against real boundaries when mocks cannot prove the requirement.
5. End-to-end or smoke tests for user-visible critical paths.
6. Data integrity, restart persistence, idempotency, concurrency, migration, or rollback checks when relevant.

For frontend work, verify at least the changed visual and interaction states, keyboard or assistive access where applicable, narrow and wide layouts, error recovery, navigation/back behavior, and the real API response shape. A successful production build does not prove a user flow works.

Do not claim completion from a command that skipped tests, used stale artifacts, or failed to exercise the changed path. Separate failures caused by the change from pre-existing failures and provide evidence for that distinction.

## Finish cleanly

Report:

- the achieved outcome;
- material implementation decisions and preserved invariants;
- tests and real-world checks run, with their results;
- remaining risks, blocked decisions, and unrelated failures;
- files, commits, migrations, or operational actions that matter to handoff.

Do not deploy, tag, migrate production data, rewrite shared history, or contact external parties unless the user authorized that action. Do not commit or push by default for ordinary tasks; however, follow an explicit user or project standing rule that requires confirmed product/development changes to be committed and pushed. Before committing, confirm the intended branch, exclude unrelated user changes, and verify the remote result before reporting archival.

## Reusable task contract

Use this compact form when a task benefits from an explicit contract:

```text
Outcome:
Reason:
Scope and authority:
Sources of truth:
Invariants and non-goals:
Failure behavior:
Acceptance evidence:
Decisions still required:
```

Optimize for this principle: express intent as boundaries, encode rules as constraints, and prove outcomes with executable evidence.
