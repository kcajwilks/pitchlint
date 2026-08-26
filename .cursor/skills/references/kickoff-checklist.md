# Kickoff checklist (new app from this starter)

Pack: [pack.md](pack.md). Stack is **Django + Vite + React**. Use with `/new-saas-app` or follow manually in **Agent mode**. Do not run Hallmark until plans are **Approved**.

## 1. Clone and remote

```bash
git clone git@github.com:kcajwilks/django-cookiecutter.git my-saas-app
cd my-saas-app
git remote remove origin
git remote add origin git@github.com:kcajwilks/my-saas-app.git
git branch -M main
git push -u origin main
```

## 2. Environment

- [ ] `cp core/.env.example core/.env` (do not copy secrets from another app)
- [ ] Set `DJANGO_SECRET_KEY`, Stripe keys if billing, `OPENAI_API_KEY` if AI
- [ ] `cd core && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- [ ] `python manage.py migrate`
- [ ] `python manage.py seed_plans` (optional)
- [ ] Or: `docker compose up --build` from repo root

## 3. Plan (Agent mode)

- [ ] Run `/plan-saas-from-starter` (or continue from `/new-saas-app`)
- [ ] Confirm a **design** plan element exists in `docs/plans/` + `PLANS.md`
- [ ] Human sets plans to **Approved** (do not self-approve)

## 4. Design (after approval)

- [ ] Run `/design-with-hallmark`
- [ ] Choose Hallmark verb: build (default) / study / redesign
- [ ] Marketing + light shell theming only (see `ui-surface-map.md`)

## 5. Implement

- [ ] Implement remaining approved domain plans (TDD / normal Agent work)
- [ ] Later UI changes: `/design-with-hallmark` with audit or redesign
