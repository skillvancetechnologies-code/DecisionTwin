import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

function LandingPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[#050816] text-white">

      {/* Background Glow */}
      <div className="absolute left-[-100px] top-[100px] h-[300px] w-[300px] rounded-full bg-purple-600 opacity-30 blur-[120px]"></div>

      <div className="absolute right-[-100px] top-[200px] h-[300px] w-[300px] rounded-full bg-orange-500 opacity-20 blur-[120px]"></div>

      {/* Navbar */}
      <nav className="relative z-10 flex items-center justify-between border-b border-white/10 bg-black/20 px-10 py-6 backdrop-blur-md">

        <h1 className="text-3xl font-bold">
          DecisionTwin
        </h1>

        <div className="flex items-center gap-5">

          <Link
            to="/login"
            className="rounded-lg border border-white/20 px-5 py-2 hover:bg-white hover:text-black"
          >
            Login
          </Link>

          <Link
            to="/signup"
            className="rounded-lg bg-gradient-to-r from-orange-500 to-pink-500 px-5 py-2 font-semibold shadow-[0_0_25px_rgba(255,120,50,0.6)]"
          >
            Sign Up
          </Link>

        </div>

      </nav>

      {/* Hero */}
      <section className="relative z-10 grid min-h-[90vh] items-center gap-12 px-10 py-20 md:grid-cols-2">

        <div>

          <div className="mb-6 inline-block rounded-full border border-purple-500/40 bg-purple-500/10 px-4 py-2 text-sm text-purple-300 backdrop-blur-md">
            AI-Powered Decision Intelligence
          </div>

          <h1 className="max-w-2xl text-6xl font-black leading-tight">

            AI-Powered

            <span className="bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
              {" "}Business Decision
            </span>

            Simulator

          </h1>

          <p className="mt-8 max-w-xl text-lg leading-8 text-gray-300">

            Upload your business data, simulate decisions,
            analyze risks, and compare scenarios using AI.

          </p>

          <div className="mt-10 flex gap-5">

            <Link
              to="/upload"
              className="rounded-xl bg-gradient-to-r from-orange-500 to-pink-500 px-8 py-4 text-lg font-semibold shadow-[0_0_35px_rgba(255,120,50,0.7)]"
            >
              Get Started
            </Link>

            <Link
              to="/dashboard"
              className="rounded-xl border border-white/20 bg-white/5 px-8 py-4 text-lg font-semibold backdrop-blur-md hover:bg-white hover:text-black"
            >
              Dashboard
            </Link>

          </div>

        </div>

        {/* Dashboard Preview */}
        <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl backdrop-blur-xl">

          <div className="grid gap-4 md:grid-cols-3">

            <div className="rounded-2xl border border-white/10 bg-black/30 p-5">
              <p className="text-sm text-gray-400">Revenue</p>
              <h3 className="mt-3 text-3xl font-bold">$2.4M</h3>
              <p className="mt-2 text-green-400">+12%</p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/30 p-5">
              <p className="text-sm text-gray-400">Risk Score</p>
              <h3 className="mt-3 text-3xl font-bold">25</h3>
              <p className="mt-2 text-purple-400">Low Risk</p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/30 p-5">
              <p className="text-sm text-gray-400">Confidence</p>
              <h3 className="mt-3 text-3xl font-bold">85%</h3>
              <p className="mt-2 text-orange-400">High Accuracy</p>
            </div>

          </div>

          <div className="mt-8 rounded-2xl border border-white/10 bg-black/20 p-6">

            <div className="mb-6 flex items-end gap-4">

              <div className="h-20 w-10 rounded-t-xl bg-gradient-to-t from-purple-600 to-pink-400"></div>

              <div className="h-32 w-10 rounded-t-xl bg-gradient-to-t from-purple-600 to-pink-400"></div>

              <div className="h-24 w-10 rounded-t-xl bg-gradient-to-t from-purple-600 to-pink-400"></div>

              <div className="h-40 w-10 rounded-t-xl bg-gradient-to-t from-purple-600 to-pink-400"></div>

              <div className="h-28 w-10 rounded-t-xl bg-gradient-to-t from-purple-600 to-pink-400"></div>

              <div className="h-48 w-10 rounded-t-xl bg-gradient-to-t from-orange-500 to-pink-500"></div>

            </div>

            <p className="text-gray-400">
              Revenue Simulation Analytics
            </p>

          </div>

        </div>

      </section>

    </div>
  );
}

function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#050816] text-white">

      <div className="w-[400px] rounded-3xl border border-white/10 bg-white/5 p-10 backdrop-blur-xl">

        <h1 className="mb-8 text-4xl font-bold">
          Login
        </h1>

        <input
          type="email"
          placeholder="Email"
          className="mb-5 w-full rounded-xl border border-white/10 bg-black/30 p-4"
        />

        <input
          type="password"
          placeholder="Password"
          className="mb-6 w-full rounded-xl border border-white/10 bg-black/30 p-4"
        />

        <button className="w-full rounded-xl bg-gradient-to-r from-orange-500 to-pink-500 py-4 font-semibold">
          Login
        </button>

      </div>

    </div>
  );
}

function SignupPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#050816] text-white">

      <div className="w-[400px] rounded-3xl border border-white/10 bg-white/5 p-10 backdrop-blur-xl">

        <h1 className="mb-8 text-4xl font-bold">
          Sign Up
        </h1>

        <input
          type="text"
          placeholder="Full Name"
          className="mb-5 w-full rounded-xl border border-white/10 bg-black/30 p-4"
        />

        <input
          type="email"
          placeholder="Email"
          className="mb-5 w-full rounded-xl border border-white/10 bg-black/30 p-4"
        />

        <input
          type="password"
          placeholder="Password"
          className="mb-6 w-full rounded-xl border border-white/10 bg-black/30 p-4"
        />

        <button className="w-full rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 py-4 font-semibold">
          Create Account
        </button>

      </div>

    </div>
  );
}

function UploadPage() {
  return (
    <div className="min-h-screen bg-[#050816] p-10 text-white">

      <h1 className="mb-10 text-5xl font-bold">
        Upload Dataset
      </h1>

      <div className="rounded-3xl border-2 border-dashed border-purple-500 bg-white/5 p-20 text-center backdrop-blur-xl">

        <p className="text-2xl text-gray-300">
          Drag & Drop CSV File Here
        </p>

        <button className="mt-8 rounded-xl bg-gradient-to-r from-orange-500 to-pink-500 px-8 py-4">
          Browse Files
        </button>

      </div>

    </div>
  );
}

function DashboardPage() {
  return (
    <div className="min-h-screen bg-[#050816] p-10 text-white">

      <h1 className="mb-10 text-5xl font-bold">
        Analytics Dashboard
      </h1>

      <div className="grid gap-6 md:grid-cols-3">

        <div className="rounded-3xl bg-white/5 p-8 backdrop-blur-xl">
          <p className="text-gray-400">Revenue</p>
          <h2 className="mt-4 text-4xl font-bold">$2.4M</h2>
        </div>

        <div className="rounded-3xl bg-white/5 p-8 backdrop-blur-xl">
          <p className="text-gray-400">Risk Level</p>
          <h2 className="mt-4 text-4xl font-bold text-orange-400">
            Medium
          </h2>
        </div>

        <div className="rounded-3xl bg-white/5 p-8 backdrop-blur-xl">
          <p className="text-gray-400">Confidence</p>
          <h2 className="mt-4 text-4xl font-bold text-green-400">
            85%
          </h2>
        </div>

      </div>

    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<LandingPage />} />

        <Route path="/login" element={<LoginPage />} />

        <Route path="/signup" element={<SignupPage />} />

        <Route path="/upload" element={<UploadPage />} />

        <Route path="/dashboard" element={<DashboardPage />} />

      </Routes>

    </BrowserRouter>
  );
}