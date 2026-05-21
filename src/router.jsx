import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import DashboardPage from "./pages/DashboardPage";
import UploadPage from "./pages/UploadPage";
import ChatPage from "./pages/ChatPage";
import MainLayout from "./components/layout/MainLayout";

export default function Router() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>

          <Route path="/" element={<LandingPage />} />

          <Route path="/login" element={<LoginPage />} />

          <Route path="/signup" element={<SignupPage />} />

          <Route path="/dashboard" element={<DashboardPage />} />

          <Route path="/upload" element={<UploadPage />} />

          <Route path="/chat" element={<ChatPage />} />

        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}