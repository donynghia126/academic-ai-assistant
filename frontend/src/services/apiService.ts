import axios from "axios";

// Tạo một instance của axios với cấu hình cơ bản
const apiClient = axios.create({
  baseURL: "http://localhost:8000/api/v1", // URL gốc của backend API
  headers: {
    "Content-Type": "application/json",
  },
});

// Định nghĩa một hàm để gọi đến endpoint health check
export const checkHealth = async () => {
  try {
    const response = await apiClient.get("/status");
    return response.data;
  } catch (error) {
    console.error("Lỗi khi kết nối tới API:", error);
    throw error; // Ném lỗi ra để component có thể xử lý
  }
};
