import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import { SiteProvider } from "./auth/SiteContext";
import { AppLayout, MarketingLayout } from "./layouts/Layouts";
import { LoginPage, SignupPage } from "./pages/AuthPages";
import {
  DashboardPage,
  RequireAuth,
  WorkspaceDetailPage,
  WorkspaceListPage,
} from "./pages/AppPages";
import { BillingSettingsPage, PricingPage, ProfileSettingsPage } from "./pages/BillingPages";
import { HomePage } from "./pages/HomePage";

export default function App() {
  return (
    <SiteProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<MarketingLayout />}>
              <Route index element={<HomePage />} />
              <Route path="pricing" element={<PricingPage />} />
              <Route path="login" element={<LoginPage />} />
              <Route path="signup" element={<SignupPage />} />
            </Route>
            <Route
              element={
                <RequireAuth>
                  <AppLayout />
                </RequireAuth>
              }
            >
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="workspace" element={<WorkspaceListPage />} />
              <Route path="workspace/:id" element={<WorkspaceDetailPage />} />
              <Route path="settings/profile" element={<ProfileSettingsPage />} />
              <Route path="settings/billing" element={<BillingSettingsPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </SiteProvider>
  );
}
