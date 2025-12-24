from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

giftDB = {
  "Trần Thị Phương Quỳnh": "Phạm Quang Bình",
  "Phạm Quang Bình": "Nguyễn Minh Nhật",
  "Nguyễn Minh Nhật": "Trần Thị Phương Quỳnh",
  "Lâm Gia Tài": "Hoàng Lam Ngọc",
  "Hoàng Lam Ngọc": "Lâm Gia Tài",
  "Trì Nam An": "Trần Thái Bảo",
  "Trần Thái Bảo": "Trì Nam An",
  "Nguyễn Trần Nam Khôi": "Phan Xuân Khoa",
  "Phan Xuân Khoa": "Nguyễn Trần Nam Khôi",
  "Hoàng Nhật Nam": "Lê Nguyễn Đăng Khoa",
  "Lê Nguyễn Đăng Khoa": "Hoàng Nhật Nam"
}

sessions = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    name = request.json.get("name")
    question = request.json.get("question")

    if name not in giftDB:
        return jsonify({"answer": "❌ Không tìm thấy người này trong danh sách."})

    if name not in sessions:
        sessions[name] = {
            "count": 0,
            "guessed": False
        }

    s = sessions[name]

    if s["count"] >= 3:
        return jsonify({"answer": "⛔ Bạn đã hỏi đủ 3 câu rồi."})

    s["count"] += 1

    giver = giftDB[name]
    answer = generate_answer(question, giver)

    return jsonify({
        "answer": answer,
        "count": s["count"]
    })

def generate_answer(question, giver):
    q = question.lower()
    name_len = len(giver.replace(" ", ""))
    word_count = len(giver.split())

    if "ký tự" in q:
        return f"Tên người tặng có {name_len} ký tự."
    if "mấy từ" in q or "bao nhiêu từ" in q:
        return f"Tên người tặng gồm {word_count} từ."
    if "họ" in q:
        return f"Họ của người tặng nằm trong họ phổ biến ở Việt Nam."
    if "tên" in q:
        return "Tên người tặng không quá ngắn và cũng không quá dài."
    return "Câu hỏi hợp lệ 👍 nhưng mình chỉ có thể trả lời liên quan đến cấu trúc tên."

if __name__ == "__main__":
    app.run()
