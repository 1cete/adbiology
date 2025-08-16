from flask import Flask, render_template
import os

app = Flask(__name__)

# Funkcija automatiškai surenka temas pagal paveikslėlius ir PDF konspektus
def gauti_temus():
    paveiksleliai_folderis = 'static/paveiksleliai'
    konspektai_folderis = 'static/konspektai'
    temos = []

    for failas in os.listdir(paveiksleliai_folderis):
        if failas.endswith(('.jpg', '.png', '.jpeg', '.gif')):
            tema_vardas = os.path.splitext(failas)[0]  # pvz., 'citologija'
            paveikslelis = f"paveiksleliai/{failas}"
            konspektas_path = f"konspektai/{tema_vardas}.pdf"
            testas_url = "https://forms.gle/"  # gali pakeisti pagal temą
            
            # Tikrina, ar PDF konspektas egzistuoja
            if not os.path.exists(f"static/{konspektas_path}"):
                konspektas_path = "#"  # jei nėra konspekto, rodo tuščią nuorodą
            
            temos.append({
                "pavadinimas": tema_vardas.replace('_', ' ').title(),
                "paveikslelis": paveikslelis,
                "konspektas": konspektas_path,
                "testas": testas_url
            })
    
    # Rūšiuoja temas pagal pavadinimą
    return sorted(temos, key=lambda x: x['pavadinimas'])


@app.route("/")
def home():
    temos = gauti_temus()
    return render_template("index.html", temos=temos)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render ar kitas hostas priskirs savo PORT
    app.run(host="0.0.0.0", port=port, debug=True)
