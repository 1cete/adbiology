from flask import Flask, render_template

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
    app.run(debug=True)