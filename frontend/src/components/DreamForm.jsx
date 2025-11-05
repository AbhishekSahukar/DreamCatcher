import React, { useState } from "react";
import { saveAs } from "file-saver";
import "../App.css";

export default function DreamForm() {
  const [dream, setDream] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  // 🔮 Analyze dream
  const analyzeDream = async () => {
    if (!dream.trim()) return;
    setLoading(true);
    const res = await fetch("http://localhost:8000/analyse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dream }),
    });
    const data = await res.json();
    setResponse(data.interpretation);
    setLoading(false);
  };

  // 🧾 Download as PDF
  const downloadPDF = async () => {
    const res = await fetch("http://localhost:8000/download-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dream }),
    });
    const blob = await res.blob();
    saveAs(blob, "dream_interpretation.pdf");
  };

  return (
  <div className="app-container">
  

    <div className="chat-container">
      <div className="chat-messages">
        {response && (
          <div className="chat-message bot">
            <strong>Interpretation:</strong> {response}
          </div>
        )}
      </div>

      {response && (
        <button onClick={downloadPDF} className="download-btn">
          Download as PDF
        </button>
      )}

      <div className="input-area">
        <input
          type="text"
          value={dream}
          onChange={(e) => setDream(e.target.value)}
          placeholder="Describe your dream..."
        />
        <button onClick={analyzeDream} disabled={loading}>
          {loading ? "Interpreting..." : "Send"}
        </button>
      </div>
    </div>
  </div>
);
}
