import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:5000/api", // adapte au tien
});

export async function applyBackendProcessing(imageBase64, operation, params = {}) {
  const res = await API.post("/process", {
    image: imageBase64,
    operation,
    params,
  });

  return res.data.image; // base64 retournée
}
