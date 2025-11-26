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
  Select,
  MenuItem,
  FormControl,
  InputLabel,
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
import CropSquareIcon from "@mui/icons-material/CropSquare";
import ImageIcon from "@mui/icons-material/Image";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";
import { useImageStore } from "../../store/useImageStore";

export default function ProcessingWorkspace() {
  // Refs to canvases
  const originalCanvasRef = useRef(null);
  const processedCanvasRef = useRef(null);
  const originalImgRef = useRef(null);

  // Split view state (0..1 fraction)
  const [split, setSplit] = useState(0.5);
  const splitRef = useRef(false);

  // Zoom & pan
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const isPanningRef = useRef(false);
  const panStartRef = useRef({ x: 0, y: 0 });

  // Processing parameters (UI)
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

  // ROI selection (in canvas coords)
  const [roi, setRoi] = useState(null); // {x,y,w,h}
  const roiDragRef = useRef(false);
  const roiStartRef = useRef(null);

  // Undo/Redo stacks for settings & ROI
  const undoStackRef = useRef([]);
  const redoStackRef = useRef([]);

  // Helper: push current state into undo
  const pushStateToUndo = useCallback(() => {
    const state = {
      grayscale, threshold, blur, resizePercent, rotation, flipH, flipV,
      normalize, equalize, segmentationRGB,
      roi,
    };
    undoStackRef.current.push(JSON.stringify(state));
    // limit stack size
    if (undoStackRef.current.length > 50) undoStackRef.current.shift();
    // clear redo stack on new action
    redoStackRef.current = [];
  }, [grayscale, threshold, blur, resizePercent, rotation, flipH, flipV, normalize, equalize, segmentationRGB, roi]);

  // Undo/Redo handlers
  const handleUndo = () => {
    const u = undoStackRef.current;
    if (u.length === 0) return;
    const last = u.pop();
    redoStackRef.current.push(JSON.stringify({
      grayscale, threshold, blur, resizePercent, rotation, flipH, flipV,
      normalize, equalize, segmentationRGB,
      roi,
    }));
    const st = JSON.parse(last);
    applyStateFromObject(st, false);
  };

  const handleRedo = () => {
    const r = redoStackRef.current;
    if (r.length === 0) return;
    const last = r.pop();
    undoStackRef.current.push(JSON.stringify({
      grayscale, threshold, blur, resizePercent, rotation, flipH, flipV,
      normalize, equalize, segmentationRGB,
      roi,
    }));
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

  // Reset
  const handleReset = () => {
    pushStateToUndo();
    applyStateFromObject({
      grayscale: false, threshold: 128, blur: 0, resizePercent: 100, rotation: 0,
      flipH: false, flipV: false, normalize: false, equalize: false, segmentationRGB: false, roi: null
    }, false);
  };

 // Récupération du store
const { images, selectedImage } = useImageStore();

// image sélectionnée
const imageSrc = selectedImage !== null ? images[selectedImage]?.dataUrl : null;


  // Draw original image to original canvas, and apply lightweight processing to processed canvas
  const redrawCanvases = useCallback(() => {
    const img = originalImgRef.current;
    const origCanvas = originalCanvasRef.current;
    const procCanvas = processedCanvasRef.current;
    if (!img || !origCanvas || !procCanvas) return;

    const oCtx = origCanvas.getContext("2d");
    const pCtx = procCanvas.getContext("2d");

    // compute target size based on resizePercent
    const baseW = img.width;
    const baseH = img.height;
    const scale = resizePercent / 100;
    const w = Math.max(1, Math.round(baseW * scale));
    const h = Math.max(1, Math.round(baseH * scale));

    // set canvas sizes (also preserve display scale for crispness)
    const dpr = window.devicePixelRatio || 1;
    origCanvas.width = img.width * dpr;
    origCanvas.height = img.height * dpr;
    origCanvas.style.width = `${img.width}px`;
    origCanvas.style.height = `${img.height}px`;

    procCanvas.width = w * dpr;
    procCanvas.height = h * dpr;
    procCanvas.style.width = `${w}px`;
    procCanvas.style.height = `${h}px`;

    // Draw original (scaled by DPR)
    oCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    oCtx.clearRect(0, 0, img.width, img.height);
    oCtx.drawImage(img, 0, 0, img.width, img.height);

    // Prepare processed canvas context filters (simple preview using ctx.filter)
    // Note: ctx.filter supports blur and grayscale in modern browsers.
    // Compose filters:
    const filters = [];
    if (blur > 0) filters.push(`blur(${blur}px)`);
    if (grayscale) filters.push("grayscale(1)");
    // rotation/flip applied via transform when drawing image
    pCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    pCtx.clearRect(0, 0, w, h);

    // set filter if supported
    try {
      pCtx.filter = filters.join(" ") || "none";
    } catch (e) {
      // ignore if not supported
      pCtx.filter = "none";
    }

    // draw image onto proc canvas with resize, rotation & flip
    pCtx.save();
    // translate to center if we want to rotate around center
    if (rotation !== 0 || flipH || flipV) {
      pCtx.translate(w / 2, h / 2);
      pCtx.rotate((rotation * Math.PI) / 180);
      pCtx.scale(flipH ? -1 : 1, flipV ? -1 : 1);
      pCtx.drawImage(img, -w / 2, -h / 2, w, h);
    } else {
      pCtx.drawImage(img, 0, 0, w, h);
    }
    pCtx.restore();

    // Simple threshold implementation (pixel-level) if threshold != 128 or segmentationRGB
    if (threshold !== 128 || segmentationRGB || normalize || equalize) {
      // do pixel-level manipulations (slow for large images; OK for UI demo)
      const imgData = pCtx.getImageData(0, 0, procCanvas.width, procCanvas.height);
      const data = imgData.data;
      // normalize: map min-max to 0-255
      if (normalize) {
        let min = 255, max = 0;
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
      // simplistic histogram equalization (per channel)
      if (equalize) {
        // compute hist for each channel
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
      // threshold or segmentationRGB
      if (segmentationRGB) {
        // naive: highlight red channel regions above threshold
        for (let i = 0; i < data.length; i += 4) {
          const r = data[i], g = data[i + 1], b = data[i + 2];
          const maxc = Math.max(r, g, b);
          // colorize based on dominant channel
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
  }, [imageSrc, grayscale, threshold, blur, resizePercent, rotation, flipH, flipV, normalize, equalize, segmentationRGB]);

  // When imageSrc or parameters change, load image and redraw
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


  // Also redraw whenever processing params change (debounce not implemented for brevity)
  useEffect(() => {
    redrawCanvases();
  }, [grayscale, threshold, blur, resizePercent, rotation, flipH, flipV, normalize, equalize, segmentationRGB, redrawCanvases]);

  // Dragging split handler (mouse events on overlay)
  useEffect(() => {
    const onMove = (e) => {
      if (!splitRef.current) return;
      const container = document.getElementById("pv-container");
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

  // Zoom handlers
  const handleZoomIn = () => setZoom((z) => Math.min(4, +(z + 0.25).toFixed(2)));
  const handleZoomOut = () => setZoom((z) => Math.max(0.25, +(z - 0.25).toFixed(2)));
  const handleWheel = (e) => {
    if (e.ctrlKey) {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      setZoom((z) => Math.max(0.25, Math.min(4, +(z + delta).toFixed(2))));
    }
  };

  // Pan handlers on viewer wrapper
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

  // ROI mouse handlers (on processed canvas). Coordinates are in displayed pixels; convert to canvas coordinates when storing.
  const onRoiMouseDown = (e) => {
    // only left click
    if (e.button !== 0) return;
    const el = processedCanvasRef.current;
    const rect = el.getBoundingClientRect();
    const x = (e.clientX - rect.left);
    const y = (e.clientY - rect.top);
    roiDragRef.current = true;
    roiStartRef.current = { x, y };
  };
  const onRoiMouseMove = (e) => {
    if (!roiDragRef.current) return;
    const el = processedCanvasRef.current;
    const rect = el.getBoundingClientRect();
    const x = (e.clientX - rect.left);
    const y = (e.clientY - rect.top);
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
    // push to undo history
    pushStateToUndo();
  };

  // File upload handler (drag-drop and input)
  const handleFile = (file) => {
    if (!file) return;
    const allowed = ["image/png", "image/jpeg", "image/jpg", "image/bmp", "image/svg+xml"];
    if (!allowed.includes(file.type)) {
      alert("Format non supporté. Utilisez JPG/PNG/BMP/SVG.");
      return;
    }
    const reader = new FileReader();
    reader.onload = (ev) => {
      setImageSrc(ev.target.result);
      pushStateToUndo();
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

  // Download processed canvas
  const handleDownload = () => {
    const canvas = processedCanvasRef.current;
    if (!canvas) return;
    const link = document.createElement("a");
    link.download = "processed.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
  };

  // Reset view transforms
  const resetView = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  // UI layout
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
            {/* Controls overlay top-right */}
            <Box sx={{ position: "absolute", right: 12, top: 12, zIndex: 20 }}>
              <Stack direction="row" spacing={1}>
                <Tooltip title="Zoom out">
                  <IconButton onClick={handleZoomOut} size="small"><ZoomOutIcon /></IconButton>
                </Tooltip>
                <Tooltip title="Zoom in">
                  <IconButton onClick={handleZoomIn} size="small"><ZoomInIcon /></IconButton>
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

            {/* Viewer content: two canvases side-by-side in split view */}
            <Box
              sx={{
                width: "100%",
                height: "100%",
                position: "relative",
                background: "linear-gradient(180deg, #fff 0%, #f8fafc 100%)"
              }}
              onWheel={handleWheel}
            >
              {/* transform wrapper for zoom & pan */}
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
                  <canvas
                    ref={originalCanvasRef}
                    style={{
                      display: "block",
                      margin: 8,
                      background: "#fff",
                      borderRadius: 8,
                      boxShadow: "0 4px 12px rgba(0,0,0,0.06)"
                    }}
                  />
                </div>

                {/* Processed canvas with cropping overlay sized according to split */}
                <div style={{ display: "inline-block", verticalAlign: "top", position: "relative" }}>
                  <Typography variant="caption" sx={{ ml: 2 }}>Traité</Typography>
                  <div style={{ position: "relative", display: "inline-block" }}>
                    <canvas
                      ref={processedCanvasRef}
                      onMouseDown={onRoiMouseDown}
                      onMouseMove={onRoiMouseMove}
                      onMouseUp={onRoiMouseUp}
                      style={{
                        display: "block",
                        margin: 8,
                        background: "#fff",
                        borderRadius: 8,
                        boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
                        userSelect: "none",
                      }}
                    />
                    {/* ROI overlay */}
                    {roi && (
                      <div
                        style={{
                          position: "absolute",
                          left: `${roi.x}px`,
                          top: `${roi.y}px`,
                          width: `${roi.w}px`,
                          height: `${roi.h}px`,
                          border: "2px dashed rgba(255,165,0,0.95)",
                          background: "rgba(255,165,0,0.08)",
                          pointerEvents: "none",
                        }}
                      />
                    )}
                  </div>
                </div>
              </div>

              {/* Split handle overlay (draggable) */}
              <div
                onMouseDown={() => (splitRef.current = true)}
                style={{
                  position: "absolute",
                  left: `${split * 100}%`,
                  top: 0,
                  bottom: 0,
                  width: 8,
                  marginLeft: -4,
                  cursor: "ew-resize",
                  zIndex: 30,
                }}
              >
                <div style={{
                  position: "absolute",
                  top: "50%",
                  left: 0,
                  transform: "translateY(-50%)",
                  width: 8,
                  height: 50,
                  borderRadius: 4,
                  background: "rgba(0,0,0,0.07)"
                }} />
              </div>
            </Box>
          </Paper>

          {/* small hint bar below viewer */}
          <Box sx={{ mt: 2, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <Typography variant="body2" color="text.secondary">
              Glisser-déposer une image ici ou utiliser le upload (à droite). Zoom avec Ctrl + molette.
            </Typography>
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
                  <input
                    id="file-input"
                    type="file"
                    accept="image/*"
                    style={{ display: "none" }}
                    onChange={(e) => {
                      const f = e.target.files && e.target.files[0];
                      handleFile(f);
                    }}
                  />
                  <Button variant="outlined" component="span" fullWidth>Upload image</Button>
                </label>
              </div>

              <Divider />

              {/* Grayscale */}
              <div>
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                  <Typography variant="subtitle2">Grayscale</Typography>
                  <Button size="small" variant={grayscale ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setGrayscale(!grayscale); }}>
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
                  onChangeCommitted={() => pushStateToUndo()}
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
                  onChangeCommitted={() => pushStateToUndo()}
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
                  onChangeCommitted={() => pushStateToUndo()}
                  valueLabelDisplay="auto"
                />
              </div>

              {/* Rotation */}
              <div>
                <Typography variant="subtitle2">Rotation (°)</Typography>
                <Stack direction="row" spacing={1} alignItems="center">
                  <Button size="small" variant="outlined" onClick={() => { pushStateToUndo(); setRotation((r) => (r - 90) % 360); }}>⟲</Button>
                  <Button size="small" variant="outlined" onClick={() => { pushStateToUndo(); setRotation((r) => (r + 90) % 360); }}>⟳</Button>
                  <Typography sx={{ ml: 1 }}>{rotation}°</Typography>
                </Stack>
                <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                  <Button size="small" variant={flipH ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setFlipH((v) => !v); }}>Flip H</Button>
                  <Button size="small" variant={flipV ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setFlipV((v) => !v); }}>Flip V</Button>
                </Stack>
              </div>

              {/* Normalization / equalize / segmentation */}
              <div>
                <Stack direction="column" spacing={1}>
                  <Stack direction="row" justifyContent="space-between">
                    <Typography variant="subtitle2">Normalisation</Typography>
                    <Button size="small" variant={normalize ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setNormalize((s) => !s); }}>
                      {normalize ? "On" : "Off"}
                    </Button>
                  </Stack>
                  <Stack direction="row" justifyContent="space-between">
                    <Typography variant="subtitle2">Égalisation hist.</Typography>
                    <Button size="small" variant={equalize ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setEqualize((s) => !s); }}>
                      {equalize ? "On" : "Off"}
                    </Button>
                  </Stack>
                  <Stack direction="row" justifyContent="space-between">
                    <Typography variant="subtitle2">Segmentation RGB</Typography>
                    <Button size="small" variant={segmentationRGB ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setSegmentationRGB((s) => !s); }}>
                      {segmentationRGB ? "On" : "Off"}
                    </Button>
                  </Stack>
                </Stack>
              </div>

              {/* ROI selection */}
              <div>
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                  <Typography variant="subtitle2">ROI (glisser sur l'image)</Typography>
                  <Button size="small" variant={roi ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setRoi(null); }}>
                    Clear
                  </Button>
                </Stack>
                <Typography variant="caption" color="text.secondary">Cliquer & glisser dans la zone "Traité" pour dessiner un rectangle.</Typography>
              </div>

              <Divider />

              {/* Undo / Redo / Reset / Download buttons */}
              <Stack direction="row" spacing={1} justifyContent="space-between" sx={{ mt: 1 }}>
                <Button startIcon={<UndoIcon />} onClick={handleUndo}>Undo</Button>
                <Button startIcon={<RedoIcon />} onClick={handleRedo}>Redo</Button>
                <Button startIcon={<RefreshIcon />} onClick={handleReset}>Reset</Button>
              </Stack>

              <Button startIcon={<DownloadIcon />} variant="contained" onClick={handleDownload} sx={{ mt: 1 }}>
                Télécharger
              </Button>
            </Stack>
          </Paper>

          {/* Histogram / Analysis panel (placeholder) */}
          <Paper sx={{ mt: 2, p: 2, borderRadius: 2 }} elevation={2}>
            <Typography variant="subtitle1">Histogrammes & Analyse</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Histogramme interactif et analyse de région (bientôt). Ici on affichera les histogrammes par canal et le profil d'intensité.
            </Typography>
            <Box sx={{ mt: 2, height: 120, borderRadius: 1, background: "linear-gradient(90deg,#fff,#f7f7f9)", border: "1px solid #eee" }} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
