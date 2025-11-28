// useHistogramStore.js
import { create } from "zustand";

export const useHistogramStore = create((set, get) => ({
  histograms: [],

  addHistogram: async (title, imageSrc) => {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.src = imageSrc;

    await new Promise((resolve) => {
      img.onload = resolve;
    });

    const canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    const data = ctx.getImageData(0, 0, img.width, img.height).data;

    const grayHist = new Array(256).fill(0);
    const rHist = new Array(256).fill(0);
    const gHist = new Array(256).fill(0);
    const bHist = new Array(256).fill(0);

    for (let i = 0; i < data.length; i += 4) {
      const r = data[i],
        g = data[i + 1],
        b = data[i + 2];
      const gray = Math.round((r + g + b) / 3);
      grayHist[gray]++;
      rHist[r]++;
      gHist[g]++;
      bHist[b]++;
    }

    set((state) => ({
      histograms: [
        ...state.histograms,
        {
          title,
          imageSrc,
          gray: grayHist,
          rgb: { r: rHist, g: gHist, b: bHist },
        },
      ],
    }));
  },

  clearHistograms: () => set({ histograms: [] }),
}));
