from flask import Flask, render_template
import os
import re

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

# Funkcija automatiškai surenka VBE metus iš pdf failų
def gauti_vbe_metus():
    pdf_folderis = 'static/pdf'
    metai = set()

    if os.path.exists(pdf_folderis):
        for failas in os.listdir(pdf_folderis):
            match = re.match(r"(\d{4})_(pagrindine|pakartotine)\.pdf", failas)
            if match:
                metai.add(int(match.group(1)))  # išsaugom metus kaip skaičių

    return sorted(metai, reverse=True)  # nuo naujausių iki seniausių


@app.route("/")
def home():
    temos = gauti_temus()
    vbe_metai = gauti_vbe_metus()
    return render_template("index.html", temos=temos, vbe_metai=vbe_metai)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render ar kitas hostas priskirs savo PORT
    app.run(host="0.0.0.0", port=port, debug=True)
