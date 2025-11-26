import React from "react";
import { useNavigate } from "react-router-dom";
export default function HomePage() {
    const navigate = useNavigate();

  const handleNavigate = () => {
    navigate("/gallery"); 
  };
 

  const features = [
    {
      title: "Import Simple",
      description: "Téléversez vos images aux formats JPG, PNG ou BMP pour traitement.",
      icon: "📤",
      color: "#2e7d32",
    },
    {
      title: "Prétraitement Interactif",
      description: "Appliquez des filtres, seuillage, redimensionnement et plus via une interface conviviale.",
      icon: "⚙️",
      color: "#1976d2",
    },
    {
      title: "Visualisation & Téléchargement",
      description: "Comparez les images originales et traitées et téléchargez-les facilement.",
      icon: "👁️",
      color: "#7b1fa2",
    },
  ];

  return (
    <div
      style={{
        height: "100vh",         // <-- remplit toute la hauteur du viewport
        width: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center", // centre verticalement
        alignItems: "center",     // centre horizontalement
        background: "linear-gradient(135deg, #fef9e7 0%, #ffffff 50%, #fef9e7 100%)",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        boxSizing: "border-box",
        padding: "40px 20px",
      }}
    >
      {/* Header */}
      <div style={{ textAlign: "center", maxWidth: "800px", marginBottom: "60px" }}>
        <div style={{ fontSize: "100px", marginBottom: "20px" }}>🖼️</div>
        <h1 style={{ fontSize: "2.5rem", fontWeight: 700, color: "#2c3e50", marginBottom: "20px" }}>
          Plateforme de Prétraitement d'Images
        </h1>
        <p style={{ fontSize: "1.2rem", color: "#546e7a", lineHeight: 1.6, marginBottom: "40px" }}>
          Téléversez vos images, appliquez des filtres et visualisez vos résultats en ligne.
        </p>
        <button
          onClick={handleNavigate}
          style={{
            backgroundColor: "#f9a825",
            color: "white",
            border: "none",
            padding: "16px 48px",
            fontSize: "1.1rem",
            fontWeight: 600,
            borderRadius: "12px",
            cursor: "pointer",
            boxShadow: "0 4px 12px rgba(249,168,37,0.2)",
            transition: "all 0.3s ease",
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = "#f57f17";
            e.currentTarget.style.transform = "translateY(-2px)";
            e.currentTarget.style.boxShadow = "0 8px 16px rgba(249,168,37,0.3)";
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = "#f9a825";
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "0 4px 12px rgba(249,168,37,0.2)";
          }}
        >
          Commencer
        </button>
      </div>

      {/* Features */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
          gap: "30px",
          maxWidth: "1000px",
          width: "100%",
        }}
      >
        {features.map((feature, index) => (
          <div
            key={index}
            style={{
              background: "white",
              padding: "30px 20px",
              borderRadius: "16px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
              textAlign: "center",
              transition: "all 0.3s ease",
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = "translateY(-8px)";
              e.currentTarget.style.boxShadow = "0 12px 24px rgba(0,0,0,0.1)";
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0 2px 8px rgba(0,0,0,0.1)";
            }}
          >
            <div style={{ fontSize: "50px", marginBottom: "16px" }}>{feature.icon}</div>
            <h3 style={{ fontSize: "1.3rem", fontWeight: 600, color: "#2c3e50", marginBottom: "12px" }}>
              {feature.title}
            </h3>
            <p style={{ fontSize: "0.95rem", color: "#546e7a", lineHeight: 1.5 }}>
              {feature.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
