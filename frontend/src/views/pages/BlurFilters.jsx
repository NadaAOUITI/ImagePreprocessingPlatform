import React, { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function BlurFilters() {
  const { state } = useLocation();
  const navigate = useNavigate();

  const imageSrc = state?.image;

  const originalCanvasRef = useRef(null);
  const processedCanvasRef = useRef(null);

  const [kernelSize, setKernelSize] = useState(5);

  // Charger l'image
  useEffect(() => {
    if (!imageSrc) return;

    const img = new Image();
    img.onload = () => {
      const o = originalCanvasRef.current;
      const p = processedCanvasRef.current;

      o.width = p.width = img.width;
      o.height = p.height = img.height;

      o.getContext("2d").drawImage(img, 0, 0);
      p.getContext("2d").drawImage(img, 0, 0);
    };
    img.src = imageSrc;
  }, [imageSrc]);

  // ---------- OUTILS ----------
  const clamp = v => Math.max(0, Math.min(255, v));

  const getKernelMean = k =>
    Array.from({ length: k * k }, () => 1 / (k * k));

  const getKernelGaussian = k => {
    const sigma = k / 6;
    const center = Math.floor(k / 2);
    let kernel = [];
    let sum = 0;

    for (let y = -center; y <= center; y++) {
      for (let x = -center; x <= center; x++) {
        const v = Math.exp(-(x * x + y * y) / (2 * sigma * sigma));
        kernel.push(v);
        sum += v;
      }
    }
    return kernel.map(v => v / sum);
  };

  // ---------- CONVOLUTION ----------
  const applyConvolution = (kernel) => {
    const canvas = processedCanvasRef.current;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imgData.data;

    const output = new Uint8ClampedArray(data);
    const k = Math.sqrt(kernel.length);
    const half = Math.floor(k / 2);

    for (let y = half; y < canvas.height - half; y++) {
      for (let x = half; x < canvas.width - half; x++) {
        let r = 0, g = 0, b = 0;

        let idx = 0;
        for (let ky = -half; ky <= half; ky++) {
          for (let kx = -half; kx <= half; kx++) {
            const px = ((y + ky) * canvas.width + (x + kx)) * 4;
            const w = kernel[idx++];
            r += data[px] * w;
            g += data[px + 1] * w;
            b += data[px + 2] * w;
          }
        }

        const i = (y * canvas.width + x) * 4;
        output[i] = clamp(r);
        output[i + 1] = clamp(g);
        output[i + 2] = clamp(b);
      }
    }

    imgData.data.set(output);
    ctx.putImageData(imgData, 0, 0);
  };

  // ---------- FILTRES ----------
  const blurMean = () => applyConvolution(getKernelMean(kernelSize));
  const blurGaussian = () => applyConvolution(getKernelGaussian(kernelSize));

  const blurMedian = () => {
    const canvas = processedCanvasRef.current;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imgData.data;
    const output = new Uint8ClampedArray(data);

    const half = Math.floor(kernelSize / 2);

    for (let y = half; y < canvas.height - half; y++) {
      for (let x = half; x < canvas.width - half; x++) {
        let rs = [], gs = [], bs = [];

        for (let ky = -half; ky <= half; ky++) {
          for (let kx = -half; kx <= half; kx++) {
            const i = ((y + ky) * canvas.width + (x + kx)) * 4;
            rs.push(data[i]);
            gs.push(data[i + 1]);
            bs.push(data[i + 2]);
          }
        }

        rs.sort((a, b) => a - b);
        gs.sort((a, b) => a - b);
        bs.sort((a, b) => a - b);

        const mid = Math.floor(rs.length / 2);
        const idx = (y * canvas.width + x) * 4;

        output[idx] = rs[mid];
        output[idx + 1] = gs[mid];
        output[idx + 2] = bs[mid];
      }
    }

    imgData.data.set(output);
    ctx.putImageData(imgData, 0, 0);
  };

  const resetImage = () => {
    const o = originalCanvasRef.current;
    const p = processedCanvasRef.current;
    p.getContext("2d").drawImage(o, 0, 0);
  };

  // ---------- UI ----------
  return (
    <div style={{ minHeight: "100vh", padding: 32 }}>
      <button onClick={() => navigate(-1)} style={backBtn}>⬅ Retour</button>

      <h1> Blur Filters </h1>

      <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", gap: 32 }}>

        {/* CONTROLS */}
        <aside style={panelStyle}>
          <h3>Paramètres</h3>

          <label>Noyau : {kernelSize}</label>
          <input
            type="range"
            min="3"
            max="21"
            step="2"
            value={kernelSize}
            onChange={e => setKernelSize(+e.target.value)}
            style={{ width: "100%" }}
          />

          <button style={btn} onClick={blurMean}>Blur Moyen</button>
          <button style={btn} onClick={blurGaussian}>Blur Gaussien</button>
          <button style={btn} onClick={blurMedian}>Blur Médian</button>

          <button style={{ ...btn, background: "#999" }} onClick={resetImage}>
            Réinitialiser
          </button>
        </aside>

        {/* IMAGES */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
          <div style={panelStyle}>
            <h3>Original</h3>
            <canvas ref={originalCanvasRef} style={canvasStyle} />
          </div>

          <div style={panelStyle}>
            <h3>Traité</h3>
            <canvas ref={processedCanvasRef} style={canvasStyle} />
          </div>
        </div>
      </div>
    </div>
  );
}

/* STYLES */
const panelStyle = {
  background: "white",
  padding: 20,
  borderRadius: 16,
  boxShadow: "0 4px 12px rgba(0,0,0,0.1)"
};

const canvasStyle = {
  width: "100%",
  borderRadius: 12
};

const btn = {
  width: "100%",
  padding: 12,
  marginTop: 12,
  borderRadius: 8,
  border: "none",
  background: "#1976d2",
  color: "white",
  fontWeight: 600,
  cursor: "pointer"
};

const backBtn = {
  marginBottom: 20,
  padding: "8px 16px",
  borderRadius: 8,
  border: "none",
  background: "#eee",
  cursor: "pointer",
  fontWeight: 600
};
