import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <>
      <section className="hero">
        <h1>Ship AI SaaS without rebuilding the shell</h1>
        <p>
          Auth, billing, workspace, and CopilotKit on Django REST — with a React
          front end you can restyle, not rewrite.
        </p>
        <div className="hero-actions">
          <Link className="btn" to="/signup">
            Start free
          </Link>
          <Link className="btn btn-ghost" to="/pricing">
            See pricing
          </Link>
        </div>
      </section>
      <section className="stat-strip">
        <div className="stat">
          <strong>REST</strong>
          <span className="muted">Session-authenticated JSON API</span>
        </div>
        <div className="stat">
          <strong>Stripe</strong>
          <span className="muted">Checkout and portal wired</span>
        </div>
        <div className="stat">
          <strong>Agents</strong>
          <span className="muted">Agno + CopilotKit ready</span>
        </div>
      </section>
      <section className="hero" style={{ paddingTop: 0 }}>
        <div className="grid-3">
          <div className="card stack">
            <h2>1. Sign up</h2>
            <p className="muted">Email/password session auth against /api.</p>
          </div>
          <div className="card stack">
            <h2>2. Create a project</h2>
            <p className="muted">Workspace CRUD + optional AI brief.</p>
          </div>
          <div className="card stack">
            <h2>3. Upgrade</h2>
            <p className="muted">Pricing cards and Stripe when keys are set.</p>
          </div>
        </div>
      </section>
    </>
  );
}
