import React from "react";
import { useImageStore } from "../../store/useImageStore";

function ImageHistoryPage() {
  const { images, selectedImage, revertToHistory } = useImageStore();

  if (selectedImage === null || !images[selectedImage]) {
    return <div>Aucune image sélectionnée.</div>;
  }

  const image = images[selectedImage];

  return (
    <div style={{ padding: 20 }}>
      <h2>Historique des actions</h2>

      <div style={{ marginBottom: 20 }}>
        <h3>Image actuelle :</h3>
        <img
          src={image.dataUrl}
          alt="Image sélectionnée"
          style={{ maxWidth: 300, border: "1px solid #ccc" }}
        />
      </div>

      <div>
        <h3>Journal des actions :</h3>
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {image.history.map((h, i) => (
            <li
              key={i}
              style={{
                marginBottom: 10,
                padding: 10,
                border: "1px solid #eee",
                borderRadius: 5,
              }}
            >
              <strong>{h.action}</strong> - {new Date(h.timestamp).toLocaleString()}
              <div style={{ marginTop: 5 }}>
                <button
                  onClick={() => revertToHistory(selectedImage, i)}
                  style={{ marginRight: 10 }}
                >
                  Revenir à cet état
                </button>
                <img
                  src={h.dataUrl}
                  alt="Preview"
                  style={{ width: 100, verticalAlign: "middle" }}
                />
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default ImageHistoryPage;
