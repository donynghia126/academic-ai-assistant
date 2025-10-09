import os
import google.generativeai as genai
from dotenv import load_dotenv 
from typing import List, Dict

# Load biến môi trường NGAY tại đây
load_dotenv()

# --- Cấu hình AI Model ---
try:
    # Lấy API key từ biến môi trường đã được load ở main.py
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
    print(f"🔍 Debug - API Key loaded: {GEMINI_API_KEY[:10] if GEMINI_API_KEY else 'NONE'}...")  # Chỉ in 10 ký tự đầu
    
    if not GEMINI_API_KEY:
        raise ValueError("Lỗi: Biến môi trường GOOGLE_API_KEY chưa được thiết lập.")
        
    # Thiết lập API key cho thư viện của Google
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Khởi tạo model AI. Sử dụng 'gemini-1.5-flash' (model mới nhất và nhanh)
    # Cấu hình an toàn để tránh các nội dung không phù hợp
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    model = genai.GenerativeModel('gemini-2.0-flash', safety_settings=safety_settings)
    print("✅  Gemini 2.0 Flash model đã được cấu hình và sẵn sàng hoạt động.")

except Exception as e:
    print(f" Lỗi nghiêm trọng khi cấu hình Gemini: {e}")
    model = None # Đặt model là None nếu có lỗi

# --- Hàm chức năng ---
def explain_code_from_gemini(code_snippet: str) -> dict:
    """
    Gửi một đoạn code đến Gemini và yêu cầu giải thích.

    Args:
        code_snippet: Đoạn mã nguồn cần được giải thích.

    Returns:
        Một dictionary chứa kết quả hoặc thông báo lỗi.
    """
    if not model:
        return {"error": "Mô hình AI chưa được khởi tạo thành công."}

    # Đây là "câu lệnh" (prompt) chúng ta ra lệnh cho AI
    prompt = f"""
    Bạn là một chuyên gia lập trình và là một người hướng dẫn giỏi. 
    Hãy phân tích và giải thích đoạn code sau đây một cách chi tiết, rõ ràng và dễ hiểu cho người mới học.
    
    Yêu cầu giải thích:
    1.  **Mục đích chính:** Đoạn code này làm gì?
    2.  **Giải thích từng dòng:** Phân tích logic của các dòng hoặc khối lệnh quan trọng.
    3.  **Gợi ý cải tiến (nếu có):** Có cách nào để viết code này tốt hơn, sạch hơn, hoặc hiệu quả hơn không?

    Đây là đoạn code cần phân tích:
    ```
    {code_snippet}
    ```
    """
    
    try:
        # Gửi yêu cầu đến Gemini
        response = model.generate_content(prompt)
        # Trả về kết quả thành công
        return {"explanation": response.text}
    except Exception as e:
        # Xử lý nếu có lỗi xảy ra trong quá trình gọi API
        print(f" Lỗi khi gọi Gemini API: {e}")
        return {"error": f"Đã xảy ra lỗi khi giao tiếp với AI: {e}"}
    
def generate_chat_response(history: List[Dict[str, any]], message: str) -> dict:
    """
    Tạo phản hồi từ AI dựa trên lịch sử trò chuyện và tin nhắn mới.

    Args:
        history: Lịch sử cuộc trò chuyện trước đó.
        message: Tin nhắn mới từ người dùng.

    Returns:
        Một dictionary chứa phản hồi của AI hoặc thông báo lỗi.
    """
    if not model:
        return {"error": "Mô hình AI chưa được khởi tạo thành công."}

    try:
        # Khởi tạo một phiên trò chuyện (chat session) với lịch sử đã có
        chat_session = model.start_chat(history=history)
        
        # Gửi tin nhắn mới của người dùng vào phiên trò chuyện
        response = chat_session.send_message(message)
        
        # Trả về kết quả thành công
        return {"role": "model", "parts": [response.text]}

    except Exception as e:
        print(f" Lỗi khi gọi Gemini API trong chat session: {e}")
        return {"error": f"Đã xảy ra lỗi khi giao tiếp với AI: {e}"}