# backend/app/services/azure_service.py
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from app.core.config import settings

try:
    # Lấy thông tin xác thực từ file config
    endpoint = settings.AZURE_AI_ENDPOINT
    key = settings.AZURE_AI_KEY

    # Kiểm tra xem các biến đã được thiết lập chưa
    if not endpoint or not key:
        raise ValueError("Lỗi: Biến môi trường Azure (ENDPOINT, KEY) chưa được thiết lập.")

    # Tạo một đối tượng client để giao tiếp với Azure
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    print("✅ Azure Text Analytics client đã được cấu hình và sẵn sàng hoạt động.")

except Exception as e:
    print(f" Lỗi nghiêm trọng khi cấu hình Azure AI client: {e}")
    text_analytics_client = None

def analyze_document_with_azure(document_text: str) -> dict:
    """
    (Ví dụ) Gửi một đoạn văn bản đến Azure để phân tích các thực thể.
    """
    if not text_analytics_client:
        return {"error": "Azure AI client chưa được khởi tạo thành công."}

    try:
        # Gọi API của Azure để nhận diện các thực thể (ví dụ: tên người, địa điểm,...)
        result = text_analytics_client.recognize_entities(documents=[document_text])
        entities = [
            {"text": entity.text, "category": entity.category, "confidence_score": entity.confidence_score}
            for entity in result[0].entities
        ]

        return {"entities": entities}

    except Exception as e:
        print(f"Lỗi khi gọi Azure Text Analytics API: {e}")
        return {"error": f"Đã xảy ra lỗi khi giao tiếp với Azure AI: {str(e)}"}