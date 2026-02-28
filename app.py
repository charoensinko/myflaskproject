from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # render_template จะไปหาไฟล์ในโฟลเดอร์ templates/
    return render_template("index.html")

if __name__ == "__main__":
    # debug=True ช่วยให้แก้โค้ดแล้วรีโหลดอัตโนมัติ (เหมาะกับตอนพัฒนา)
    app.run(host="0.0.0.0", port=5000, debug=True)
