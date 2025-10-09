// frontend/src/pages/ChatPage.tsx

import { useState, useRef, useEffect } from "react";
import { useTranslation } from "react-i18next";
import type { ChatMessage } from "../services/apiService";
import { postChatMessage } from "../services/apiService";
import "../styles/ChatPage.css";

function ChatPage() {
  const { t } = useTranslation();

  // --- STATE MANAGEMENT ---
  // State để lưu tin nhắn người dùng đang gõ
  const [currentMessage, setCurrentMessage] = useState("");
  // State để lưu toàn bộ lịch sử cuộc trò chuyện
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  // State để quản lý trạng thái loading khi chờ AI trả lời
  const [isLoading, setIsLoading] = useState(false);

  // --- REFS & EFFECTS ---
  // Ref để trỏ đến phần tử cuối cùng trong danh sách tin nhắn
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Hàm để tự động cuộn xuống tin nhắn mới nhất
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Sử dụng useEffect để thực hiện việc cuộn mỗi khi chatHistory thay đổi
  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  // --- EVENT HANDLERS ---
  const handleSendMessage = async () => {
    // Không gửi nếu tin nhắn rỗng hoặc đang loading
    if (!currentMessage.trim() || isLoading) return;

    // 1. Tạo tin nhắn mới của người dùng
    const userMessage: ChatMessage = {
      role: "user",
      parts: [{ text: currentMessage }],
    };

    // 2. Cập nhật giao diện ngay lập tức với tin nhắn của người dùng
    const updatedHistory = [...chatHistory, userMessage];
    setChatHistory(updatedHistory);
    setCurrentMessage(""); // Xóa nội dung trong ô input
    setIsLoading(true); // Bật trạng thái loading

    try {
      // 3. Gửi tin nhắn và lịch sử (trước đó) lên API
      // Chúng ta chỉ gửi `chatHistory` vì `updatedHistory` đã có trên UI
      const aiResponse = await postChatMessage({
        history: chatHistory,
        message: currentMessage,
      });

      // 4. Thêm phản hồi của AI vào lịch sử
      setChatHistory((prevHistory) => [...prevHistory, aiResponse]);
    } catch (error) {
      console.error("Failed to get AI response:", error);
      // (Tùy chọn) Có thể thêm tin nhắn lỗi vào UI
      const errorResponse: ChatMessage = {
        role: "model",
        parts: [{ text: "Sorry, I encountered an error. Please try again." }],
      };
      setChatHistory((prevHistory) => [...prevHistory, errorResponse]);
    } finally {
      // 5. Tắt trạng thái loading dù thành công hay thất bại
      setIsLoading(false);
    }
  };

  // Xử lý khi người dùng nhấn Enter
  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div className="chat-page-container">
      <h1 className="chat-title">{t("chatPage.title")}</h1>
      <div className="chat-window">
        <div className="message-list">
          {chatHistory.length === 0 && !isLoading ? (
            <p style={{ textAlign: "center" }}>
              {t("chatPage.welcomeMessage")}
            </p>
          ) : (
            chatHistory.map((msg, index) => (
              <div key={index} className={`message-container ${msg.role}`}>
                <div className={`message-bubble ${msg.role}`}>
                  {msg.parts[0].text}
                </div>
              </div>
            ))
          )}
          {/* Hiển thị "..." khi AI đang soạn tin */}
          {isLoading && (
            <div className="loading-indicator">Assistant is typing...</div>
          )}
          {/* Đây là một div trống để tự động cuộn */}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className="chat-input-area">
        <input
          type="text"
          className="chat-input"
          placeholder={t("chatPage.inputPlaceholder")}
          value={currentMessage}
          onChange={(e) => setCurrentMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button
          className="send-button"
          onClick={handleSendMessage}
          disabled={isLoading || !currentMessage.trim()}
        >
          {t("chatPage.sendButton")}
        </button>
      </div>
    </div>
  );
}

export default ChatPage;
