# Feature plan template (docs-plans mapping)

Pack: [pack.md](pack.md). Use this shape for every greenfield SaaS element plan under `docs/plans/<slug>.md`. Follow the vendored `docs-plans` skill for frontmatter, `PLANS.md`, and status lifecycle. Inventory: `django-saas-starter`.

```markdown
---
status: Pending Review
owner: <name>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Title>

## Context
Product intent for this element; who needs it. 2–3 paragraphs of known facts.

## Findings
What the starter already provides (cite apps/paths from `django-saas-starter`).

## Root Cause
The gap — why this element is not already done.

## Proposed Solution
How to extend the starter. Include **Starter mapping**:
- reuse: …
- extend: …
- new app: …

## Implementation Steps
- [ ] Step 1
- [ ] Step 2 (requires migration)  # mark schema work

## Risks & Dependencies
- Other element plans, Stripe, Copilot, deploy, design plan

## Expected Outcome
User-visible MVP criterion for this element.

---
Owner: <name>
Last reviewed: YYYY-MM-DD
Review cadence: on change
```

### Always-included design element

`/plan-saas-from-starter` always emits a design plan (slug like `marketing-shell-design`). That plan is implemented by `/design-with-hallmark` after approval — not by inventing CSS ad hoc.
