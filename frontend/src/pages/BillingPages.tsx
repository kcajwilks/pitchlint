import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../auth/AuthContext";

type Plan = {
  code: string;
  name: string;
  tagline: string;
  features: string[];
  is_free: boolean;
  highlighted: boolean;
  monthly_amount_cents: number | null;
  yearly_amount_cents: number | null;
};

type PlansResponse = {
  plans: Plan[];
  billing_enabled: boolean;
  missing_env: string[];
};

type SubResponse = {
  status: string;
  plan_code: string | null;
  plan_name: string | null;
  current_period_end: string | null;
};

function formatCents(cents: number | null) {
  if (cents == null) return "—";
  return `$${(cents / 100).toFixed(0)}`;
}

function statusBadge(status: string | undefined) {
  const s = (status || "").toLowerCase();
  if (s === "active" || s === "trialing") return "badge badge-ok";
  if (s === "incomplete" || s === "past_due" || !s) return "badge badge-warn";
  return "badge";
}

function statusCopy(status: string | undefined) {
  const s = (status || "").toLowerCase();
  if (s === "active") return "Your subscription is active.";
  if (s === "trialing") return "You are on a trial.";
  if (s === "incomplete" || !s)
    return "No paid plan yet. Choose a plan to start checkout, or stay on Free.";
  if (s === "canceled") return "Subscription canceled. You can resubscribe from Pricing.";
  if (s === "past_due") return "Payment past due. Update your card in the Stripe portal.";
  return `Status: ${status}`;
}

export function PricingPage() {
  const { user } = useAuth();
  const [data, setData] = useState<PlansResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [interval, setIntervalBilling] = useState<"monthly" | "yearly">("monthly");
  const [checkoutCode, setCheckoutCode] = useState<string | null>(null);

  useEffect(() => {
    api<PlansResponse>("/api/billing/plans/")
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function checkout(planCode: string) {
    setError("");
    setCheckoutCode(planCode);
    try {
      const res = await api<{ url: string }>("/api/billing/checkout/", {
        method: "POST",
        body: JSON.stringify({ plan_code: planCode, interval }),
      });
      window.location.href = res.url;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Checkout failed");
      setCheckoutCode(null);
    }
  }

  return (
    <div className="hero">
      <div className="page-header" style={{ padding: 0 }}>
        <div>
          <h1>Pricing</h1>
          <p className="lede muted">Simple plans. Upgrade when you are ready to ship.</p>
        </div>
        <div className="segment" role="group" aria-label="Billing interval">
          <button
            type="button"
            className={interval === "monthly" ? "is-on" : ""}
            onClick={() => setIntervalBilling("monthly")}
          >
            Monthly
          </button>
          <button
            type="button"
            className={interval === "yearly" ? "is-on" : ""}
            onClick={() => setIntervalBilling("yearly")}
          >
            Yearly
          </button>
        </div>
      </div>

      {data && !data.billing_enabled ? (
        <div className="alert alert-warn" style={{ marginBottom: 24 }}>
          Stripe is not fully configured ({data.missing_env.join(", ") || "missing keys"}). Plan cards
          still show; checkout stays disabled until keys are set in{" "}
          <span className="mono">core/.env</span>.
        </div>
      ) : null}

      {error ? <div className="alert alert-err" style={{ marginBottom: 24 }}>{error}</div> : null}

      {loading ? (
        <p className="muted">Loading plans…</p>
      ) : !data?.plans?.length ? (
        <div className="empty">
          <h2>No plans in the database</h2>
          <p>
            From <span className="mono">core/</span> run{" "}
            <span className="mono">python manage.py seed_plans</span>, then refresh.
          </p>
        </div>
      ) : (
        <div className="grid-3" style={{ marginTop: 8 }}>
          {data.plans.map((plan) => (
            <div
              className={`card stack${plan.highlighted ? " card-highlight" : ""}`}
              key={plan.code}
            >
              <div className="row-actions" style={{ justifyContent: "space-between" }}>
                <h2 style={{ margin: 0 }}>{plan.name}</h2>
                {plan.highlighted ? <span className="badge badge-accent">Popular</span> : null}
              </div>
              <p className="muted" style={{ margin: 0 }}>
                {plan.tagline}
              </p>
              <p className="plan-price" style={{ margin: "8px 0" }}>
                {plan.is_free
                  ? "Free"
                  : formatCents(
                      interval === "monthly" ? plan.monthly_amount_cents : plan.yearly_amount_cents,
                    )}
                {!plan.is_free ? (
                  <span> / {interval === "monthly" ? "month" : "year"}</span>
                ) : null}
              </p>
              <ul className="feature-list">
                {(plan.features || []).map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
              {plan.is_free ? (
                user ? (
                  <Link className="btn btn-ghost" to="/dashboard">
                    Go to dashboard
                  </Link>
                ) : (
                  <Link className="btn" to="/signup">
                    Start free
                  </Link>
                )
              ) : user ? (
                <button
                  type="button"
                  onClick={() => checkout(plan.code)}
                  disabled={!data.billing_enabled || checkoutCode === plan.code}
                >
                  {checkoutCode === plan.code ? "Redirecting…" : `Choose ${plan.name}`}
                </button>
              ) : (
                <Link className="btn" to="/signup">
                  Sign up to upgrade
                </Link>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export function ProfileSettingsPage() {
  const { user } = useAuth();
  return (
    <div className="stack">
      <div className="page-header">
        <div>
          <h1>Profile</h1>
          <p className="lede muted">Account details for this workspace.</p>
        </div>
      </div>
      <div className="card stack">
        <div>
          <div className="muted" style={{ fontSize: "0.85em" }}>
            Email
          </div>
          <strong>{user?.email}</strong>
        </div>
        <div>
          <div className="muted" style={{ fontSize: "0.85em" }}>
            User ID
          </div>
          <span className="mono">{user?.id}</span>
        </div>
        <p className="muted" style={{ margin: 0, fontSize: "0.9em" }}>
          Password and Google connections are managed via django-allauth (
          <span className="mono">/accounts/</span>) when you enable those flows.
        </p>
      </div>
    </div>
  );
}

export function BillingSettingsPage() {
  const [sub, setSub] = useState<SubResponse | null>(null);
  const [plansMeta, setPlansMeta] = useState<PlansResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [portalBusy, setPortalBusy] = useState(false);

  useEffect(() => {
    Promise.all([
      api<SubResponse>("/api/billing/subscription/"),
      api<PlansResponse>("/api/billing/plans/"),
    ])
      .then(([s, p]) => {
        setSub(s);
        setPlansMeta(p);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function openPortal() {
    setError("");
    if (plansMeta && !plansMeta.billing_enabled) {
      setError(
        `Stripe is not configured (${(plansMeta.missing_env || []).join(", ") || "missing keys"}). Add keys to core/.env before opening the portal.`,
      );
      return;
    }
    setPortalBusy(true);
    try {
      const res = await api<{ url: string }>("/api/billing/portal/", {
        method: "POST",
        body: "{}",
      });
      window.location.href = res.url;
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to open billing portal. Complete checkout once so Stripe has a customer.",
      );
      setPortalBusy(false);
    }
  }

  const hasPaidPlan = Boolean(sub?.plan_code && sub.plan_code !== "free");

  return (
    <div className="stack">
      <div className="page-header">
        <div>
          <h1>Billing</h1>
          <p className="lede muted">Subscription status and Stripe customer portal.</p>
        </div>
        <Link className="btn" to="/pricing">
          Change plan
        </Link>
      </div>

      {error ? <div className="alert alert-err">{error}</div> : null}

      {loading ? (
        <p className="muted">Loading billing…</p>
      ) : (
        <>
          <div className="alert">{statusCopy(sub?.status)}</div>

          <div className="card stack">
            <div className="row-actions" style={{ justifyContent: "space-between" }}>
              <div>
                <div className="muted" style={{ fontSize: "0.85em" }}>
                  Current plan
                </div>
                <strong>{sub?.plan_name || sub?.plan_code || "Free / none"}</strong>
              </div>
              <span className={statusBadge(sub?.status)}>{sub?.status || "none"}</span>
            </div>

            {sub?.current_period_end ? (
              <p className="muted" style={{ margin: 0, fontSize: "0.9em" }}>
                Current period ends {new Date(sub.current_period_end).toLocaleDateString()}
              </p>
            ) : null}

            <div className="row-actions">
              <button type="button" className="btn-ghost" onClick={openPortal} disabled={portalBusy}>
                {portalBusy ? "Opening…" : "Open Stripe portal"}
              </button>
              {!hasPaidPlan ? (
                <Link className="btn" to="/pricing">
                  Choose a plan
                </Link>
              ) : null}
            </div>

            {plansMeta && !plansMeta.billing_enabled ? (
              <p className="muted" style={{ margin: 0, fontSize: "0.85em" }}>
                Portal and checkout need Stripe keys:{" "}
                {(plansMeta.missing_env || []).join(", ") || "see .env.example"}.
              </p>
            ) : !hasPaidPlan ? (
              <p className="muted" style={{ margin: 0, fontSize: "0.85em" }}>
                The portal needs an existing Stripe customer. Start a checkout from Pricing first.
              </p>
            ) : null}
          </div>
        </>
      )}
    </div>
  );
}
