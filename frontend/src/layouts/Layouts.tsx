import { Link, NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { useSite } from "../auth/SiteContext";
import { AppCopilot } from "../components/AppCopilot";

export function MarketingLayout() {
  const { user, logout } = useAuth();
  const { site_name: siteName } = useSite();
  return (
    <div className="shell">
      <header className="topnav">
        <Link to="/" className="brand">
          {siteName}
        </Link>
        <nav className="nav-links">
          <Link to="/pricing">Pricing</Link>
          {user ? (
            <>
              <Link to="/dashboard">Dashboard</Link>
              <button type="button" className="btn-ghost" onClick={() => logout()}>
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Log in</Link>
              <Link className="btn" to="/signup">
                Sign up
              </Link>
            </>
          )}
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer className="footer">
        <strong>{siteName}</strong> — API-ready SaaS shell. Built to ship, not to decorate.
      </footer>
    </div>
  );
}

export function AppLayout() {
  const { user, logout } = useAuth();
  const { site_name: siteName } = useSite();
  return (
    <AppCopilot>
      <div className="shell">
        <header className="topnav">
          <Link to="/dashboard" className="brand">
            {siteName}
          </Link>
          <nav className="nav-links">
            <span className="muted">{user?.email}</span>
            <button type="button" className="btn-ghost" onClick={() => logout()}>
              Log out
            </button>
          </nav>
        </header>
        <div className="app-frame">
          <aside className="sidebar">
            <span className="sidebar-label">App</span>
            <NavLink to="/dashboard" end className={({ isActive }) => (isActive ? "active" : undefined)}>
              Dashboard
            </NavLink>
            <NavLink to="/workspace" className={({ isActive }) => (isActive ? "active" : undefined)}>
              Workspace
            </NavLink>
            <span className="sidebar-label">Account</span>
            <NavLink to="/settings/profile" className={({ isActive }) => (isActive ? "active" : undefined)}>
              Profile
            </NavLink>
            <NavLink to="/settings/billing" className={({ isActive }) => (isActive ? "active" : undefined)}>
              Billing
            </NavLink>
            <NavLink to="/pricing" className={({ isActive }) => (isActive ? "active" : undefined)}>
              Pricing
            </NavLink>
          </aside>
          <div className="main">
            <Outlet />
          </div>
        </div>
      </div>
    </AppCopilot>
  );
}
