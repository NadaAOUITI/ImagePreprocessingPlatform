// src/views/pages/ProcessingWorkspace.jsx
import React, { useRef, useState, useEffect, useCallback } from "react";
import {
  Box,
  Button,
  Container,
  Grid,
  Paper,
  Slider,
  Typography,
  IconButton,
  Stack,
  Divider,
  Tooltip,
} from "@mui/material";
import UndoIcon from "@mui/icons-material/Undo";
import RedoIcon from "@mui/icons-material/Redo";
import RefreshIcon from "@mui/icons-material/Refresh";
import DownloadIcon from "@mui/icons-material/Download";
import ZoomInIcon from "@mui/icons-material/ZoomIn";
import ZoomOutIcon from "@mui/icons-material/ZoomOut";
import ImageIcon from "@mui/icons-material/Image";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";
import { useImageStore } from "../../store/useImageStore";
import { useNavigate } from "react-router-dom";
import { useHistogramStore } from "../../store/useHistogramStore";
export default function ProcessingWorkspace() {
  const navigate = useNavigate();


const { addHistogram } = useHistogramStore();
  // Refs
  const originalCanvasRef = useRef(null);
  const processedCanvasRef = useRef(null);
  const originalImgRef = useRef(null);

  // split view
  const [split, setSplit] = useState(0.5);
  const splitRef = useRef(false);

  // pan/zoom
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const isPanningRef = useRef(false);
  const panStartRef = useRef({ x: 0, y: 0 });

  // processing params
  const [grayscale, setGrayscale] = useState(false);
  const [threshold, setThreshold] = useState(128);
  const [blur, setBlur] = useState(0);
  const [resizePercent, setResizePercent] = useState(100);
  const [rotation, setRotation] = useState(0);
  const [flipH, setFlipH] = useState(false);
  const [flipV, setFlipV] = useState(false);
  const [normalize, setNormalize] = useState(false);
  const [equalize, setEqualize] = useState(false);
  const [segmentationRGB, setSegmentationRGB] = useState(false);

  // ROI
  const [roi, setRoi] = useState(null);
  const roiDragRef = useRef(false);
  const roiStartRef = useRef(null);

  // undo/redo stacks (for settings)
  const undoStackRef = useRef([]);
  const redoStackRef = useRef([]);

  // store access
  const {
    images,
    selectedImage,
    addHistory,
    addImages,
    setSelectedImage,
  } = useImageStore();

  // local image src (keeps sync with store selectedImage)
  const [imageSrc, setImageSrc] = useState(
    selectedImage !== null ? images[selectedImage]?.dataUrl : null
  );

  // Keep local imageSrc in sync when user selects another image in gallery
  useEffect(() => {
    const src = selectedImage !== null ? images[selectedImage]?.dataUrl : null;
    setImageSrc(src || null);
  }, [selectedImage, images]);

  // Helper: push current param state to undo stack
  const pushStateToUndo = useCallback(() => {
    const state = {
      grayscale,
      threshold,
      blur,
      resizePercent,
      rotation,
      flipH,
      flipV,
      normalize,
      equalize,
      segmentationRGB,
      roi,
      // Note: We don't push image dataUrl here to avoid huge strings in undo;
      // image reverting is handled via history entries.
    };
    undoStackRef.current.push(JSON.stringify(state));
    if (undoStackRef.current.length > 50) undoStackRef.current.shift();
    redoStackRef.current = [];
  }, [
    grayscale,
    threshold,
    blur,
    resizePercent,
    rotation,
    flipH,
    flipV,
    normalize,
    equalize,
    segmentationRGB,
    roi,
  ]);

  // Undo / Redo handlers (settings only)
  const handleUndo = () => {
    const u = undoStackRef.current;
    if (u.length === 0) return;
    const last = u.pop();
    redoStackRef.current.push(
      JSON.stringify({
        grayscale,
        threshold,
        blur,
        resizePercent,
        rotation,
        flipH,
        flipV,
        normalize,
        equalize,
        segmentationRGB,
        roi,
      })
    );
    const st = JSON.parse(last);
    applyStateFromObject(st, false);
  };

  const handleRedo = () => {
    const r = redoStackRef.current;
    if (r.length === 0) return;
    const last = r.pop();
    undoStackRef.current.push(
      JSON.stringify({
        grayscale,
        threshold,
        blur,
        resizePercent,
        rotation,
        flipH,
        flipV,
        normalize,
        equalize,
        segmentationRGB,
        roi,
      })
    );
    const st = JSON.parse(last);
    applyStateFromObject(st, false);
  };

  const applyStateFromObject = (st, pushUndo = true) => {
    if (pushUndo) pushStateToUndo();
    setGrayscale(st.grayscale ?? false);
    setThreshold(st.threshold ?? 128);
    setBlur(st.blur ?? 0);
    setResizePercent(st.resizePercent ?? 100);
    setRotation(st.rotation ?? 0);
    setFlipH(st.flipH ?? false);
    setFlipV(st.flipV ?? false);
    setNormalize(st.normalize ?? false);
    setEqualize(st.equalize ?? false);
    setSegmentationRGB(st.segmentationRGB ?? false);
    setRoi(st.roi ?? null);
  };

  const handleReset = () => {
    pushStateToUndo();
    applyStateFromObject(
      {
        grayscale: false,
        threshold: 128,
        blur: 0,
        resizePercent: 100,
        rotation: 0,
        flipH: false,
        flipV: false,
        normalize: false,
        equalize: false,
        segmentationRGB: false,
        roi: null,
      },
      false
    );
  };

  // commit change to history: takes a short action description
  const commitChange = (action) => {
    if (selectedImage === null) return;
    const canvas = processedCanvasRef.current;
    if (!canvas) return;
    try {
      const newDataUrl = canvas.toDataURL("image/png");
      addHistory(selectedImage, action, newDataUrl);
    } catch (e) {
      // cross-origin or other issues
      console.warn("Impossible d'enregistrer l'historique (toDataURL):", e);
    }
  };

  // redraw canvases and apply pixel-level ops (preview)
  const redrawCanvases = useCallback(() => {
    const img = originalImgRef.current;
    const origCanvas = originalCanvasRef.current;
    const procCanvas = processedCanvasRef.current;
    if (!img || !origCanvas || !procCanvas) return;

    const oCtx = origCanvas.getContext("2d");
    const pCtx = procCanvas.getContext("2d");

    const baseW = img.width;
    const baseH = img.height;
    const scale = resizePercent / 100;
    const w = Math.max(1, Math.round(baseW * scale));
    const h = Math.max(1, Math.round(baseH * scale));

    const dpr = window.devicePixelRatio || 1;
    origCanvas.width = img.width * dpr;
    origCanvas.height = img.height * dpr;
    origCanvas.style.width = `${img.width}px`;
    origCanvas.style.height = `${img.height}px`;

    procCanvas.width = w * dpr;
    procCanvas.height = h * dpr;
    procCanvas.style.width = `${w}px`;
    procCanvas.style.height = `${h}px`;

    oCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    oCtx.clearRect(0, 0, img.width, img.height);
    oCtx.drawImage(img, 0, 0, img.width, img.height);

    const filters = [];
    if (blur > 0) filters.push(`blur(${blur}px)`);
    if (grayscale) filters.push("grayscale(1)");

    pCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    pCtx.clearRect(0, 0, w, h);

    try {
      pCtx.filter = filters.join(" ") || "none";
    } catch (e) {
      pCtx.filter = "none";
    }

    pCtx.save();
    if (rotation !== 0 || flipH || flipV) {
      pCtx.translate(w / 2, h / 2);
      pCtx.rotate((rotation * Math.PI) / 180);
      pCtx.scale(flipH ? -1 : 1, flipV ? -1 : 1);
      pCtx.drawImage(img, -w / 2, -h / 2, w, h);
    } else {
      pCtx.drawImage(img, 0, 0, w, h);
    }
    pCtx.restore();

    // pixel manipulations when toggled on (done in preview)
    if (threshold !== 128 || segmentationRGB || normalize || equalize || grayscale) {
      const imgData = pCtx.getImageData(0, 0, procCanvas.width, procCanvas.height);
      const data = imgData.data;

      if (normalize) {
        let min = 255,
          max = 0;
        for (let i = 0; i < data.length; i += 4) {
          const lum = 0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2];
          if (lum < min) min = lum;
          if (lum > max) max = lum;
        }
        const range = max - min || 1;
        for (let i = 0; i < data.length; i += 4) {
          data[i] = ((data[i] - min) * 255) / range;
          data[i + 1] = ((data[i + 1] - min) * 255) / range;
          data[i + 2] = ((data[i + 2] - min) * 255) / range;
        }
      }

      if (equalize) {
        const histR = new Array(256).fill(0);
        const histG = new Array(256).fill(0);
        const histB = new Array(256).fill(0);
        for (let i = 0; i < data.length; i += 4) {
          histR[data[i]]++;
          histG[data[i + 1]]++;
          histB[data[i + 2]]++;
        }
        const cdf = (hist) => {
          const out = new Array(256);
          let c = 0;
          for (let i = 0; i < 256; i++) {
            c += hist[i];
            out[i] = Math.round((c / (data.length / 4)) * 255);
          }
          return out;
        };
        const mapR = cdf(histR);
        const mapG = cdf(histG);
        const mapB = cdf(histB);
        for (let i = 0; i < data.length; i += 4) {
          data[i] = mapR[data[i]];
          data[i + 1] = mapG[data[i + 1]];
          data[i + 2] = mapB[data[i + 2]];
        }
      }

      if (segmentationRGB) {
        for (let i = 0; i < data.length; i += 4) {
          const r = data[i],
            g = data[i + 1],
            b = data[i + 2];
          const maxc = Math.max(r, g, b);
          if (maxc === r && r > threshold) {
            data[i] = 255;
            data[i + 1] = 0;
            data[i + 2] = 0;
          } else if (maxc === g && g > threshold) {
            data[i] = 0;
            data[i + 1] = 255;
            data[i + 2] = 0;
          } else if (maxc === b && b > threshold) {
            data[i] = 0;
            data[i + 1] = 0;
            data[i + 2] = 255;
          }
        }
      } else if (threshold !== 128 || grayscale) {
        for (let i = 0; i < data.length; i += 4) {
          const lum = 0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2];
          const val = lum >= threshold ? 255 : 0;
          if (grayscale || threshold !== 128) {
            data[i] = data[i + 1] = data[i + 2] = val;
          }
        }
      }

      pCtx.putImageData(imgData, 0, 0);
    }
  }, [
    imageSrc,
    grayscale,
    threshold,
    blur,
    resizePercent,
    rotation,
    flipH,
    flipV,
    normalize,
    equalize,
    segmentationRGB,
  ]);

  // load selected image into originalImgRef when imageSrc changes
  useEffect(() => {
    if (!imageSrc) return;
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => {
      originalImgRef.current = img;
      redrawCanvases();
    };
    img.src = imageSrc;
  }, [imageSrc, redrawCanvases]);

  // redraw whenever params change
  useEffect(() => {
    redrawCanvases();
  }, [grayscale, threshold, blur, resizePercent, rotation, flipH, flipV, normalize, equalize, segmentationRGB, redrawCanvases]);

  // split dragging
  useEffect(() => {
    const onMove = (e) => {
      if (!splitRef.current) return;
      const container = document.getElementById("pv-container");
      if (!container) return;
      const rect = container.getBoundingClientRect();
      const fraction = Math.min(1, Math.max(0, (e.clientX - rect.left) / rect.width));
      setSplit(fraction);
    };
    const onUp = () => {
      splitRef.current = false;
    };
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
    };
  }, []);

  // zoom handlers
  const handleZoomIn = () => setZoom((z) => Math.min(4, +(z + 0.25).toFixed(2)));
  const handleZoomOut = () => setZoom((z) => Math.max(0.25, +(z - 0.25).toFixed(2)));
  const handleWheel = (e) => {
    if (e.ctrlKey) {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      setZoom((z) => Math.max(0.25, Math.min(4, +(z + delta).toFixed(2))));
    }
  };

  // pan handlers
  const onPanMouseDown = (e) => {
    isPanningRef.current = true;
    panStartRef.current = { x: e.clientX - pan.x, y: e.clientY - pan.y };
  };
  const onPanMouseMove = (e) => {
    if (!isPanningRef.current) return;
    setPan({ x: e.clientX - panStartRef.current.x, y: e.clientY - panStartRef.current.y });
  };
  const onPanMouseUp = () => {
    isPanningRef.current = false;
  };
  useEffect(() => {
    window.addEventListener("mousemove", onPanMouseMove);
    window.addEventListener("mouseup", onPanMouseUp);
    return () => {
      window.removeEventListener("mousemove", onPanMouseMove);
      window.removeEventListener("mouseup", onPanMouseUp);
    };
  });

  // ROI handlers
  const onRoiMouseDown = (e) => {
    if (e.button !== 0) return;
    const el = processedCanvasRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    roiDragRef.current = true;
    roiStartRef.current = { x, y };
  };
  const onRoiMouseMove = (e) => {
    if (!roiDragRef.current) return;
    const el = processedCanvasRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const sx = roiStartRef.current.x;
    const sy = roiStartRef.current.y;
    const rx = Math.min(sx, x);
    const ry = Math.min(sy, y);
    const rw = Math.abs(x - sx);
    const rh = Math.abs(y - sy);
    setRoi({ x: rx, y: ry, w: rw, h: rh });
  };
  const onRoiMouseUp = () => {
    if (!roiDragRef.current) return;
    roiDragRef.current = false;
    pushStateToUndo();
    commitChange("ROI sélectionné");
  };

  // File upload inside Processing (adds image to store and selects it)
  const handleFile = (file) => {
    if (!file) return;
    const allowed = ["image/png", "image/jpeg", "image/jpg", "image/bmp", "image/svg+xml"];
    if (!allowed.includes(file.type)) {
      alert("Format non supporté. Utilisez JPG/PNG/BMP/SVG.");
      return;
    }
    const reader = new FileReader();
    reader.onload = (ev) => {
      const durl = ev.target.result;
      // add to store and select new image
      addImages([{ dataUrl: durl, name: file.name }]);
      // select last added
      const idx = useImageStore.getState().images.length - 1;
      if (idx >= 0) {
        setSelectedImage(idx);
        // initial history entry will be created by addImages if implemented that way,
        // otherwise add a simple history entry:
        addHistory(idx, "Image importée", durl);
      }
      // local sync
      setImageSrc(durl);
    };
    reader.readAsDataURL(file);
  };

  const onDrop = (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files && e.dataTransfer.files[0];
    handleFile(f);
  };
  const onDragOver = (e) => {
    e.preventDefault();
  };

  // Download processed image
  const handleDownload = () => {
    const canvas = processedCanvasRef.current;
    if (!canvas) return;
    const link = document.createElement("a");
    link.download = "processed.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
  };

  const resetView = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };
  const handleAction = async (actionType) => {
  const newImage = await applyAction(imageSrc, actionType);
  setImageSrc(newImage);
  addHistogram(actionType, newImage); // ici addHistogram doit être awaité si tu veux garantir la mise à jour
};
const getTraitementName = () => {
  const names = [];
  if (grayscale) names.push("Grayscale");
  if (equalize) names.push("Égalisation");
  if (normalize) names.push("Normalisation");
  if (segmentationRGB) names.push("Segmentation RGB");
  if (threshold !== 128) names.push(`Seuillage ${threshold}`);
  if (blur > 0) names.push(`Flou ${blur}px`);
  if (resizePercent !== 100) names.push(`Redimensionnement ${resizePercent}%`);
  if (rotation !== 0) names.push(`Rotation ${rotation}°`);
  if (flipH) names.push("Flip H");
  if (flipV) names.push("Flip V");
  return names.length > 0 ? names.join(" + ") : "Original";
};
  // UI
  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Grid container spacing={3}>
        {/* Left: Viewer */}
        <Grid item xs={12} md={8}>
          <Paper
            id="pv-container"
            onDrop={onDrop}
            onDragOver={onDragOver}
            sx={{
              height: "78vh",
              minHeight: 540,
              position: "relative",
              overflow: "hidden",
              borderRadius: 2,
              p: 0,
            }}
            elevation={3}
          >
            {/* Controls overlay */}
            <Box sx={{ position: "absolute", right: 12, top: 12, zIndex: 20 }}>
              <Stack direction="row" spacing={1}>
                <Tooltip title="Zoom out">
                  <IconButton onClick={() => setZoom((z) => Math.max(0.25, +(z - 0.25).toFixed(2)))} size="small"><ZoomOutIcon /></IconButton>
                </Tooltip>
                <Tooltip title="Zoom in">
                  <IconButton onClick={() => setZoom((z) => Math.min(4, +(z + 0.25).toFixed(2)))} size="small"><ZoomInIcon /></IconButton>
                </Tooltip>
                <Tooltip title="Reset view">
                  <IconButton onClick={resetView} size="small"><OpenInFullIcon /></IconButton>
                </Tooltip>
                <Divider orientation="vertical" flexItem sx={{ mx: 0.5 }} />
                <Tooltip title="Undo">
                  <span>
                    <IconButton onClick={handleUndo} size="small"><UndoIcon /></IconButton>
                  </span>
                </Tooltip>
                <Tooltip title="Redo">
                  <IconButton onClick={handleRedo} size="small"><RedoIcon /></IconButton>
                </Tooltip>
                <Tooltip title="Reset settings">
                  <IconButton onClick={handleReset} size="small"><RefreshIcon /></IconButton>
                </Tooltip>
                <Tooltip title="Download processed image">
                  <IconButton onClick={handleDownload} size="small"><DownloadIcon /></IconButton>
                </Tooltip>
              </Stack>
            </Box>

            {/* Viewer content */}
            <Box sx={{ width: "100%", height: "100%", position: "relative", background: "linear-gradient(180deg, #fff 0%, #f8fafc 100%)" }} onWheel={handleWheel}>
              <div
                style={{
                  transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
                  transformOrigin: "0 0",
                  width: "max-content",
                  height: "max-content",
                  position: "absolute",
                  left: 0,
                  top: 0,
                  cursor: isPanningRef.current ? "grabbing" : "grab",
                }}
                onMouseDown={onPanMouseDown}
              >
                {/* Original canvas */}
                <div style={{ display: "inline-block", verticalAlign: "top" }}>
                  <Typography variant="caption" sx={{ ml: 2 }}>Original</Typography>
                  <canvas ref={originalCanvasRef} style={{ display: "block", margin: 8, background: "#fff", borderRadius: 8, boxShadow: "0 4px 12px rgba(0,0,0,0.06)" }} />
                </div>

                {/* Processed canvas */}
                <div style={{ display: "inline-block", verticalAlign: "top", position: "relative" }}>
                  <Typography variant="caption" sx={{ ml: 2 }}>Traité</Typography>
                  <div style={{ position: "relative", display: "inline-block" }}>
                    <canvas
                      ref={processedCanvasRef}
                      onMouseDown={onRoiMouseDown}
                      onMouseMove={onRoiMouseMove}
                      onMouseUp={onRoiMouseUp}
                      style={{ display: "block", margin: 8, background: "#fff", borderRadius: 8, boxShadow: "0 4px 12px rgba(0,0,0,0.06)", userSelect: "none" }}
                    />
                    {roi && <div style={{ position: "absolute", left: `${roi.x}px`, top: `${roi.y}px`, width: `${roi.w}px`, height: `${roi.h}px`, border: "2px dashed rgba(255,165,0,0.95)", background: "rgba(255,165,0,0.08)", pointerEvents: "none" }} />}
                  </div>
                </div>
              </div>

              {/* Split handle */}
              <div onMouseDown={() => (splitRef.current = true)} style={{ position: "absolute", left: `${split * 100}%`, top: 0, bottom: 0, width: 8, marginLeft: -4, cursor: "ew-resize", zIndex: 30 }}>
                <div style={{ position: "absolute", top: "50%", left: 0, transform: "translateY(-50%)", width: 8, height: 50, borderRadius: 4, background: "rgba(0,0,0,0.07)" }} />
              </div>
            </Box>
          </Paper>

          {/* hint bar */}
          <Box sx={{ mt: 2, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <Typography variant="body2" color="text.secondary">Glisser-déposer une image ici ou utiliser le upload (à droite). Zoom avec Ctrl + molette.</Typography>
            <Stack direction="row" spacing={1} alignItems="center">
              <ImageIcon fontSize="small" />
              <Typography variant="body2" color="text.secondary">{imageSrc ? "Image chargée" : "Aucune image"}</Typography>
            </Stack>
          </Box>
        </Grid>

        {/* Right: Controls */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, borderRadius: 2 }} elevation={3}>
            <Typography variant="h6" gutterBottom>Prétraitement</Typography>

            <Stack spacing={2}>
              {/* File upload */}
              <div>
                <label htmlFor="file-input" style={{ display: "inline-block" }}>
                  <input id="file-input" type="file" accept="image/*" style={{ display: "none" }} onChange={(e) => {
                    const f = e.target.files && e.target.files[0];
                    handleFile(f);
                  }} />
                  <Button variant="outlined" component="span" fullWidth>Upload image</Button>
                </label>
              </div>

              <Divider />

              {/* Grayscale toggle */}
              <div>
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                  <Typography variant="subtitle2">Grayscale</Typography>
                  <Button size="small" variant={grayscale ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setGrayscale((g) => { const next = !g; commitChange(next ? "Activer grayscale" : "Désactiver grayscale"); return next; }); }}>
                    {grayscale ? "On" : "Off"}
                  </Button>
                </Stack>
              </div>

              {/* Threshold */}
              <div>
                <Typography variant="subtitle2">Seuillage (Threshold)</Typography>
                <Slider
                  value={threshold}
                  min={0}
                  max={255}
                  onChange={(e, v) => setThreshold(v)}
                  onChangeCommitted={(e, v) => { pushStateToUndo(); commitChange(`Seuillage ${v}`); }}
                  valueLabelDisplay="auto"
                />
              </div>

              {/* Blur */}
              <div>
                <Typography variant="subtitle2">Flou (px)</Typography>
                <Slider
                  value={blur}
                  min={0}
                  max={20}
                  onChange={(e, v) => setBlur(v)}
                  onChangeCommitted={(e, v) => { pushStateToUndo(); commitChange(`Flou ${v}px`); }}
                  valueLabelDisplay="auto"
                />
              </div>

              {/* Resize */}
              <div>
                <Typography variant="subtitle2">Redimensionnement (%)</Typography>
                <Slider
                  value={resizePercent}
                  min={10}
                  max={200}
                  onChange={(e, v) => setResizePercent(v)}
                  onChangeCommitted={(e, v) => { pushStateToUndo(); commitChange(`Redimensionnement ${v}%`); }}
                  valueLabelDisplay="auto"
                />
              </div>

              {/* Rotation */}
              <div>
                <Typography variant="subtitle2">Rotation (°)</Typography>
                <Stack direction="row" spacing={1} alignItems="center">
                  <Button size="small" variant="outlined" onClick={() => { pushStateToUndo(); setRotation((r) => { const next = (r - 90) % 360; commitChange("Rotation -90°"); return next; }); }}>⟲</Button>
                  <Button size="small" variant="outlined" onClick={() => { pushStateToUndo(); setRotation((r) => { const next = (r + 90) % 360; commitChange("Rotation +90°"); return next; }); }}>⟳</Button>
                  <Typography sx={{ ml: 1 }}>{rotation}°</Typography>
                </Stack>
                <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                  <Button size="small" variant={flipH ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setFlipH((v) => { const next = !v; commitChange(next ? "Flip H on" : "Flip H off"); return next; }); }}>Flip H</Button>
                  <Button size="small" variant={flipV ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setFlipV((v) => { const next = !v; commitChange(next ? "Flip V on" : "Flip V off"); return next; }); }}>Flip V</Button>
                </Stack>
              </div>

              {/* Normalization / equalize / segmentation */}
              <div>
                <Stack direction="column" spacing={1}>
                  <Stack direction="row" justifyContent="space-between">
                    <Typography variant="subtitle2">Normalisation</Typography>
                    <Button size="small" variant={normalize ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setNormalize((s) => { const next = !s; commitChange(next ? "Normalisation On" : "Normalisation Off"); return next; }); }}>
                      {normalize ? "On" : "Off"}
                    </Button>
                  </Stack>
                  <Stack direction="row" justifyContent="space-between">
                    <Typography variant="subtitle2">Égalisation hist.</Typography>
                    <Button size="small" variant={equalize ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setEqualize((s) => { const next = !s; commitChange(next ? "Égalisation On" : "Égalisation Off"); return next; }); }}>
                      {equalize ? "On" : "Off"}
                    </Button>
                  </Stack>
                  <Stack direction="row" justifyContent="space-between">
                    <Typography variant="subtitle2">Segmentation RGB</Typography>
                    <Button size="small" variant={segmentationRGB ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setSegmentationRGB((s) => { const next = !s; commitChange(next ? "Segmentation RGB On" : "Segmentation RGB Off"); return next; }); }}>
                      {segmentationRGB ? "On" : "Off"}
                    </Button>
                  </Stack>
                </Stack>
              </div>

              {/* ROI selection */}
              <div>
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                  <Typography variant="subtitle2">ROI (glisser sur l'image)</Typography>
                  <Button size="small" variant={roi ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setRoi(null); commitChange("ROI cleared"); }}>
                    Clear
                  </Button>
                </Stack>
                <Typography variant="caption" color="text.secondary">Cliquer & glisser dans la zone "Traité" pour dessiner un rectangle.</Typography>
              </div>

              <Divider />

              {/* Undo / Redo / Reset / Download */}
              <Stack direction="row" spacing={1} justifyContent="space-between" sx={{ mt: 1 }}>
                <Button startIcon={<UndoIcon />} onClick={handleUndo}>Undo</Button>
                <Button startIcon={<RedoIcon />} onClick={handleRedo}>Redo</Button>
                <Button startIcon={<RefreshIcon />} onClick={() => { handleReset(); commitChange("Reset paramètres"); }}>Reset</Button>
              </Stack>

              <Button startIcon={<DownloadIcon />} variant="contained" onClick={handleDownload} sx={{ mt: 1 }}>
                Télécharger
              </Button>
            </Stack>
          </Paper>

          {/* Histogram button: just navigates and passes processed image */}
          <Button
  variant="contained"
  color="primary"
  sx={{ mt: 2 }}
  onClick={async () => {
    const canvas = processedCanvasRef.current;
    if (!canvas) {
      alert("Veuillez charger une image avant d'afficher l'histogramme.");
      return;
    }

    const imageSrc = canvas.toDataURL("image/png");
    const traitementName = getTraitementName(); // <-- nom du traitement actif

    await addHistogram(traitementName, imageSrc);

    navigate("/histogram");
  }}
>
  Voir Histogramme
</Button>

          <button onClick={() => navigate("/historique")}>
        Voir l'historique
      </button>
        </Grid>
      </Grid>
    </Container>
  );
}
