import apiClient from "../api/axiosConfig";

export const UploadService = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const response = await apiClient.post(
      "/api/v1/contracts/review",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error Uploading Contract:", error);
    throw error;
  }
};
