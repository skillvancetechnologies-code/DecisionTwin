import React, { useEffect } from "react";
import UploadPage from "./pages/UploadPage";
import TestPage from "./pages/TestPage";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

function LandingPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[#050816] text-white">

      <div className="absolute left-[-100px] top-[100px] h-[300px] w-[300px] rounded-full bg-purple-600 opacity-30 blur-[120px]"></div>

      <div className="absolute right-[-100px] top-[200px] h-[300px] w-[300px] rounded-full bg-orange-500 opacity-20 blur-[120px]"></div>

      <nav className="relative z-10 flex items-center justify-between border-b border-white/10 bg-black/20 px-10 py-6">

        <h1 className="text-3xl font-bold">
          DecisionTwin
        </h1>

        <div className="flex gap-5">

          <Link
            to="/login"
            className="rounded-lg border border-white/20 px-5 py-2 hover:bg-white hover:text-black"
          >
            Login
          </Link>

          <Link
            to="/signup"
            className="rounded-lg bg-gradient-to-r from-orange-500 to-pink-500 px-5 py-2"
          >
            Sign Up
          </Link>

        </div>

      </nav>

      <section className="relative z-10 grid min-h-[90vh] items-center px-10 py-20 md:grid-cols-2 gap-12">

        <div>

          <div className="mb-6 inline-block rounded-full border border-purple-500/40 bg-purple-500/10 px-4 py-2">

            AI-Powered Decision Intelligence

          </div>

          <h1 className="text-6xl font-black leading-tight">

            AI-Powered

            <span className="bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
              {" "}Business Decision
            </span>

            Simulator

          </h1>

          <p className="mt-8 text-gray-300">

            Securely analyze business strategies,
            compare scenarios and gain AI-powered insights.

          </p>

        </div>

        <div className="rounded-3xl bg-white/5 p-6 backdrop-blur-xl">

          <div className="grid gap-4 md:grid-cols-3">

            <div className="rounded-2xl bg-black/30 p-5">
              <p className="text-gray-400">Revenue</p>
              <h3 className="text-3xl font-bold">$2.4M</h3>
              <p className="text-green-400">+12%</p>
            </div>

            <div className="rounded-2xl bg-black/30 p-5">
              <p className="text-gray-400">Risk</p>
              <h3 className="text-3xl font-bold">Low</h3>
            </div>

            <div className="rounded-2xl bg-black/30 p-5">
              <p className="text-gray-400">Confidence</p>
              <h3 className="text-3xl font-bold">85%</h3>
            </div>

          </div>

        </div>

      </section>

    </div>
  );
}

function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#050816] text-white">

      <div className="w-[400px] rounded-3xl bg-white/5 p-10">

        <h1 className="mb-8 text-4xl font-bold">
          Login
        </h1>

        <input
          placeholder="Email"
          className="mb-5 w-full rounded-xl bg-black/30 p-4"
        />

        <input
          placeholder="Password"
          className="mb-6 w-full rounded-xl bg-black/30 p-4"
        />

        <Link
          to="/dashboard"
          className="block rounded-xl bg-gradient-to-r from-orange-500 to-pink-500 py-4 text-center"
        >
          Login
        </Link>

      </div>

    </div>
  );
}

function SignupPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#050816] text-white">

      <div className="w-[400px] rounded-3xl bg-white/5 p-10">

        <h1 className="mb-8 text-4xl font-bold">
          Sign Up
        </h1>

        <input
          placeholder="Full Name"
          className="mb-5 w-full rounded-xl bg-black/30 p-4"
        />

        <input
          placeholder="Email"
          className="mb-5 w-full rounded-xl bg-black/30 p-4"
        />

        <input
          placeholder="Password"
          className="mb-6 w-full rounded-xl bg-black/30 p-4"
        />

        <Link
          to="/dashboard"
          className="block rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 py-4 text-center"
        >
          Create Account
        </Link>

      </div>

    </div>
  );
}

function DashboardPage() {

  const data =
    JSON.parse(
      sessionStorage.getItem("csvData")
    ) || [];

  const totalRevenue =
    data.reduce(
      (sum, row) =>
        sum + Number(row.revenue),
      0
    );

  const totalRows = data.length;
const chartData = Object.values(

  data.reduce((acc, item) => {

    if (!acc[item.month]) {

      acc[item.month] = {
        month: item.month,
        revenue: 0
      };

    }

    acc[item.month].revenue +=
      Number(item.revenue);

    return acc;

  }, {})

);

  useEffect(() => {

    const clearData = () => {

      sessionStorage.removeItem(
        "csvData"
      );

    };

    window.addEventListener(
      "beforeunload",
      clearData
    );

    return () => {

      window.removeEventListener(
        "beforeunload",
        clearData
      );

    };

  }, []);


  return (

    <div className="min-h-screen bg-[#050816] text-white p-10">

      <div className="flex items-center justify-between mb-10">

        <div>

          <h1 className="text-5xl font-bold">
            Analytics Dashboard
          </h1>

          <p className="mt-2 text-gray-400">
            AI-powered business insights and scenario analysis
          </p>

        </div>

        <Link
          to="/upload"
          className="rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 px-8 py-4 font-semibold shadow-[0_0_30px_rgba(150,80,255,0.5)]"
        >
          Upload Dataset
        </Link>

      </div>


      <div className="grid gap-6 md:grid-cols-4 mb-10">

        <div className="rounded-3xl bg-white/5 p-6">

          <p>Revenue</p>

          <h2 className="text-4xl font-bold">

            {totalRevenue > 0
              ? `$${totalRevenue}`
              : "$2.4M"}

          </h2>

        </div>


        <div className="rounded-3xl bg-white/5 p-6">

          <p>Risk Level</p>

          <h2 className="text-4xl text-orange-400">
            Medium
          </h2>

        </div>


        <div className="rounded-3xl bg-white/5 p-6">

          <p>Confidence</p>

          <h2 className="text-4xl text-green-400">
            85%
          </h2>

        </div>


        <div className="rounded-3xl bg-white/5 p-6">

          <p>Rows</p>

          <h2 className="text-4xl">
            {totalRows}
          </h2>

        </div>

      </div>


      <div className="grid gap-8 md:grid-cols-2">

        {/* Revenue Trend */}

        <div className="rounded-3xl bg-white/5 p-8">

          <h2 className="text-2xl font-bold mb-6">
            Revenue Trend
          </h2>

          
<div className="flex items-end justify-center gap-4 h-[220px]">

  {data.length > 0 ? (

    chartData.map((item, index) => (

      <div
        key={index}
        className="flex flex-col items-center"
      >

        <div
          className="w-10 rounded-t-xl bg-gradient-to-t from-purple-600 to-pink-500"
          style={{
            height: `${Math.min(
              Number(item.revenue)/100,
              180
            )}px`
          }}
        ></div>

        <p className="mt-2 text-sm text-gray-400">
          {item.month}
        </p>

      </div>

    ))

) : (

    <>
      <div className="w-10 h-20 rounded-t-xl bg-purple-500"></div>
      <div className="w-10 h-28 rounded-t-xl bg-purple-500"></div>
      <div className="w-10 h-40 rounded-t-xl bg-purple-500"></div>
      <div className="w-10 h-32 rounded-t-xl bg-purple-500"></div>
      <div className="w-10 h-52 rounded-t-xl bg-orange-500"></div>
    </>

  )}

</div>
</div>


        {/* AI */}

        <div className="rounded-3xl bg-white/5 overflow-hidden">

          <div className="border-b border-white/10 p-5">

            <h2 className="font-bold">
              AI Copilot
            </h2>

          </div>

          <div className="h-[250px] p-5">

            <div className="max-w-[80%] rounded-2xl rounded-tl-sm bg-purple-600 p-4">

              Hi 👋 Ask me about business scenarios

            </div>

          </div>

          <div className="flex gap-3 border-t border-white/10 p-4">

            <input
              placeholder="Type message..."
              className="flex-1 rounded-full bg-black/30 px-5 py-3"
            />

            <button
              className="rounded-full bg-purple-600 px-6"
            >
              ➤
            </button>

          </div>

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
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/test" element={<TestPage />} />

      </Routes>

    </BrowserRouter>
  );
}