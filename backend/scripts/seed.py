# backend/scripts/seed.py
import sys
import os

# Thêm đường dẫn gốc của dự án vào Python path
# để có thể import các module từ app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal
from app.models.subject import Subject, Topic

def seed_data():
    db = SessionLocal()
    try:
        # Kiểm tra xem dữ liệu đã tồn tại chưa
        if db.query(Subject).first():
            print("Dữ liệu đã tồn tại, bỏ qua seeding.")
            return

        print("Bắt đầu seeding dữ liệu mẫu...")

        # --- Môn học 1: Lập trình Web ---
        web_dev = Subject(
            name="Lập trình Web",
            description="Khám phá thế giới phát triển web từ front-end đến back-end."
        )
        db.add(web_dev)
        db.commit() # Commit để web_dev có ID

        topics_web = [
            Topic(name="HTML & CSS Cơ Bản", subject_id=web_dev.id),
            Topic(name="JavaScript Nền Tảng", subject_id=web_dev.id),
            Topic(name="ReactJS Framework", subject_id=web_dev.id),
            Topic(name="Node.js & Express", subject_id=web_dev.id)
        ]
        db.bulk_save_objects(topics_web)

        # --- Môn học 2: DevOps ---
        devops = Subject(
            name="DevOps",
            description="Tìm hiểu văn hóa và công cụ để tự động hóa quy trình phát triển phần mềm."
        )
        db.add(devops)
        db.commit() # Commit để devops có ID

        topics_devops = [
            Topic(name="Git & Version Control", subject_id=devops.id),
            Topic(name="Docker & Containerization", subject_id=devops.id),
            Topic(name="CI/CD với GitHub Actions", subject_id=devops.id),
            Topic(name="Kubernetes Basics", subject_id=devops.id)
        ]
        db.bulk_save_objects(topics_devops)

        db.commit()
        print("Seeding dữ liệu thành công!")

    except Exception as e:
        print(f"Lỗi trong quá trình seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()