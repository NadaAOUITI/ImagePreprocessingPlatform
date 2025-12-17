import React, { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function EdgeFilters() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const imageSrc = state?.image;

  const originalCanvas = useRef(null);
  const processedCanvas = useRef(null);

  const [low, setLow] = useState(50);
  const [high, setHigh] = useState(150);

  useEffect(() => {
    if (!imageSrc) return;
    const img = new Image();
    img.onload = () => {
      [originalCanvas, processedCanvas].forEach(ref => {
        ref.current.width = img.width;
        ref.current.height = img.height;
        ref.current.getContext("2d").drawImage(img, 0, 0);
      });
    };
    img.src = imageSrc;
  }, [imageSrc]);

  /* ---------- OUTILS ---------- */
  const clamp = v => Math.max(0, Math.min(255, v));

  const toGray = (data) => {
    for (let i = 0; i < data.length; i += 4) {
      const g = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
      data[i] = data[i + 1] = data[i + 2] = g;
    }
  };

  const applyKernel = (kernelX, kernelY = null) => {
    const canvas = processedCanvas.current;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const img = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = img.data;
    const out = new Uint8ClampedArray(data);

    toGray(data);

    const k = Math.sqrt(kernelX.length);
    const h = Math.floor(k / 2);

    for (let y = h; y < canvas.height - h; y++) {
      for (let x = h; x < canvas.width - h; x++) {
        let gx = 0, gy = 0;
        let idx = 0;

        for (let ky = -h; ky <= h; ky++) {
          for (let kx = -h; kx <= h; kx++) {
            const p = ((y + ky) * canvas.width + (x + kx)) * 4;
            gx += data[p] * kernelX[idx];
            if (kernelY) gy += data[p] * kernelY[idx];
            idx++;
          }
        }

        const mag = kernelY ? Math.sqrt(gx * gx + gy * gy) : Math.abs(gx);
        const i = (y * canvas.width + x) * 4;
        out[i] = out[i + 1] = out[i + 2] = clamp(mag);
      }
    }

    img.data.set(out);
    ctx.putImageData(img, 0, 0);
  };

  /* ---------- FILTRES ---------- */

  const sobel = () => {
    applyKernel(
      [-1,0,1,-2,0,2,-1,0,1],
      [-1,-2,-1,0,0,0,1,2,1]
    );
  };

  const prewitt = () => {
    applyKernel(
      [-1,0,1,-1,0,1,-1,0,1],
      [-1,-1,-1,0,0,0,1,1,1]
    );
  };

  const laplacian = () => {
    applyKernel([0,1,0,1,-4,1,0,1,0]);
  };

  const canny = () => {
    sobel();
    const ctx = processedCanvas.current.getContext("2d");
    const img = ctx.getImageData(0, 0, processedCanvas.current.width, processedCanvas.current.height);
    const d = img.data;

    for (let i = 0; i < d.length; i += 4) {
      const v = d[i];
      const edge = v >= high ? 255 : v >= low ? 128 : 0;
      d[i] = d[i + 1] = d[i + 2] = edge;
    }
    ctx.putImageData(img, 0, 0);
  };

  const reset = () => {
    processedCanvas.current
      .getContext("2d")
      .drawImage(originalCanvas.current, 0, 0);
  };

  /* ---------- UI ---------- */
  return (
    <div style={{ minHeight: "100vh", padding: 32 }}>
      <button onClick={() => navigate(-1)} style={backBtn}>⬅ Retour</button>

      <h1> Edge Detection </h1>

      <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", gap: 32 }}>

        <aside style={panel}>
          <h3>Paramètres Canny</h3>

          <label>Low: {low}</label>
          <input type="range" min="0" max="255" value={low}
            onChange={e => setLow(+e.target.value)} />

          <label>High: {high}</label>
          <input type="range" min="0" max="255" value={high}
            onChange={e => setHigh(+e.target.value)} />

          <button style={btn} onClick={sobel}>Sobel</button>
          <button style={btn} onClick={prewitt}>Prewitt</button>
          <button style={btn} onClick={laplacian}>Laplacian</button>
          <button style={btn} onClick={canny}>Canny</button>

          <button style={{ ...btn, background: "#999" }} onClick={reset}>Réinitialiser</button>
        </aside>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
          <div style={panel}>
            <h3>Original</h3>
            <canvas ref={originalCanvas} style={canvas} />
          </div>

          <div style={panel}>
            <h3>Contours</h3>
            <canvas ref={processedCanvas} style={canvas} />
          </div>
        </div>
      </div>
    </div>
  );
}

/* STYLES */
const panel = {
  background: "#fff",
  padding: 20,
  borderRadius: 16,
  boxShadow: "0 4px 12px rgba(0,0,0,0.1)"
};

const canvas = { width: "100%", borderRadius: 12 };

const btn = {
  width: "100%",
  padding: 12,
  marginTop: 10,
  borderRadius: 8,
  border: "none",
  background: "#1976d2",
  color: "#fff",
  fontWeight: 600
};

const backBtn = {
  marginBottom: 20,
  padding: "8px 16px",
  borderRadius: 8,
  border: "none",
  background: "#eee",
  fontWeight: 600
};
