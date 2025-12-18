// src/views/pages/ProcessingWorkspaceClean.jsx
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

const BACKEND_URL = "http://localhost:5000/api"; 

export default function ProcessingWorkspaceClean() {
  const navigate = useNavigate();
  const { images, selectedImage, addHistory, addImages, setSelectedImage } = useImageStore();
  const { addHistogram } = useHistogramStore();
  const [histStretch, setHistStretch] = useState(false);

  const [roiMode, setRoiMode] = useState(false);



  const originalCanvasRef = useRef(null);
  const processedCanvasRef = useRef(null);
  const originalImgRef = useRef(null);

  // Zoom & Pan
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const isPanningRef = useRef(false);
  const panStartRef = useRef({ x: 0, y: 0 });

  // Params
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
  const [roi, setRoi] = useState(null);
  const roiDragRef = useRef(false);
  const roiStartRef = useRef(null);

  // Undo / redo stacks
  const undoStackRef = useRef([]);
  const redoStackRef = useRef([]);

  const [imageSrc, setImageSrc] = useState(
    selectedImage !== null ? images[selectedImage]?.dataUrl : null
  );

  useEffect(() => {
    const src = selectedImage !== null ? images[selectedImage]?.dataUrl : null;
    setImageSrc(src || null);
  }, [selectedImage, images]);

  // -------------------- Backend save --------------------
  const saveToBackend = async (imgBase64, actionName = "frontend") => {
    try {
      const blob = await (await fetch(imgBase64)).blob();
      const formData = new FormData();
      const name = selectedImage !== null ? images[selectedImage]?.name || "image.png" : "image.png";
      formData.append("files", new File([blob], name));
      const res = await fetch(`${BACKEND_URL}/upload`, { method: "POST", body: formData });
      if (!res.ok) console.warn("Erreur backend:", res.statusText);
    } catch (err) {
      console.error("Erreur sauvegarde backend:", err);
    }
  };

  // -------------------- Undo / Redo / Reset --------------------
  const pushStateToUndo = useCallback(() => {
    undoStackRef.current.push(JSON.stringify({
      grayscale, threshold, blur, resizePercent, rotation,
      flipH, flipV, normalize, equalize, segmentationRGB, roi,histStretch,

    }));
    if (undoStackRef.current.length > 50) undoStackRef.current.shift();
    redoStackRef.current = [];
  }, [grayscale, threshold, blur, resizePercent, rotation, flipH, flipV, normalize, equalize, segmentationRGB, roi,histStretch]);

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
    setHistStretch(st.histStretch ?? false);

  };

  const handleUndo = () => {
    const u = undoStackRef.current;
    if (!u.length) return;
    const last = u.pop();
    redoStackRef.current.push(JSON.stringify({
      grayscale, threshold, blur, resizePercent, rotation,
      flipH, flipV, normalize, equalize, segmentationRGB, roi,histStretch
    }));
    applyStateFromObject(JSON.parse(last), false);
  };

  const handleRedo = () => {
    const r = redoStackRef.current;
    if (!r.length) return;
    const last = r.pop();
    undoStackRef.current.push(JSON.stringify({
      grayscale, threshold, blur, resizePercent, rotation,
      flipH, flipV, normalize, equalize, segmentationRGB, roi,histStretch
    }));
    applyStateFromObject(JSON.parse(last), false);
  };

  const handleReset = () => {
    pushStateToUndo();
    applyStateFromObject({
      grayscale: false, threshold: 128, blur: 0, resizePercent: 100,
      rotation: 0, flipH: false, flipV: false, normalize: false,
      equalize: false, segmentationRGB: false, roi: null
    }, false);
  };

  // -------------------- Redraw canvas --------------------
  const redrawCanvases = useCallback(() => {
    const img = originalImgRef.current;
    const origCanvas = originalCanvasRef.current;
    const procCanvas = processedCanvasRef.current;
    if (!img || !origCanvas || !procCanvas) return;

    const oCtx = origCanvas.getContext("2d");
    const pCtx = procCanvas.getContext("2d",{ willReadFrequently: true });

    const baseW = img.width;
    const baseH = img.height;
    const scale = resizePercent / 100;
    const w = Math.max(1, Math.round(baseW * scale));
    const h = Math.max(1, Math.round(baseH * scale));
    const dpr = window.devicePixelRatio || 1;
    
    const isInROI = (i) => {
    if (!roi) return true;

    const px = (i / 4) % procCanvas.width;
    const py = Math.floor((i / 4) / procCanvas.width);

    return (
    px >= roi.x &&
    px <= roi.x + roi.w &&
    py >= roi.y &&
    py <= roi.y + roi.h
  );
  };
 
    origCanvas.width = baseW * dpr;
    origCanvas.height = baseH * dpr;
    origCanvas.style.width = `${baseW}px`;
    origCanvas.style.height = `${baseH}px`;

    procCanvas.width = w * dpr;
    procCanvas.height = h * dpr;
    procCanvas.style.width = `${w}px`;
    procCanvas.style.height = `${h}px`;

    oCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    oCtx.clearRect(0, 0, baseW, baseH);
    oCtx.drawImage(img, 0, 0, baseW, baseH);

    pCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    pCtx.clearRect(0, 0, w, h);

    const filters = [];
    if (blur > 0) filters.push(`blur(${blur}px)`);
    if (grayscale) filters.push("grayscale(1)");
    try { pCtx.filter = filters.join(" ") || "none"; } catch { pCtx.filter = "none"; }

    pCtx.save();
    pCtx.translate(w/2, h/2);
    pCtx.rotate((rotation * Math.PI)/180);
    pCtx.scale(flipH?-1:1, flipV?-1:1);
    pCtx.drawImage(img, -w/2, -h/2, w, h);
    pCtx.restore();

    const imgData = pCtx.getImageData(0,0,procCanvas.width,procCanvas.height);
    const data = imgData.data;
  const applyHistogramStretch = (imageData) => {
  const data = imageData.data;

  let minR = 255, minG = 255, minB = 255;
  let maxR = 0,   maxG = 0,   maxB = 0;

  // === min / max par canal (équivalent img[:,:,c].min()) ===
  for (let i = 0; i < data.length; i += 4) {
    minR = Math.min(minR, data[i]);
    minG = Math.min(minG, data[i + 1]);
    minB = Math.min(minB, data[i + 2]);

    maxR = Math.max(maxR, data[i]);
    maxG = Math.max(maxG, data[i + 1]);
    maxB = Math.max(maxB, data[i + 2]);
  }

  const rangeR = maxR - minR || 1;
  const rangeG = maxG - minG || 1;
  const rangeB = maxB - minB || 1;

  // === (img - min) * 255 / (max - min) ===
  for (let i = 0; i < data.length; i += 4) {
    data[i]     = Math.round((data[i]     - minR) * 255 / rangeR);
    data[i + 1] = Math.round((data[i + 1] - minG) * 255 / rangeG);
    data[i + 2] = Math.round((data[i + 2] - minB) * 255 / rangeB);
    // alpha (i+3) inchangé
  }
};


    // Pixel-level ops
    if (normalize) {
      
      let min=255,max=0;
      for(let i=0;i<data.length;i+=4)
        {  if (!isInROI(i)) continue;
          const lum=0.2126*data[i]+0.7152*data[i+1]+0.0722*data[i+2];
           if(lum<min)min=lum;
            if(lum>max)max=lum; }
      const range=max-min||1;
      for(let i=0;i<data.length;i+=4){
          if (!isInROI(i)) continue; 
        data[i]=((data[i]-min)*255)/range; data[i+1]=((data[i+1]-min)*255)/range;
         data[i+2]=((data[i+2]-min)*255)/range;}
    }
    if (histStretch) {applyHistogramStretch(data);}


   if (equalize) {
  const histR = new Array(256).fill(0), histG = new Array(256).fill(0), histB = new Array(256).fill(0);

  // Calcul histogramme uniquement dans la ROI
  for (let i = 0; i < data.length; i += 4) {
    if (!isInROI(i)) continue;
    histR[data[i]]++;
    histG[data[i + 1]]++;
    histB[data[i + 2]]++;
  }

  // CDF
  const cdf = (h) => {
    const out = [];
    let c = 0;
    const totalPixels = h.reduce((acc, v) => acc + v, 0); // total pixels dans la ROI
    for (let i = 0; i < 256; i++) {
      c += h[i];
      out[i] = Math.round((c / totalPixels) * 255);
    }
    return out;
  };

  const mapR = cdf(histR);
  const mapG = cdf(histG);
  const mapB = cdf(histB);

  // Appliquer égalisation uniquement dans la ROI
  for (let i = 0; i < data.length; i += 4) {
    if (!isInROI(i)) continue;
    data[i] = mapR[data[i]];
    data[i + 1] = mapG[data[i + 1]];
    data[i + 2] = mapB[data[i + 2]];
  }
}


    if (segmentationRGB) {
      for(let i=0;i<data.length;i+=4){
         if (!isInROI(i)) continue;
        const r=data[i],g=data[i+1],b=data[i+2], maxc=Math.max(r,g,b);
        if(maxc===r && r>threshold){data[i]=255;data[i+1]=0;data[i+2]=0;}
        else if(maxc===g && g>threshold){data[i]=0;data[i+1]=255;data[i+2]=0;}
        else if(maxc===b && b>threshold){data[i]=0;data[i+1]=0;data[i+2]=255;}
      }
    } else if(threshold!==128 || grayscale){
      for(let i=0;i<data.length;i+=4){
         if (!isInROI(i)) continue;
        const lum=0.2126*data[i]+0.7152*data[i+1]+0.0722*data[i+2];
        const val=lum>=threshold?255:0;
        if(grayscale || threshold!==128){ data[i]=data[i+1]=data[i+2]=val; }
      }
    }
    pCtx.putImageData(imgData,0,0);


const getCanvasCoords = (e, canvas) => {
  const rect = canvas.getBoundingClientRect();

  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;

  return {
    x: (e.clientX - rect.left) * scaleX,
    y: (e.clientY - rect.top) * scaleY
  };
};




    // Save processed image to backend
    saveToBackend(procCanvas.toDataURL());
  }, [imageSrc, grayscale, threshold, blur, resizePercent, rotation, flipH, flipV, normalize, equalize, segmentationRGB]);

  useEffect(() => {
    if (!imageSrc) return;
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => { originalImgRef.current = img; redrawCanvases(); };
    img.src = imageSrc;
  }, [imageSrc, redrawCanvases]);

  useEffect(() => { redrawCanvases(); }, [grayscale, threshold, blur, resizePercent, rotation, flipH, flipV, normalize, equalize, segmentationRGB, redrawCanvases,histStretch]);

  // -------------------- Pan / Zoom --------------------
  const onPanMouseDown = e => {
      if (roiMode) return;   
     isPanningRef.current=true; 
     panStartRef.current={x:e.clientX-pan.x, y:e.clientY-pan.y};
     };
  const onPanMouseMove = e => { if(!isPanningRef.current) return; setPan({x:e.clientX-panStartRef.current.x, y:e.clientY-panStartRef.current.y}); };
  const onPanMouseUp = () => { isPanningRef.current=false; };
  useEffect(()=>{ window.addEventListener("mousemove",onPanMouseMove); window.addEventListener("mouseup",onPanMouseUp); return ()=>{ window.removeEventListener("mousemove",onPanMouseMove); window.removeEventListener("mouseup",onPanMouseUp); }; });

  const handleWheel = e => { if(e.ctrlKey){ e.preventDefault(); const delta=e.deltaY>0?-0.1:0.1; setZoom(z=>Math.max(0.25,Math.min(4, +(z+delta).toFixed(2)))); } };
  const resetView = () => { setZoom(1); setPan({x:0,y:0}); };

  // -------------------- ROI --------------------
const onRoiMouseDown = e => {
  if (!roiMode) return;
  if (e.button !== 0) return;

  e.stopPropagation(); // 🔥 CRUCIAL

  const canvas = processedCanvasRef.current;
  if (!canvas) return;

  const rect = canvas.getBoundingClientRect();

  roiDragRef.current = true;
  roiStartRef.current = {
    x: (e.clientX - rect.left) * window.devicePixelRatio,
    y: (e.clientY - rect.top) * window.devicePixelRatio
  };

  setRoi({ x: roiStartRef.current.x, y: roiStartRef.current.y, w: 0, h: 0 });
};

const onRoiMouseMove = e => {
  if (!roiMode) return;
  if (!roiDragRef.current) return;

  e.stopPropagation();

  const canvas = processedCanvasRef.current;
  if (!canvas) return;

  const rect = canvas.getBoundingClientRect();

  const x = (e.clientX - rect.left) * window.devicePixelRatio;
  const y = (e.clientY - rect.top) * window.devicePixelRatio;

  const sx = roiStartRef.current.x;
  const sy = roiStartRef.current.y;

  setRoi({
    x: Math.min(sx, x),
    y: Math.min(sy, y),
    w: Math.abs(x - sx),
    h: Math.abs(y - sy)
  });
};

  const onRoiMouseUp = e => {
  if (!roiMode) return;
  if (!roiDragRef.current) return;

  e.stopPropagation();

  roiDragRef.current = false;
  pushStateToUndo();
};


  // -------------------- File upload --------------------
  const handleFile = file => {
    if(!file) return;
    const allowed=["image/png","image/jpeg","image/jpg","image/bmp","image/svg+xml"];
    if(!allowed.includes(file.type)){ alert("Format non supporté."); return; }
    const reader=new FileReader();
    reader.onload=ev=>{
      const durl=ev.target.result;
      addImages([{dataUrl:durl,name:file.name}]);
      const idx=useImageStore.getState().images.length-1;
      if(idx>=0){ setSelectedImage(idx); addHistory(idx,"Image importée",durl); }
      setImageSrc(durl);
    };
    reader.readAsDataURL(file);
  };
  const onDrop=e=>{ e.preventDefault(); const f=e.dataTransfer.files && e.dataTransfer.files[0]; handleFile(f); };
  const onDragOver=e=>{ e.preventDefault(); };

  // -------------------- Download --------------------
  const handleDownload = () => {
    const canvas = processedCanvasRef.current;
    if(!canvas) return;
    const link=document.createElement("a");
    link.download="processed.png";
    link.href=canvas.toDataURL("image/png");
    link.click();
  };

  // -------------------- Navigation to histogram --------------------
  const getTraitementName = () => {
    const names=[];
    if(grayscale) names.push("Grayscale");
    if(equalize) names.push("Égalisation");
    if(normalize) names.push("Normalisation");
    if (histStretch) names.push("Étirement histogramme");
    if(segmentationRGB) names.push("Segmentation RGB");
    if(threshold!==128) names.push(`Seuillage ${threshold}`);
    if(blur>0) names.push(`Flou ${blur}px`);
    if(resizePercent!==100) names.push(`Redimensionnement ${resizePercent}%`);
    if(rotation!==0) names.push(`Rotation ${rotation}°`);
    if(flipH) names.push("Flip H");
    if(flipV) names.push("Flip V");
    return names.length>0?names.join(" + "):"Original";
  };

  const goHistogram = async () => {
    const canvas = processedCanvasRef.current;
    if(!canvas){ alert("Chargez une image d'abord"); return; }
    const imgSrc = canvas.toDataURL("image/png");
    const traitementName = getTraitementName();
    await addHistogram(traitementName,imgSrc);
    navigate("/histogram");
  };

  // -------------------- UI --------------------
//   return (
//     <Container maxWidth="xl" sx={{ py:4 }}>
//       <Grid container spacing={3}>
//         {/* Left: Viewer */}
//         <Grid item xs={12} md={9}>
//           <Paper
//             id="pv-container"
//             onDrop={onDrop}
//             onDragOver={onDragOver}
//             sx={{ height:"78vh", minHeight:540, position:"relative", overflow:"hidden", borderRadius:2, p:0 }}
//             elevation={3}
//           >
//             <Box sx={{ position:"absolute", right:12, top:12, zIndex:20 }}>
//               <Stack direction="row" spacing={1}>
//                 <Tooltip title="Zoom out"><IconButton onClick={()=>setZoom(z=>Math.max(0.25,+(z-0.25).toFixed(2)))} size="small"><ZoomOutIcon/></IconButton></Tooltip>
//                 <Tooltip title="Zoom in"><IconButton onClick={()=>setZoom(z=>Math.min(4,+(z+0.25).toFixed(2)))} size="small"><ZoomInIcon/></IconButton></Tooltip>
//                 <Tooltip title="Reset view"><IconButton onClick={resetView} size="small"><OpenInFullIcon/></IconButton></Tooltip>
//                 <Divider orientation="vertical" flexItem sx={{mx:0.5}}/>
//                 <Tooltip title="Undo"><IconButton onClick={handleUndo} size="small"><UndoIcon/></IconButton></Tooltip>
//                 <Tooltip title="Redo"><IconButton onClick={handleRedo} size="small"><RedoIcon/></IconButton></Tooltip>
//                 <Tooltip title="Reset settings"><IconButton onClick={handleReset} size="small"><RefreshIcon/></IconButton></Tooltip>
//                 <Tooltip title="Download"><IconButton onClick={handleDownload} size="small"><DownloadIcon/></IconButton></Tooltip>
//               </Stack>
//             </Box>

//             <Box sx={{ width:"100%", height:"100%", position:"relative", background:"linear-gradient(180deg, #fff 0%, #f8fafc 100%)" }} onWheel={handleWheel}>
//               <div style={{ transform:`translate(${pan.x}px, ${pan.y}px) scale(${zoom})`, transformOrigin:"0 0", width:"max-content", height:"max-content", position:"absolute", left:0, top:0, cursor:isPanningRef.current?"grabbing":"grab" }} onMouseDown={onPanMouseDown}>
//                 <div style={{ display:"inline-block", verticalAlign:"top" }}>
//                   <Typography variant="caption" sx={{ml:2}}>Original</Typography>
//                   <canvas ref={originalCanvasRef} style={{ display:"block", margin:8, background:"#fff", borderRadius:8, boxShadow:"0 4px 12px rgba(0,0,0,0.06)" }}/>
//                 </div>
//                 <div style={{ display:"inline-block", verticalAlign:"top", position:"relative" }}>
//                   <Typography variant="caption" sx={{ml:2}}>Traité</Typography>
//                   <div style={{ position:"relative", display:"inline-block" }}>
//                     <canvas ref={processedCanvasRef} 
//                     onMouseDown={onRoiMouseDown} 
//                     onMouseMove={onRoiMouseMove} onMouseUp={onRoiMouseUp} 
//                     style={
//                       { display:"block", margin:8, background:"#fff", borderRadius:8, boxShadow:"0 4px 12px rgba(0,0,0,0.06)", userSelect:"none" }
//                       }/>
//                     {roi && <div style={{ position:"absolute", left:`${roi.x}px`, top:`${roi.y}px`, width:`${roi.w}px`, height:`${roi.h}px`, border:"2px dashed rgba(255,165,0,0.95)", background:"rgba(255,165,0,0.08)", pointerEvents:"none"}}/>}
//                   </div>
//                 </div>
//               </div>
//             </Box>
//           </Paper>
//           <Box sx={{mt:2, display:"flex", justifyContent:"space-between", alignItems:"center"}}>
//             <Typography variant="body2" color="text.secondary">Glisser-déposer ou uploader une image. Ctrl+Molette pour zoom.</Typography>
//             <Stack direction="row" spacing={1} alignItems="center">
//               <ImageIcon fontSize="small"/>
//               <Typography variant="body2" color="text.secondary">{imageSrc?"Image chargée":"Aucune image"}</Typography>
//             </Stack>
//           </Box>
//         </Grid>

//         {/* Right: Controls */}
//         <Grid item xs={12} md={3}>
//           <Paper sx={{p:2, borderRadius:2}} elevation={3}>
//             <Typography variant="h6" gutterBottom>Prétraitement</Typography>
//             <Stack spacing={2}>
//               <div>
//                 <label htmlFor="file-input" style={{display:"inline-block"}}>
//                   <input id="file-input" type="file" accept="image/*" style={{display:"none"}} onChange={e=>{const f=e.target.files && e.target.files[0]; handleFile(f);}}/>
//                   <Button variant="outlined" component="span" fullWidth>Upload image</Button>
//                 </label>
//               </div>

//               <Divider/>

//               {/* Grayscale */}
//               <Stack direction="row" justifyContent="space-between" alignItems="center">
//                 <Typography variant="subtitle2">Grayscale</Typography>
//                 <Button size="small" variant={grayscale?"contained":"outlined"} onClick={()=>{pushStateToUndo(); setGrayscale(g=>!g);}}> {grayscale?"On":"Off"} </Button>
//               </Stack>

//               {/* Threshold */}
//               <Typography variant="subtitle2">Threshold</Typography>
//               <Slider value={threshold} min={0} max={255} onChange={(e,v)=>setThreshold(v)} valueLabelDisplay="auto"/>


//               {/* Resize */}
//               <Typography variant="subtitle2">Resize (%)</Typography>
//               <Slider value={resizePercent} min={10} max={200} onChange={(e,v)=>setResizePercent(v)} valueLabelDisplay="auto"/>

//               {/* Rotation & Flip */}
//               <Typography variant="subtitle2">Rotation (°)</Typography>
//               <Stack direction="row" spacing={1}>
//                 <Button size="small" variant="outlined" onClick={()=>{pushStateToUndo(); setRotation(r=>(r-90)%360)}}>⟲</Button>
//                 <Button size="small" variant="outlined" onClick={()=>{pushStateToUndo(); setRotation(r=>(r+90)%360)}}>⟳</Button>
//                 <Typography sx={{ml:1}}>{rotation}°</Typography>
//               </Stack>
//               <Stack direction="row" spacing={1} sx={{mt:1}}>
//                 <Button size="small" variant={flipH?"contained":"outlined"} onClick={()=>{pushStateToUndo(); setFlipH(f=>!f)}}>Flip H</Button>
//                 <Button size="small" variant={flipV?"contained":"outlined"} onClick={()=>{pushStateToUndo(); setFlipV(f=>!f)}}>Flip V</Button>
//               </Stack>

//               {/* Normalize / Equalize / Segmentation */}
//              {/* Normalize */}
// <Stack direction="row" justifyContent="space-between">
//   <Typography variant="subtitle2">Normalisation</Typography>
//   <Button
//     size="small"
//     variant={normalize ? "contained" : "outlined"}
//     onClick={() => {
//       pushStateToUndo();
//       setNormalize(v => !v);
//     }}
//   >
//     {normalize ? "On" : "Off"}
//   </Button>
// </Stack>

// {/* Histogram Stretch */}
// <Stack direction="row" justifyContent="space-between">
//   <Typography variant="subtitle2">Étirement</Typography>
//   <Button
//     size="small"
//     variant={histStretch ? "contained" : "outlined"}
//     onClick={() => {
//       pushStateToUndo();
//       setHistStretch(v => !v);
//     }}
//   >
//     {histStretch ? "On" : "Off"}
//   </Button>
// </Stack>

// {/* Equalization */}
// <Stack direction="row" justifyContent="space-between">
//   <Typography variant="subtitle2">Égalisation</Typography>
//   <Button
//     size="small"
//     variant={equalize ? "contained" : "outlined"}
//     onClick={() => {
//       pushStateToUndo();
//       setEqualize(v => !v);
//     }}
//   >
//     {equalize ? "On" : "Off"}
//   </Button>
// </Stack>

// {/* Segmentation RGB */}
// <Stack direction="row" justifyContent="space-between">
//   <Typography variant="subtitle2">Segmentation RGB</Typography>
//   <Button
//     size="small"
//     variant={segmentationRGB ? "contained" : "outlined"}
//     onClick={() => {
//       pushStateToUndo();
//       setSegmentationRGB(v => !v);
//     }}
//   >
//     {segmentationRGB ? "On" : "Off"}
//   </Button>
// </Stack>




              

//               {/* ROI */}
//               <Stack direction="row" justifyContent="space-between" alignItems="center">
//                 <Typography variant="subtitle2">ROI</Typography>
//                 <Button
//                   size="small"
//                   variant={roiMode ? "contained" : "outlined"}
//                   onClick={() => setRoiMode(v => !v)}
//                 >
//                   Draw ROI
//                 </Button>

//               </Stack>

//               <Divider/>

//               <Stack direction="row" spacing={1} justifyContent="space-between">
//                 <Button startIcon={<UndoIcon/>} onClick={handleUndo}>Undo</Button>
//                 <Button startIcon={<RedoIcon/>} onClick={handleRedo}>Redo</Button>
//                 <Button startIcon={<RefreshIcon/>} onClick={handleReset}>Reset</Button>
//               </Stack>

//               <Button startIcon={<DownloadIcon/>} variant="contained" onClick={handleDownload} sx={{mt:1}}>Télécharger</Button>
//               <Button variant="contained" color="primary" sx={{mt:1}} onClick={goHistogram}>Voir Histogramme</Button>
//               <Typography variant="subtitle1">Filtres :</Typography>
              
//              <Button
//   variant="contained"
//   onClick={() =>
//     navigate("/blur-filters", {
//       state: {
//         image: imageSrc,           // DataURL du canvas traité
//         filename: images[selectedImage]?.name // nom du fichier pour le backend
//       }
//     })
//   }
// >
//   Blur filters
// </Button>

              
//               <Button
//   variant="contained"
//   color="secondary"
//   onClick={() =>
//     navigate("/edge-filters", {
//       state: {
//         image: imageSrc,
//         filename: images[selectedImage]?.name
//       }
//     })
//   }
// >
//   Edge filters
// </Button>

              
//             </Stack>
//           </Paper>
//         </Grid>
//       </Grid>
//     </Container>
//   );
// }
 return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#f5f7fa' }}>
      {/* Main Content Area */}
      <Box sx={{ flexGrow: 1, p: 3, overflow: 'auto' }}>
        <Container maxWidth="xl">
          {/* Viewer */}
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
              mb: 2
            }}
            elevation={3}
          >
            <Box sx={{ position: "absolute", right: 12, top: 12, zIndex: 20 }}>
              <Stack direction="row" spacing={1}>
                <Tooltip title="Zoom out"><IconButton onClick={() => setZoom(z => Math.max(0.25, +(z - 0.25).toFixed(2)))} size="small"><ZoomOutIcon /></IconButton></Tooltip>
                <Tooltip title="Zoom in"><IconButton onClick={() => setZoom(z => Math.min(4, +(z + 0.25).toFixed(2)))} size="small"><ZoomInIcon /></IconButton></Tooltip>
                <Tooltip title="Reset view"><IconButton onClick={resetView} size="small"><OpenInFullIcon /></IconButton></Tooltip>
                <Divider orientation="vertical" flexItem sx={{ mx: 0.5 }} />
                <Tooltip title="Undo"><IconButton onClick={handleUndo} size="small"><UndoIcon /></IconButton></Tooltip>
                <Tooltip title="Redo"><IconButton onClick={handleRedo} size="small"><RedoIcon /></IconButton></Tooltip>
                <Tooltip title="Reset settings"><IconButton onClick={handleReset} size="small"><RefreshIcon /></IconButton></Tooltip>
                <Tooltip title="Download"><IconButton onClick={handleDownload} size="small"><DownloadIcon /></IconButton></Tooltip>
              </Stack>
            </Box>

            <Box sx={{ width: "100%", height: "100%", position: "relative", background: "linear-gradient(180deg, #fff 0%, #f8fafc 100%)" }} onWheel={handleWheel}>
              <div style={{ transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`, transformOrigin: "0 0", width: "max-content", height: "max-content", position: "absolute", left: 0, top: 0, cursor: isPanningRef.current ? "grabbing" : "grab" }}  onMouseDown={roiMode ? undefined : onPanMouseDown}>
                <div style={{ display: "inline-block", verticalAlign: "top" }}>
                  <Typography variant="caption" sx={{ ml: 2 }}>Original</Typography>
                  <canvas ref={originalCanvasRef} style={{ display: "block", margin: 8, background: "#fff", borderRadius: 8, boxShadow: "0 4px 12px rgba(0,0,0,0.06)" }} />
                </div>
                <div style={{ display: "inline-block", verticalAlign: "top", position: "relative" }}>
                  <Typography variant="caption" sx={{ ml: 2 }}>Traité</Typography>
                  <div style={{ position: "relative", display: "inline-block" }}>
                    <canvas ref={processedCanvasRef}
                      onMouseDown={onRoiMouseDown}
                      onMouseMove={onRoiMouseMove} onMouseUp={onRoiMouseUp}
                      // style={
                      //   { display: "block", margin: 8, background: "#fff", borderRadius: 8, boxShadow: "0 4px 12px rgba(0,0,0,0.06)", userSelect: "none" }
                      // } 
                      style={{
  cursor: roiMode ? "crosshair" : isPanningRef.current ? "grabbing" : "grab"
}}
                      />
                   {roi && (
  <div
    style={{
      position: "absolute",
      left: roi.x / window.devicePixelRatio,
      top: roi.y / window.devicePixelRatio,
      width: roi.w / window.devicePixelRatio,
      height: roi.h / window.devicePixelRatio,
      border: "2px dashed rgba(255,165,0,0.95)",
      background: "rgba(255,165,0,0.08)",
      pointerEvents: "none",
      boxSizing: "border-box"
    }}
  />
)}

                  </div>
                </div>
              </div>
            </Box>
          </Paper>
          
          <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <Typography variant="body2" color="text.secondary">Glisser-déposer ou uploader une image. Ctrl+Molette pour zoom.</Typography>
            <Stack direction="row" spacing={1} alignItems="center">
              <ImageIcon fontSize="small" />
              <Typography variant="body2" color="text.secondary">{imageSrc ? "Image chargée" : "Aucune image"}</Typography>
            </Stack>
          </Box>
        </Container>
      </Box>

      {/* Right Sidebar - Fixed width */}
      <Paper 
        sx={{ 
          width: 320, 
          flexShrink: 0,
          p: 2.5, 
          borderRadius: 0,
          borderLeft: '1px solid',
          borderColor: 'divider',
          overflowY: 'auto',
          maxHeight: '100vh'
        }} 
        elevation={0}
      >
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2.5 }}>
          Prétraitement
        </Typography>
        <Stack spacing={2.5}>
          <div>
            <label htmlFor="file-input" style={{ display: "inline-block", width: '100%' }}>
              <input id="file-input" type="file" accept="image/*" style={{ display: "none" }} onChange={e => { const f = e.target.files && e.target.files[0]; handleFile(f); }} />
              <Button variant="outlined" component="span" fullWidth>Upload image</Button>
            </label>
          </div>

          <Divider />

          {/* Grayscale */}
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Typography variant="subtitle2">Grayscale</Typography>
            <Button size="small" variant={grayscale ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setGrayscale(g => !g); }}> {grayscale ? "On" : "Off"} </Button>
          </Stack>

          {/* Threshold */}
          <Box>
            <Typography variant="subtitle2" gutterBottom>Threshold</Typography>
            <Slider value={threshold} min={0} max={255} onChange={(e, v) => setThreshold(v)} valueLabelDisplay="auto" />
          </Box>

          {/* Resize */}
          <Box>
            <Typography variant="subtitle2" gutterBottom>Resize (%)</Typography>
            <Slider value={resizePercent} min={10} max={200} onChange={(e, v) => setResizePercent(v)} valueLabelDisplay="auto" />
          </Box>

          {/* Rotation & Flip */}
          <Box>
            <Typography variant="subtitle2" gutterBottom>Rotation (°)</Typography>
            <Stack direction="row" spacing={1} alignItems="center">
              <Button size="small" variant="outlined" onClick={() => { pushStateToUndo(); setRotation(r => (r - 90) % 360) }}>⟲</Button>
              <Button size="small" variant="outlined" onClick={() => { pushStateToUndo(); setRotation(r => (r + 90) % 360) }}>⟳</Button>
              <Typography sx={{ ml: 1 }}>{rotation}°</Typography>
            </Stack>
            <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
              <Button size="small" variant={flipH ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setFlipH(f => !f) }}>Flip H</Button>
              <Button size="small" variant={flipV ? "contained" : "outlined"} onClick={() => { pushStateToUndo(); setFlipV(f => !f) }}>Flip V</Button>
            </Stack>
          </Box>

          {/* Normalize */}
          <Stack direction="row" justifyContent="space-between">
            <Typography variant="subtitle2">Normalisation</Typography>
            <Button
              size="small"
              variant={normalize ? "contained" : "outlined"}
              onClick={() => {
                pushStateToUndo();
                setNormalize(v => !v);
              }}
            >
              {normalize ? "On" : "Off"}
            </Button>
          </Stack>

          {/* Histogram Stretch */}
          <Stack direction="row" justifyContent="space-between">
            <Typography variant="subtitle2">Étirement</Typography>
            <Button
              size="small"
              variant={histStretch ? "contained" : "outlined"}
              onClick={() => {
                pushStateToUndo();
                setHistStretch(v => !v);
              }}
            >
              {histStretch ? "On" : "Off"}
            </Button>
          </Stack>

          {/* Equalization */}
          <Stack direction="row" justifyContent="space-between">
            <Typography variant="subtitle2">Égalisation</Typography>
            <Button
              size="small"
              variant={equalize ? "contained" : "outlined"}
              onClick={() => {
                pushStateToUndo();
                setEqualize(v => !v);
              }}
            >
              {equalize ? "On" : "Off"}
            </Button>
          </Stack>

          {/* Segmentation RGB */}
          <Stack direction="row" justifyContent="space-between">
            <Typography variant="subtitle2">Segmentation RGB</Typography>
            <Button
              size="small"
              variant={segmentationRGB ? "contained" : "outlined"}
              onClick={() => {
                pushStateToUndo();
                setSegmentationRGB(v => !v);
              }}
            >
              {segmentationRGB ? "On" : "Off"}
            </Button>
          </Stack>

          {/* ROI */}
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Typography variant="subtitle2">ROI</Typography>
            <Button
              size="small"
              variant={roiMode ? "contained" : "outlined"}
              onClick={() => setRoiMode(v => !v)}
            >
              Draw ROI
            </Button>
          </Stack>

          <Divider />

          <Stack direction="row" spacing={1} justifyContent="space-between">
            <Button startIcon={<UndoIcon />} onClick={handleUndo}>Undo</Button>
            <Button startIcon={<RedoIcon />} onClick={handleRedo}>Redo</Button>
            <Button startIcon={<RefreshIcon />} onClick={handleReset}>Reset</Button>
          </Stack>

          <Button startIcon={<DownloadIcon />} variant="contained" onClick={handleDownload}>Télécharger</Button>
          <Button variant="contained" color="primary" onClick={goHistogram}>Voir Histogramme</Button>
          
          <Divider />
          
          <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>Filtres :</Typography>

          <Button
            variant="contained"
            onClick={() =>
              navigate("/blur-filters", {
                state: {
                  image: imageSrc,
                  filename: images[selectedImage]?.name
                }
              })
            }
          >
            Blur filters
          </Button>

          <Button
            variant="contained"
            color="secondary"
            onClick={() =>
              navigate("/edge-filters", {
                state: {
                  image: imageSrc,
                  filename: images[selectedImage]?.name
                }
              })
            }
          >
            Edge filters
          </Button>
        </Stack>
      </Paper>
    </Box>
  );
}