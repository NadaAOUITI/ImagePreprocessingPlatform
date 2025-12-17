import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const API_BASE = "http://localhost:5000/api"; // adapte si besoin

export default function BlurFilters() {
  const { state } = useLocation();
  const navigate = useNavigate();

  const originalImage = state?.image;
  const filename = state?.filename;

  const [processedImage, setProcessedImage] = useState(null);
  const [kernelSize, setKernelSize] = useState(5);
  const [loading, setLoading] = useState(false);

  const applyBlur = async (type) => {
    if (!filename) return alert("Image non valide");

    setLoading(true);

    const res = await fetch(`${API_BASE}/processing/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename,
        operation: type,
        parameters: { kernel_size: kernelSize }
      })
    });

    const data = await res.json();
    setLoading(false);

    if (data.output_file) {
      setProcessedImage(`${API_BASE}/processing/processed/${data.output_file}`);
    } else {
      alert(data.error || "Erreur lors du flou");
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #fef9e7, #ffffff)",
      padding: "32px",
      fontFamily: "'Segoe UI', sans-serif"
    }}>

      <button onClick={() => navigate(-1)} style={backBtn}>⬅ Retour</button>

      <h1 style={{ marginBottom: "24px" }}>🌫️ Blur Filters</h1>

      <div style={{ display: "grid", gridTemplateColumns: "300px 1fr", gap: "32px" }}>

        {/* CONTROLS */}
        <aside style={panelStyle}>
          <h3>Paramètres</h3>

          <label>Taille du noyau : {kernelSize}</label>
          <input
            type="range"
            min="3"
            max="21"
            step="2"
            value={kernelSize}
            onChange={(e) => setKernelSize(Number(e.target.value))}
            style={{ width: "100%" }}
          />

          <button style={btn} onClick={() => applyBlur("blur_mean")}>Blur Moyen</button>
          <button style={btn} onClick={() => applyBlur("blur_gaussian")}>Blur Gaussien</button>
          <button style={btn} onClick={() => applyBlur("blur_median")}>Blur Médian</button>
        </aside>

        {/* IMAGES */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
          <div style={panelStyle}>
            <h3>Image originale</h3>
            <img src={originalImage} alt="original" style={imgStyle} />
          </div>

          <div style={panelStyle}>
            <h3>Image floutée</h3>
            {loading && <p>⏳ Traitement...</p>}
            {processedImage ? (
              <img src={processedImage} alt="blurred" style={imgStyle} />
            ) : (
              <p>Aucun filtre appliqué</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ============ STYLES ============ */
const panelStyle = {
  background: "white",
  padding: "20px",
  borderRadius: "16px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.1)"
};

const imgStyle = {
  width: "100%",
  maxHeight: "500px",
  objectFit: "contain",
  marginTop: "16px",
  borderRadius: "12px"
};

const btn = {
  width: "100%",
  padding: "12px",
  marginTop: "12px",
  borderRadius: "8px",
  border: "none",
  background: "#1976d2",
  color: "white",
  fontWeight: 600,
  cursor: "pointer"
};

const backBtn = {
  marginBottom: "20px",
  padding: "8px 16px",
  borderRadius: "8px",
  border: "none",
  background: "#eeeeee",
  cursor: "pointer",
  fontWeight: 600
};
