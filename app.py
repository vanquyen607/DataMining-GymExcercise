from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import joblib
import pandas as pd
import random
from datetime import datetime

app = Flask(__name__)

# Cấu hình cơ sở dữ liệu SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tải mô hình và scaler
try:
    model = joblib.load("model/best_experience_level_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file mô hình hoặc scaler. Vui lòng kiểm tra đường dẫn.")
    exit(1)

# Định nghĩa model cơ sở dữ liệu
class UserPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    calories = db.Column(db.Float)
    duration = db.Column(db.Float)
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    avg_bpm = db.Column(db.Float)
    resting_bpm = db.Column(db.Float)
    frequency = db.Column(db.Float)
    max_bpm = db.Column(db.Float)
    fat = db.Column(db.Float)
    level = db.Column(db.String(20))

# Tạo bảng và thêm dữ liệu mẫu
with app.app_context():
    db.create_all()
    if UserPrediction.query.count() == 0:
        db.session.add(UserPrediction(calories=500, duration=1.0, age=25, weight=65, avg_bpm=120, resting_bpm=55, frequency=4, max_bpm=185, fat=20, level="Intermediate"))
        db.session.add(UserPrediction(calories=300, duration=0.5, age=40, weight=80, avg_bpm=100, resting_bpm=70, frequency=2, max_bpm=180, fat=25, level="Beginner"))
        db.session.add(UserPrediction(calories=900, duration=2.0, age=30, weight=75, avg_bpm=170, resting_bpm=50, frequency=6, max_bpm=190, fat=12, level="Advanced"))
        db.session.commit()

# Danh sách đề xuất đa dạng
exercise_options = {
    0: ["Đi bộ nhanh 20 phút.", "Đạp xe nhẹ 25 phút.", "Plank 3x20s."],
    1: ["Chạy bộ 30 phút + tạ 5kg.", "Nhảy dây 20 phút + chống đẩy.", "HIIT nhẹ 10 phút."],
    2: ["HIIT 20 phút + squat tạ 20kg.", "Deadlift + Bench press.", "Chạy bộ 40 phút 10km/h."]
}
nutrition_options = {
    0: ["Chuối + trứng luộc.", "Bánh mì + sữa.", "Salad + gà luộc."],
    1: ["Gà + cơm gạo lứt.", "Yến mạch + whey.", "Cá hồi + khoai lang."],
    2: ["Whey + cá hồi.", "Thịt bò + quinoa.", "Trứng cuộn phô mai + đậu que luộc."]
}
tips = [
    "Ngủ 7-8 giờ mỗi đêm để cơ thể phục hồi tốt hơn.",
    "Hãy uống đủ 2-3 lít nước mỗi ngày để hỗ trợ quá trình tập luyện!",
    "Kết hợp cardio và tập tạ để đạt hiệu quả tối ưu."
]

# Trung bình giả định cho so sánh
avg_data = {
    'Beginner': {'calories': 300, 'fat': 25},
    'Intermediate': {'calories': 500, 'fat': 20},
    'Advanced': {'calories': 700, 'fat': 15}
}

def get_dynamic_recommendation(prediction, data):
    calories, duration, age, weight, avg_bpm, resting_bpm, frequency, max_bpm, fat = data
    max_bpm = 220 - age if max_bpm == 0 else max_bpm
    target_bpm = max_bpm * (0.6 if prediction == 0 else 0.75 if prediction == 1 else 0.85)
    print(f"Max BPM: {max_bpm}, Target BPM: {int(target_bpm)}")  # Kiểm tra nhịp tim
    exercise_base = random.choice(exercise_options[prediction])
    if prediction == 0:
        exercise = f"{exercise_base} Giữ nhịp tim ~{int(target_bpm)} BPM. - Khởi động 5 phút. - Nghỉ 30 giây giữa các hiệp."
    elif prediction == 1:
        exercise = f"{exercise_base} Giữ nhịp tim ~{int(target_bpm)} BPM. - Khởi động 10 phút. - Nghỉ 1 phút giữa hiệp."
    else:  # Advanced
        exercise = f"{exercise_base} Giữ nhịp tim ~{int(target_bpm)} BPM. - Khởi động với tạ nhẹ. - Nghỉ 2-3 phút giữa hiệp."
    if avg_bpm > max_bpm * 0.9:
        exercise += " Cảnh báo: Bạn đang tập quá sức, hãy giảm cường độ."
    
    nutrition = random.choice(nutrition_options[prediction])
    goal = (f"Tăng tần suất lên {frequency + 1} ngày/tuần trong 1 tháng" if prediction == 0 else
            f"Đốt {int(calories * 1.2)} calo/buổi trong 3 tháng" if prediction == 1 else
            f"Giảm mỡ xuống dưới {max(10, fat - 5)}% trong 6 tháng")
    
    return {"exercise": exercise, "nutrition": nutrition, "goal": goal}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            data = [
                float(request.form['calories']),
                float(request.form['duration']),
                float(request.form['age']),
                float(request.form['weight']),
                float(request.form['avg_bpm']),
                float(request.form['resting_bpm']),
                float(request.form['frequency']),
                float(request.form['max_bpm']) if request.form['max_bpm'] else 0,
                float(request.form['fat'])
            ]
            # Kiểm tra dữ liệu hợp lệ
            age, fat, duration, frequency, max_bpm = data[2], data[8], data[1], data[6], data[7]
            if not (0 <= age <= 120 and 0 <= fat <= 100 and duration >= 0 and frequency >= 0 and max_bpm >= 0):
                return render_template('index.html', error="Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.")
            
            features = pd.DataFrame([data], columns=['Calories_Burned', 'Session_Duration (hours)', 'Age', 
                                                    'Weight (kg)', 'Avg_BPM', 'Resting_BPM', 
                                                    'Workout_Frequency (days/week)', 'Max_BPM', 'Fat_Percentage'])
            scaled_data = scaler.transform(features)
            prediction = model.predict(scaled_data)[0]
            level_map = {0: 'Beginner', 1: 'Intermediate', 2: 'Advanced'}
            level = level_map[prediction]
            rec = get_dynamic_recommendation(prediction, data)

            # Lưu vào cơ sở dữ liệu
            new_pred = UserPrediction(calories=data[0], duration=data[1], age=data[2], weight=data[3],
                                     avg_bpm=data[4], resting_bpm=data[5], frequency=data[6],
                                     max_bpm=data[7], fat=data[8], level=level)
            db.session.add(new_pred)
            db.session.commit()

            # Lấy lịch sử
            history = UserPrediction.query.order_by(UserPrediction.date.desc()).limit(5).all()
            tip = random.choice(tips)
            print(f"Input data: {data}")
            print(f"Scaled data: {scaled_data}")
            print(f"Prediction: {prediction}")
            print(f"Exercise: {rec['exercise']}, Nutrition: {rec['nutrition']}, Goal: {rec['goal']}, Tip: {tip}")  # Kiểm tra dữ liệu truyền
            
            return render_template('result.html', result=level, exercise=rec['exercise'], 
                                 nutrition=rec['nutrition'], goal=rec['goal'], 
                                 calories=data[0], fat=data[8], 
                                 avg_calories=avg_data[level]['calories'], avg_fat=avg_data[level]['fat'],
                                 history=history, tip=tip)
        except ValueError:
            return render_template('index.html', error="Vui lòng nhập đúng định dạng số.")
        except Exception as e:
            return render_template('index.html', error=f"Lỗi: {str(e)}")
    return render_template('index.html', error=None)

@app.route('/history')
def history():
    history = UserPrediction.query.order_by(UserPrediction.date.desc()).all()
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)