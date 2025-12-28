import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const analyzeProduct = async (imageUrls) => {
  try {
    const response = await axios.post(`${API_URL}/analyze-product`, {
      image_urls: imageUrls,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || error.message;
  }
};

export const analyzeProductUpload = async (files) => {
  try {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response = await axios.post(`${API_URL}/analyze/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || error.message;
  }
};
