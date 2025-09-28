import apiClient from "../api/axiosConfig";

export const ResultService = async (id) => {
  try {
    const response = await apiClient.get(`/api/v1/result/${id}`);

    return response.data;
  } catch (error) {
    console.error("Error Uploading Contract:", error);
    throw error;
  }
};
