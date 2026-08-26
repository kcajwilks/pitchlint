import { FormEvent, useEffect, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import { api, type Project } from "../api/client";
import { useAuth } from "../auth/AuthContext";
export function RequireAuth({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <p className="muted">Loading…</p>;
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export function DashboardPage() {
  const { user } = useAuth();
  const [projectCount, setProjectCount] = useState<number | null>(null);

  useEffect(() => {
    api<Project[]>("/api/projects/")
      .then((rows) => setProjectCount(rows.length))
      .catch(() => setProjectCount(null));
  }, []);

  return (
    <div className="stack">
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p className="lede muted">Welcome back{user?.email ? `, ${user.email}` : ""}.</p>
        </div>
        <Link className="btn" to="/workspace">
          New project
        </Link>
      </div>

      <div className="stat-strip" style={{ margin: 0, padding: 0, maxWidth: "none" }}>
        <div className="stat">
          <strong>{projectCount == null ? "—" : projectCount}</strong>
          <span className="muted">Projects in workspace</span>
        </div>
        <div className="stat">
          <strong>API</strong>
          <span className="muted">Session auth on /api</span>
        </div>
        <div className="stat">
          <strong>Billing</strong>
          <span className="muted">Stripe when keys are set</span>
        </div>
      </div>

      <div className="grid-2">
        <div className="card stack">
          <h2>Workspace</h2>
          <p className="muted">
            Create projects, generate AI briefs, and attach CopilotKit when enabled.
          </p>
          <div className="row-actions">
            <Link className="btn" to="/workspace">
              Open workspace
            </Link>
          </div>
        </div>
        <div className="card stack">
          <h2>Plan & billing</h2>
          <p className="muted">Pick a plan or open the Stripe customer portal for invoices and cards.</p>
          <div className="row-actions">
            <Link className="btn" to="/pricing">
              View pricing
            </Link>
            <Link className="btn btn-ghost" to="/settings/billing">
              Billing settings
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export function WorkspaceListPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  async function load() {
    const data = await api<Project[]>("/api/projects/");
    setProjects(data);
  }

  useEffect(() => {
    load()
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function createProject(e: FormEvent) {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      await api<Project>("/api/projects/", {
        method: "POST",
        body: JSON.stringify({ name, description }),
      });
      setName("");
      setDescription("");
      setShowForm(false);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Create failed");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="stack">
      <div className="page-header">
        <div>
          <h1>Workspace</h1>
          <p className="lede muted">Projects you own. Generate AI briefs from the detail page.</p>
        </div>
        <button type="button" className="btn" onClick={() => setShowForm((v) => !v)}>
          {showForm ? "Cancel" : "New project"}
        </button>
      </div>

      {error ? <div className="alert alert-err">{error}</div> : null}

      {showForm ? (
        <form className="card stack" onSubmit={createProject}>
          <h2>New project</h2>
          <div className="field">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Cost API explorer"
              required
              autoFocus
            />
          </div>
          <div className="field">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="What is this project for?"
            />
          </div>
          <div className="row-actions">
            <button type="submit" disabled={saving}>
              {saving ? "Creating…" : "Create project"}
            </button>
            <button type="button" className="btn-ghost" onClick={() => setShowForm(false)}>
              Cancel
            </button>
          </div>
        </form>
      ) : null}

      {loading ? (
        <p className="muted">Loading projects…</p>
      ) : projects.length === 0 ? (
        <div className="empty">
          <h2>No projects yet</h2>
          <p>Create your first project to try CRUD, AI briefs, and Copilot against the REST API.</p>
          <button type="button" className="btn" onClick={() => setShowForm(true)}>
            Create a project
          </button>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: "hidden" }}>
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Updated</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {projects.map((p) => (
                <tr key={p.id}>
                  <td>
                    <Link to={`/workspace/${p.id}`}>{p.name}</Link>
                    {p.description ? (
                      <div className="muted" style={{ fontSize: "0.85em", marginTop: 2 }}>
                        {p.description.slice(0, 80)}
                        {p.description.length > 80 ? "…" : ""}
                      </div>
                    ) : null}
                  </td>
                  <td className="mono muted">{new Date(p.updated_at).toLocaleString()}</td>
                  <td style={{ textAlign: "right" }}>
                    <Link to={`/workspace/${p.id}`}>Open</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export function WorkspaceDetailPage() {
  const { id } = useParams();
  const [project, setProject] = useState<Project | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!id) return;
    api<Project>(`/api/projects/${id}/`)
      .then(setProject)
      .catch((e) => setError(e.message));
  }, [id]);

  async function generateBrief() {
    if (!id) return;
    setBusy(true);
    setError("");
    try {
      const updated = await api<Project>(`/api/projects/${id}/generate-brief/`, {
        method: "POST",
        body: "{}",
      });
      setProject(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Brief failed");
    } finally {
      setBusy(false);
    }
  }

  if (!project && !error) return <p className="muted">Loading project…</p>;
  if (!project) {
    return (
      <div className="empty">
        <h2>Project not found</h2>
        <p>{error || "This project may have been deleted."}</p>
        <Link className="btn" to="/workspace">
          Back to workspace
        </Link>
      </div>
    );
  }

  return (
    <div className="stack">
      <p>
        <Link to="/workspace">← Workspace</Link>
      </p>
      <div className="page-header">
        <div>
          <h1>{project.name}</h1>
          <p className="lede muted">{project.description || "No description yet."}</p>
        </div>
        <button type="button" onClick={generateBrief} disabled={busy}>
          {busy ? "Generating…" : "Generate AI brief"}
        </button>
      </div>

      {error ? <div className="alert alert-err">{error}</div> : null}

      <div className="card stack">
        <div className="row-actions" style={{ justifyContent: "space-between" }}>
          <h2 style={{ margin: 0 }}>AI brief</h2>
          {project.ai_brief_updated_at ? (
            <span className="badge">
              Updated {new Date(project.ai_brief_updated_at).toLocaleString()}
            </span>
          ) : (
            <span className="badge">Not generated</span>
          )}
        </div>
        {project.ai_brief ? (
          <pre className="mono" style={{ whiteSpace: "pre-wrap", margin: 0 }}>
            {project.ai_brief}
          </pre>
        ) : (
          <div className="empty" style={{ padding: "1.5rem" }}>
            <p style={{ marginBottom: 0 }}>
              No brief yet. Ask the Copilot sidebar to generate one, or use the button above
              (needs <span className="mono">OPENAI_API_KEY</span>).
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
