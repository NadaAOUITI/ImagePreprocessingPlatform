// src/views/pages/ErrorPage.jsx

import React from "react";
import { useNavigate } from "react-router-dom";

export default function ErrorPage({ message }) {
  const navigate = useNavigate();

  return (
    <div style={{
      textAlign: "center",
      padding: "50px"
    }}>
      <h1 style={{ color: "red" }}>⚠️ Erreur</h1>

      <p style={{ fontSize: "18px" }}>
        {message || "Une erreur inattendue est survenue."}
      </p>

      <button
        onClick={() => navigate("/")}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          backgroundColor: "#1976d2",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Retour à l'accueil
      </button>
    </div>
  );
}
