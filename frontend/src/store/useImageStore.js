// src/store/useImageStore.js
import { create } from "zustand";

// Structure d'une image : { dataUrl: string, name: string }

export const useImageStore = create((set, get) => ({
  images: [],           // tableau d'images
  selectedImage: null,  // index de l'image sélectionnée

  // Ajouter une ou plusieurs images
  addImages: (newImages) => {
    // newImages est un tableau d'objets { dataUrl, name }
    set((state) => ({
      images: [...state.images, ...newImages],
    }));
  },

  // Supprimer une image par son index
  removeImage: (index) => {
    set((state) => {
      const updatedImages = state.images.filter((_, i) => i !== index);
      let newSelected = state.selectedImage;
      if (state.selectedImage === index) {
        newSelected = null; // si l'image sélectionnée est supprimée, désélection
      } else if (state.selectedImage > index) {
        newSelected -= 1; // ajuster l'index si nécessaire
      }
      return {
        images: updatedImages,
        selectedImage: newSelected,
      };
    });
  },

  // Sélectionner une image par son index
  setSelectedImage: (index) => {
    set({ selectedImage: index });
  },

  // Réinitialiser toutes les images
clearImages: () => set({ images: [], selectedImage: null }),

}));
