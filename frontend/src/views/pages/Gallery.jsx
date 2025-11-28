

// src/pages/Gallery.jsx
import React, { useRef } from "react";
import { useImageStore } from "../../store/useImageStore";
import { useNavigate } from "react-router-dom";

const Gallery = () => {
  const fileInputRef = useRef(null);
  const { images, selectedImage, setSelectedImage, removeImage, addImages ,selectImageWithHistory} = useImageStore();
  const navigate= useNavigate();
  const handleUploadClick = () => fileInputRef.current.click();

  const { clearImages } = useImageStore();

  const handleFiles = (e) => {
    const files = Array.from(e.target.files);
    const valid = ["image/jpeg", "image/png", "image/bmp"];

    const validImages = files.filter((file) => valid.includes(file.type));
    if (validImages.length === 0) {
      alert("Veuillez choisir des images JPG, PNG ou BMP.");
      return;
    }

    Promise.all(
      validImages.map(
        (file) =>
          new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = (ev) => resolve({ dataUrl: ev.target.result, name: file.name });
            reader.readAsDataURL(file);
          })
      )
    ).then(addImages);
  };

  /** ---------------- BUTTON STYLES ---------------- */
  const buttonStyle = {
    padding: "12px 24px",
    backgroundColor: "#2e7d32",
    color: "white",
    border: "none",
    borderRadius: "8px",
    fontSize: "1rem",
    fontWeight: 600,
    cursor: "pointer",
    transition: "all 0.3s ease",
    boxShadow: "0 2px 8px rgba(46,125,50,0.2)",
  };

  const buttonHoverStyle = {
    backgroundColor: "#1b5e20",
    transform: "translateY(-2px)",
    boxShadow: "0 4px 12px rgba(46,125,50,0.3)",
  };

  const deleteButtonStyle = {
    position: "absolute",
    top: "8px",
    right: "8px",
    padding: "6px 12px",
    backgroundColor: "#d32f2f",
    color: "white",
    border: "none",
    borderRadius: "6px",
    fontSize: "0.85rem",
    fontWeight: 600,
    cursor: "pointer",
    transition: "all 0.3s ease",
  };

  /** ---------------- EMPTY STATE ---------------- */
  if (images.length === 0) {
    return (

      <div
        style={{
         
          width: "100%",
          display: "flex",
          minHeight: "100vh",

          background: "linear-gradient(135deg, #fef9e7, #ffffff, #fef9e7)",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "40px 20px",
          fontFamily: "'Segoe UI', sans-serif",
        }}
      >
        {/* BOUTON HOME */}
<button
  onClick={() => navigate("/")}
  style={{
    position: "fixed",
    top: "20px",
    left: "20px",
    padding: "10px 20px",
    backgroundColor: "#f9a825",
    color: "white",
    border: "none",
    borderRadius: "8px",
    fontSize: "0.95rem",
    fontWeight: 600,
    cursor: "pointer",
    oxShadow: "0 4px 12px rgba(249,168,37,0.2)",
    transition: "all 0.3s ease",
  }}
  onMouseOver={(e) => {
    e.currentTarget.style.transform = "translateY(-2px)";
  }}
  onMouseOut={(e) => {
    e.currentTarget.style.transform = "translateY(0)";
  }}
>
  ⬅️ Home
</button>


        <div style={{ fontSize: "80px", marginBottom: "20px" }}>📁</div>

        <h2 style={{ fontSize: "1.8rem", fontWeight: 600, color: "#2c3e50", marginBottom: "16px" }}>
          Aucune image disponible
        </h2>

        <p style={{ fontSize: "1.1rem", color: "#546e7a", marginBottom: "32px" }}>
          Importez des images pour commencer le prétraitement.
        </p>

        <button
          onClick={handleUploadClick}
          style={{ ...buttonStyle }}
          onMouseOver={(e) => Object.assign(e.currentTarget.style, buttonHoverStyle)}
          onMouseOut={(e) => Object.assign(e.currentTarget.style, buttonStyle)}
        >
          📤 Importer des Images
        </button>

        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/bmp"
          multiple
          style={{ display: "none" }}
          onChange={handleFiles}
        />
      </div>
    );
  }

  /** ---------------- MAIN UI ---------------- */
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #fef9e7, #ffffff, #fef9e7)",
        padding: "40px 20px",
        fontFamily: "'Segoe UI', sans-serif",
      }}
    >
      <div style={{ maxWidth: "1400px", margin: "0 auto" }}>
        {/* HEADER */}
        <button
   onClick={() => {
    
    clearImages(); // supprime tout
   
    navigate("/"); // Aller à la page Home
  }}
  style={{
    position: "fixed",
    top: "20px",
    left: "20px",
    padding: "10px 20px",
    backgroundColor: "#f9a825",
    color: "white",
    border: "none",
    borderRadius: "8px",
    fontSize: "0.95rem",
    fontWeight: 600,
    cursor: "pointer",
    oxShadow: "0 4px 12px rgba(249,168,37,0.2)",
    transition: "all 0.3s ease",
  }}
  onMouseOver={(e) => {
    e.currentTarget.style.transform = "translateY(-2px)";
  }}
  onMouseOut={(e) => {
    e.currentTarget.style.transform = "translateY(0)";
  }}
>
  ⬅️ 
</button>



        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "40px",
            flexWrap: "wrap",
            gap: "20px",
          }}
        >
          <h1 style={{ fontSize: "2rem", fontWeight: 700, color: "#2c3e50" }}>🖼️ Galerie d'Images</h1>

          <button
            onClick={handleUploadClick}
            style={{ ...buttonStyle }}
            onMouseOver={(e) => Object.assign(e.currentTarget.style, buttonHoverStyle)}
            onMouseOut={(e) => Object.assign(e.currentTarget.style, buttonStyle)}
          >
            ➕ Ajouter des Images
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/png,image/bmp"
            multiple
            style={{ display: "none" }}
            onChange={handleFiles}
          />
        </div>

        {/* GRID */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
            gap: "24px",
            marginBottom: "40px",
          }}
        >
          {images.map((img, index) => {
            const isSelected = selectedImage === index;

            return (
              <div
                key={index}
                style={{
                  position: "relative",
                  backgroundColor: "white",
                  borderRadius: "12px",
                  overflow: "hidden",
                  cursor: "pointer",
                  transition: "all 0.3s ease",
                  boxShadow: isSelected
                    ? "0 0 0 4px #f9a825"
                    : "0 2px 8px rgba(0,0,0,0.1)",
                }}
                onClick={() => selectImageWithHistory(index)}
                onMouseEnter={(e) => {
                  if (!isSelected) {
                    e.currentTarget.style.transform = "translateY(-4px)";
                    e.currentTarget.style.boxShadow = "0 8px 16px rgba(0,0,0,0.15)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (!isSelected) {
                    e.currentTarget.style.transform = "translateY(0)";
                    e.currentTarget.style.boxShadow = "0 2px 8px rgba(0,0,0,0.1)";
                  }
                }}
              >
                <img
                  src={img.dataUrl}
                  alt=""
                  style={{ width: "100%", height: "220px", objectFit: "cover" }}
                />

                {/* DELETE BUTTON */}
                <button
                  style={{ ...deleteButtonStyle }}
                  onClick={(e) => {
                    e.stopPropagation();
                    removeImage(index);
                  }}
                  onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#b71c1c")}
                  onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#d32f2f")}
                >
                  🗑️ Supprimer
                </button>

                {/* IMAGE NAME */}
                <div style={{ padding: "12px", borderTop: "1px solid #f0f0f0", background: "white" }}>
                  <p
                    style={{
                      fontSize: "0.9rem",
                      color: "#546e7a",
                      fontWeight: 500,
                      overflow: "hidden",
                      whiteSpace: "nowrap",
                      textOverflow: "ellipsis",
                    }}
                  >
                    {img.name || `Image ${index + 1}`}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* SELECTED IMAGE PANEL */}
        {selectedImage !== null && (
          <div
            style={{
              backgroundColor: "white",
              borderRadius: "16px",
              padding: "32px",
              boxShadow: "0 4px 16px rgba(0,0,0,0.1)",
            }}
          >
            <h2
              style={{
                fontSize: "1.5rem",
                fontWeight: 600,
                color: "#2c3e50",
                marginBottom: "24px",
                display: "flex",
                alignItems: "center",
                gap: "10px",
              }}
            >
              ⭐ Image sélectionnée
            </h2>

            <img
              src={images[selectedImage].dataUrl}
              alt=""
              style={{
                width: "100%",
                maxWidth: "900px",
                margin: "0 auto",
                display: "block",
                borderRadius: "12px",
                boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
              }}
            />
          </div>
        )}
        {/* BUTTON GO TO PROCESSING */}
      <div style={{ marginTop: "30px", textAlign: "center" }}>
        <button
          onClick={() => {
         if (selectedImage !== null) navigate("/processing");
          }}
          style={{
            padding: "14px 32px",
            backgroundColor: "#1565c0",
            color: "white",
            border: "none",
            borderRadius: "10px",
            fontSize: "1.1rem",
            fontWeight: 600,
            cursor: "pointer",
            transition: "all 0.3s ease",
            boxShadow: "0 4px 12px rgba(21,101,192,0.3)",
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = "#0d47a1";
            e.currentTarget.style.transform = "translateY(-3px)";
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = "#1565c0";
            e.currentTarget.style.transform = "translateY(0)";
          }}
        >
           Processing
        </button>
      </div>

      </div>
    </div>
  );
};

export default Gallery;
