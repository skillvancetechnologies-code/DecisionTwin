import { createBrowserRouter } from "react-router-dom";
import RootLayout from "./components/layout/RootLayout.jsx";
import LandingPage from "./pages/LandingPage.jsx";
import UploadPage from "./pages/UploadPage.jsx";
import BaselinePage from "./pages/BaselinePage.jsx";
import SimulatePage from "./pages/SimulatePage.jsx";
import ChatPage from "./pages/ChatPage.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import NotFoundPage from "./pages/NotFoundPage.jsx";

export const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      { path: "/", element: <LandingPage /> },
      { path: "/upload", element: <UploadPage /> },
      { path: "/baseline/:datasetId", element: <BaselinePage /> },
      { path: "/simulate/:datasetId", element: <SimulatePage /> },
      { path: "/chat/:sessionId", element: <ChatPage /> },
      { path: "/dashboard", element: <DashboardPage /> },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
]);
