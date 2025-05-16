# Gym Experience Classifier

## Giới thiệu

**Gym Experience Classifier** là một dự án khai phá dữ liệu (data mining) nhằm phân loại trình độ tập gym của người dùng dựa trên các thông số sức khỏe và tập luyện, chẳng hạn như số calo tiêu thụ, nhịp tim, thời gian tập, và tỷ lệ mỡ cơ thể. Dự án sử dụng mô hình học máy để dự đoán trình độ (Cơ bản, Trung bình, Nâng cao) và cung cấp giao diện web thân thiện để người dùng nhập dữ liệu, xem kết quả, lịch sử, cùng với các mẹo tập luyện và thông tin sức khỏe.

Dự án được xây dựng với mục tiêu hỗ trợ người tập gym tối ưu hóa kế hoạch tập luyện, đồng thời cung cấp tài liệu báo cáo chi tiết về quá trình khai phá dữ liệu.

## Cấu trúc thư mục

Dưới đây là cách tổ chức file và thư mục trong dự án:

```
gym-experience-classifier/
│
├── datasets/
│   └── gym_data/
│       └── gym_members_exercise_tracking.csv   # Dataset chứa dữ liệu tập luyện của các thành viên gym
├── instance/
│   └── gym_data/                               # Thư mục lưu trữ dữ liệu runtime (có thể là lịch sử người dùng)
├── model/
│   ├── best_experience_level_model.pkl         # Mô hình học máy đã được huấn luyện để phân loại trình độ
│   └── scaler.pkl                              # File scaler để chuẩn hóa dữ liệu đầu vào
├── static/
│   ├── gym-background.jpg                      # Hình nền giao diện web
│   ├── health.jpg                              # Hình ảnh minh họa thông tin sức khỏe
│   ├── nutrition.jpg                           # Hình ảnh minh họa thông tin dinh dưỡng
│   └── running.jpg                             # Hình ảnh minh họa mẹo tập luyện
├── templates/
│   ├── history.html                            # Giao diện hiển thị lịch sử dự đoán
│   ├── index.html                              # Giao diện chính (form nhập liệu và thông tin)
│   └── result.html                             # Giao diện hiển thị kết quả dự đoán
├── app.py                                      # File chính của ứng dụng Flask, chứa logic backend
├── baocao_datamining.docx                      # Tài liệu báo cáo đề tài (PDF hoặc Word)
├── Gym_Members_Exercise_Dataset.ipynb          # Jupyter Notebook phân tích và huấn luyện mô hình
└── README.md                                   # File này, chứa thông tin giới thiệu và hướng dẫn
```

### Giải thích
- **`datasets/gym_data/gym_members_exercise_tracking.csv`**: File CSV chứa dữ liệu tập luyện (calo tiêu thụ, nhịp tim, v.v.) dùng để huấn luyện mô hình.
- **`instance/gym_data/`**: Thư mục lưu trữ dữ liệu runtime, có thể chứa lịch sử dự đoán của người dùng.
- **`model/`**: Chứa mô hình học máy (`best_experience_level_model.pkl`) và scaler (`scaler.pkl`) để chuẩn hóa dữ liệu.
- **`static/`**: Thư mục chứa các tài nguyên tĩnh:
  - Hình ảnh (`gym-background.jpg`, `health.jpg`, `nutrition.jpg`, `running.jpg`) được sử dụng trong giao diện.
- **`templates/`**: Chứa các file HTML cho giao diện web:
  - `index.html`: Giao diện chính với form nhập liệu.
  - `history.html`: Hiển thị lịch sử dự đoán.
  - `result.html`: Hiển thị kết quả dự đoán.
- **`app.py`**: File chính điều khiển ứng dụng Flask, xử lý yêu cầu và tích hợp mô hình học máy.
- **`baocao_datamining`**: Tài liệu báo cáo đề tài (có thể là PDF hoặc Word).
- **`Gym_Members_Exercise_Dataset.ipynb`**: Jupyter Notebook chứa code phân tích dữ liệu và huấn luyện mô hình.

## Hướng dẫn cài đặt và sử dụng

### Yêu cầu
- Python 3.8+
- Trình duyệt web hiện đại (Chrome, Firefox, v.v.)
- Các thư viện Python: `flask`, `pandas`, `scikit-learn`, `numpy`, `joblib`

### Cài đặt
1. **Tải dự án**:
    Tải dự án 'gym-experience-classifier'

2. **Tạo môi trường ảo và cài đặt thư viện**:
    Tải các thư viện cần thiết:
   pip install flask pandas scikit-learn numpy joblib
   

3. **Chạy ứng dụng**:
   ```bash
   python app.py
   ```
   Mở trình duyệt và truy cập: `http://127.0.0.1:5000`.

### Sử dụng
- **Giao diện chính (`index.html`)**:
  - Nhập các thông số sức khỏe (calo tiêu thụ, nhịp tim, v.v.) vào form.
  - Nhấn nút "Dự đoán" để xem trình độ tập gym.
- **Kết quả (`result.html`)**:
  - Xem trình độ dự đoán (Cơ bản, Trung bình, Nâng cao) và các gợi ý.
- **Lịch sử (`history.html`)**:
  - Xem lịch sử các lần dự đoán trước đó.
- **Xem mẹo**:
  - Cột bên phải hiển thị mẹo tập luyện và thông tin sức khỏe.

### Huấn luyện mô hình
- Mở file `Gym_Members_Exercise_Dataset.ipynb` trong Jupyter Notebook để xem quá trình phân tích dữ liệu và huấn luyện mô hình.
- Dataset được sử dụng: `datasets/gym_data/gym_members_exercise_tracking.csv`.

## Công nghệ sử dụng
- **Flask**: Framework Python để xây dựng ứng dụng web.
- **Bootstrap 5.3**: Framework CSS để thiết kế giao diện.
- **Font Awesome 6.4**: Cung cấp các biểu tượng (icons) cho giao diện.
- **Scikit-learn**: Thư viện học máy để huấn luyện mô hình phân loại.
- **Pandas/Numpy**: Xử lý và phân tích dữ liệu.
- **Jupyter Notebook**: Phân tích dữ liệu và huấn luyện mô hình.
- **HTML/CSS/JavaScript**: Xây dựng giao diện và xử lý tương tác phía client.

## Tài liệu báo cáo
- Tài liệu `baocao_datamining` báo cáo chi tiết về quá trình khai phá dữ liệu, bao gồm:
  - Phân tích dataset.
  - Quy trình huấn luyện mô hình.
  - Đánh giá hiệu suất mô hình.
  - Kết quả và kết luận.

---

**Cảm ơn bạn đã sử dụng Gym Experience Classifier!**