import { create } from "zustand";

export const useImageStore = create((set, get) => ({
  images: [], // liste des images importées
  selectedImage: null, // index de l’image sélectionnée
  imageHistory: {}, // historique simple (si tu veux le garder)

  /** Ajouter des images */
  addImages: (newImages) =>
    set((state) => ({
      images: [
        ...state.images,
        ...newImages.map((img) => ({
          ...img,
          history: [
            {
              action: "Image importée",
              timestamp: new Date().toISOString(),
              dataUrl: img.dataUrl,
            },
          ],
        })),
      ],
    })),

  /** Effacer toutes les images */
  clearImages: () =>
    set({
      images: [],
      selectedImage: null,
      imageHistory: {},
    }),

  /** Supprimer une image */
  removeImage: (index) =>
    set((state) => {
      const updatedImages = state.images.filter((_, i) => i !== index);
      const updatedHistory = { ...state.imageHistory };
      delete updatedHistory[index];

      return {
        images: updatedImages,
        selectedImage:
          state.selectedImage === index ? null : state.selectedImage,
        imageHistory: updatedHistory,
      };
    }),

  /** Sélectionner une image uniquement */
  setSelectedImage: (index) =>
    set({
      selectedImage: index,
    }),

  /** Sélectionner + ajouter dans l'historique (garde ton nom) */
  selectImageWithHistory: (index) =>
    set((state) => {
      const newHistory = { ...state.imageHistory };

      if (!newHistory[index]) newHistory[index] = [];

      newHistory[index].push({
        date: new Date().toLocaleString(),
      });

      // Ajouter aussi dans l'historique interne de l'image
      const imagesCopy = [...state.images];

      imagesCopy[index].history.push({
        action: "Image sélectionnée",
        timestamp: new Date().toISOString(),
        dataUrl: imagesCopy[index].dataUrl,
      });

      return {
        selectedImage: index,
        imageHistory: newHistory,
        images: imagesCopy,
      };
    }),

  /** Ajouter au journal d’une image — utile pour processing */
  addHistory: (index, action, dataUrl) =>
    set((state) => {
      const imagesCopy = [...state.images];

      imagesCopy[index].history.push({
        action,
        timestamp: new Date().toISOString(),
        dataUrl,
      });

      imagesCopy[index].dataUrl = dataUrl;

      return { images: imagesCopy };
    }),

  /** Revenir à un état précédent */
  revertToHistory: (imageIndex, historyIndex) =>
    set((state) => {
      const imagesCopy = [...state.images];
      const item = imagesCopy[imageIndex].history[historyIndex];

      imagesCopy[imageIndex].dataUrl = item.dataUrl;

      imagesCopy[imageIndex].history.push({
        action: `Retour à l’état ${historyIndex}`,
        timestamp: new Date().toISOString(),
        dataUrl: item.dataUrl,
      });

      return { images: imagesCopy };
    }),
}));
