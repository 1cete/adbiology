from flask import Flask, render_template
import os

app = Flask(__name__)

temos = [
    {
        "pavadinimas": "Ląstelės sandara",
        "konspektas": "lasteles_sandara.pdf",
        "testas": "https://forms.gle/"
    },
    {
        "pavadinimas": "Kraujotaka",
        "konspektas": "kraujotaka1.pdf",
        "testas": "https://forms.gle/"
    }
]

@app.route("/")
def home():
    return render_template("index.html", temos=temos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render priskirs savo PORT, o vietoje jo naudos 5000 lokaliai
    app.run(host="0.0.0.0", port=port)