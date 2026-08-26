---
name: docs-plans
description: >
  Organisation standard for creating and managing work plans in the docs/plans/ directory.
  Use this skill whenever IBM Bob (or any agent) is asked to investigate a problem, propose
  a fix, plan a feature, audit code, or document a technical decision. Triggers on: "write a
  plan", "create a plan", "add to docs/plans", "document the approach", "plan for review",
  "track this work", "update the plan tracker", "what's in progress", "mark as complete",
  "create an investigation plan", or any request that ends with output going into docs/plans/.
  Always use this skill before writing any file under docs/plans/ — it defines the file
  structure, plan format, status values, and how to update the master tracker.
---

# docs/plans — Planning Standards

All investigation, optimisation, and feature work is tracked under `docs/plans/`.
There are two things to maintain:

1. **Individual plan files** — one per piece of work
2. **`docs/plans/PLANS.md`** — the master tracker that lists every plan and its status

Never write a plan file without also updating `PLANS.md`.

---

## Directory Layout

```
docs/
└── plans/
    ├── PLANS.md                          ← master tracker (always update this)
    ├── sync-command-optimisation.md
    ├── recovery-reports-performance.md
    └── <slug>.md
```

---

## Master Tracker — `docs/plans/PLANS.md`

`PLANS.md` is a single table of all plans. Every row represents one plan file.

### Format

```markdown
# Plans Tracker

| Plan | File | Status | Owner | Created | Updated | Notes |
|------|------|--------|-------|---------|---------|-------|
| Sync command optimisation | [sync-command-optimisation.md](sync-command-optimisation.md) | 🔵 In Progress | IBM Bob | 2026-06-24 | 2026-06-24 | Initial investigation |
| Recovery reports performance | [recovery-reports-performance.md](recovery-reports-performance.md) | 🟡 Pending Review | IBM Bob | 2026-06-24 | 2026-06-24 | Awaiting team sign-off |
```

### Status Values

| Emoji | Status | Meaning |
|-------|--------|---------|
| ⚪ | Backlog | Identified, not yet started |
| 🔵 | In Progress | Actively being worked on |
| 🟡 | Pending Review | Plan written, awaiting human review |
| 🟢 | Approved | Plan reviewed and approved — ready to implement |
| 🔨 | Implementing | Code/changes being applied |
| ✅ | Complete | Fully implemented and verified |
| ❌ | Cancelled | No longer being pursued |
| 🔁 | Superseded | Replaced by a newer plan (link the new one in Notes) |

### Rules

- **Always update `PLANS.md`** when creating or changing a plan file.
- Set status to `🟡 Pending Review` when first writing a plan — a human must approve before implementation begins.
- Update the `Updated` date whenever the file changes.
- Never delete rows — use `❌ Cancelled` or `🔁 Superseded` instead.

---

## Individual Plan Files

Each plan lives at `docs/plans/<slug>.md`. Use kebab-case slugs that describe the problem, not the solution (e.g. `sync-command-optimisation`, not `fix-bulk-writes`).

### Required Structure

```markdown
---
status: Pending Review
owner: IBM Bob
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Title>

## Context
What is the problem? What symptoms are observed? Who reported it and when?
Keep this to 2–3 paragraphs. No speculation here — only known facts.

## Findings
What was discovered during investigation? Include:
- Specific code locations (file paths, function names, line numbers)
- Query counts, timing data, or other measurements where available
- The exact behaviour causing the problem

## Root Cause
One paragraph. The single clearest statement of why the problem exists.

## Proposed Solution
What should change and why. Use code snippets for non-obvious changes.

```python
# Before
for item in queryset:
    item.save()

# After — single bulk write
MyModel.objects.bulk_update(queryset, fields=["field_a", "field_b"])
```

If there are multiple options, present them as a table:

| Option | Pros | Cons | Recommended? |
|--------|------|------|--------------|
| Bulk upsert | Fast, minimal DB round-trips | Requires Django 4.1+ | ✅ Yes |
| Manual diff | Works on older Django | More complex code | No |

## Implementation Steps
A numbered checklist. Each step is small enough to ship independently if possible.

- [ ] Step 1 — description
- [ ] Step 2 — description
- [ ] Step 3 — description (requires migration — flag for review)

Mark steps that require a database migration with `(requires migration)` so they are reviewed before running.

## Risks & Dependencies
- List anything that could go wrong
- List other plans or systems this depends on or affects

## Expected Outcome
What will be measurably better after this is implemented? Be specific:
> Sync command runtime reduced from ~4 min to <30 s on a dataset of 50,000 records.
> Recovery report page load reduced from ~8 s to <1 s with query count dropping from 300+ to <10.

---
Owner: IBM Bob
Last reviewed: YYYY-MM-DD
Review cadence: on change
```

---

## Workflow — Step by Step

### When creating a new plan

1. Choose a slug: `<topic>-<type>` e.g. `sync-command-optimisation`, `auth-refactor`, `celery-worker-scaling`
2. Create `docs/plans/<slug>.md` using the structure above
3. Set frontmatter `status: Pending Review`
4. Open `docs/plans/PLANS.md` and add a new row with status `🟡 Pending Review`
5. Update the `Updated` date on the `PLANS.md` header row

### When updating a plan

1. Edit the plan file with new findings or revised steps
2. Update the `updated` date in the frontmatter
3. Update the `Updated` column and `Notes` in `PLANS.md`
4. If the status has changed (e.g. approved, implementing, complete), update both places

### When a plan is approved

1. Change status to `🟢 Approved` in both the plan file and `PLANS.md`
2. Implementation can now begin

### When implementation starts

1. Change status to `🔨 Implementing`
2. Tick off steps in the Implementation Steps checklist as they are completed

### When work is complete

1. Change status to `✅ Complete`
2. Add a brief completion note in `PLANS.md` Notes column (e.g. "Deployed 2026-06-30, p95 latency down 87%")

---

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| Writing a plan file but not updating `PLANS.md` | Always update both at the same time |
| Setting status to `Approved` yourself | Only humans approve — write the plan, set `Pending Review`, stop |
| Vague findings ("queries are slow") | Include file paths, function names, and measurements |
| Implementation steps with no migration flag | Mark any step touching the schema with `(requires migration)` |
| Deleting cancelled plans | Set status `❌ Cancelled` and keep the row |
| One plan covering multiple unrelated problems | Split into separate plan files; link them in the Notes column |
| Merging context and findings into one section | Keep them separate — context is what was known before; findings are what was discovered |
