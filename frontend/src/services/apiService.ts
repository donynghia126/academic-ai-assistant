// frontend/src/services/apiService.ts
import axios from "axios";

// Định nghĩa kiểu dữ liệu cho một tin nhắn, khớp với Pydantic model ở backend
export interface ChatMessage {
  role: "user" | "model";
  parts: { text: string }[]; // Gemini API thường dùng cấu trúc này
}

// Cấu trúc dữ liệu gửi đi khi chat
export interface ChatPayload {
  history: ChatMessage[];
  message: string;
}

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
// [MỚI] Hàm gửi tin nhắn và lịch sử trò chuyện
export const postChatMessage = async (
  payload: ChatPayload
): Promise<ChatMessage> => {
  try {
    // Chuyển đổi format trước khi gửi: từ {text: string} sang string[]
    const backendPayload = {
      history: payload.history.map(msg => ({
        role: msg.role,
        parts: msg.parts.map(part => part.text)
      })),
      message: payload.message
    };

    const response = await apiClient.post("/chat/conversation", backendPayload);
    
    // API backend trả về: {role: "model", parts: ["text response"]}
    // Chuyển đổi sang format frontend: {role: "model", parts: [{text: "text response"}]}
    const aiMessage: ChatMessage = {
      role: response.data.role,
      parts: response.data.parts.map((text: string) => ({ text }))
    };
    return aiMessage;
  } catch (error) {
    console.error("Lỗi khi gửi tin nhắn chat:", error);
    throw error;
  }
};

// [MỚI] Hàm gửi code để phân tích (từ Phase I)
// Tái cấu trúc lại để dùng chung apiClient cho gọn gàng
export const explainCode = async (code: string): Promise<string> => {
  try {
    const response = await apiClient.post("/code/explain", {
      code: code, // Backend expects "code" not "code_snippet"
    });
    return response.data.explanation;
  } catch (error) {
    console.error("Lỗi khi gửi code để phân tích:", error);
    throw error;
  }
};
