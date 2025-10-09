# backend/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Tạo một "engine" của SQLAlchemy
# Đây là điểm khởi đầu cho mọi giao tiếp với cơ sở dữ liệu.
# pool_pre_ping=True giúp kiểm tra các kết nối trong pool trước khi sử dụng,
# tránh lỗi do kết nối đã bị đóng bởi server CSDL.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Tạo một lớp SessionLocal được cấu hình sẵn.
# Mỗi instance của SessionLocal sẽ là một phiên (session) cơ sở dữ liệu mới.
# autocommit=False và autoflush=False là các cài đặt phổ biến để bạn có
# toàn quyền kiểm soát khi nào các thay đổi được ghi vào CSDL.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)