import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [amount, setAmount] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [analytics, setAnalytics] = useState(null);

  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);

  // Analytics
  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/analytics"
        );

        const data = await response.json();

        console.log("Analytics Response:", data);

        if (data.result) {
          setAnalytics(data.result);
        }
      } catch (error) {
        console.error("Analytics Error:", error);
      }
    };

    fetchAnalytics();
  }, []);

  // Fraud Prediction
  const handlePredict = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            V1: -1.359807,
            V2: -0.072781,
            V3: 2.536346,
            Amount: Number(amount),
          }),
        }
      );

      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error(error);
    }
  };

  // Upload Dataset
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/datasets/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();
      setUploadResult(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container">
      <h1 className="title">DecisionTwin AI</h1>

      <p className="subtitle">
        Fraud Detection & Transaction Analytics Platform
      </p>

      <h2>Transaction Analytics</h2>

      {analytics && (
        <div className="analytics-grid">
          <div className="card">
            <h3>Total Transactions</h3>
            <h2>{analytics.total_transactions}</h2>
          </div>

          <div className="card">
            <h3>Fraud Cases</h3>
            <h2>{analytics.fraud_cases}</h2>
          </div>

          <div className="card">
            <h3>Normal Cases</h3>
            <h2>{analytics.normal_cases}</h2>
          </div>

          <div className="card">
            <h3>Fraud Percentage</h3>
            <h2>{analytics.fraud_percentage}%</h2>
          </div>
        </div>
      )}

      <h2>Dataset Upload</h2>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br />
      <br />

      <button
        className="button"
        onClick={handleUpload}
      >
        Upload Dataset
      </button>

      {uploadResult && (
        <div className="result-card">
          <h3>Dataset Uploaded Successfully</h3>

          <p>
            Dataset ID: {uploadResult.dataset_id}
          </p>

          <p>
            File: {uploadResult.filename}
          </p>
        </div>
      )}

      <h2>Fraud Detection</h2>

      <input
        type="number"
        placeholder="Enter Amount"
        value={amount}
        onChange={(e) =>
          setAmount(e.target.value)
        }
        className="input"
      />

      <br />
      <br />

      <button
        onClick={handlePredict}
        className="button"
      >
        Predict Fraud
      </button>

      {prediction && (
        <div className="result-card">
          <h2>Prediction Result</h2>

          <h3>
            {prediction.result.prediction === 1
              ? "🚨 Fraud Detected"
              : "✅ Legitimate Transaction"}
          </h3>

          <h3>
            Confidence:{" "}
            {prediction.result.confidence}%
          </h3>
        </div>
      )}
    </div>
  );
}

export default App;