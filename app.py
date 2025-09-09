from flask import Flask, render_template
import os
import re

app = Flask(__name__)

testai = {
    "Augalai": [
        ("Audiniai/organai", "https://forms.gle/KDucLNTPh1qvzmmF8"),
        ("Dauginimasis", "https://forms.gle/HQAtTbXFDdwyUmU86"),
    ],
    "Bakterijos": "https://forms.gle/zJbxUaGXTE3R72wE9",
    "Baltymu sinteze": "https://forms.gle/ktcJ4NcaE7SuoJzg6",
    "Cheminiai junginiai": [
        ("Cheminiai junginiai", "https://forms.gle/s4jEAtbY1BFtqrvD7"),
        ("Baltymai", "https://forms.gle/WvNimTfXPPczcZ8s6"),
    ],
    "Citologija": "https://forms.gle/CN5bD8AbjZ9MqAA86",
    "Ekologija": "",
    "Endokrinine sistema": "https://forms.gle/7ZfdZ6GeeHimM1Rg8",
    "Evoliucija": "https://forms.gle/2437SXj7gNNkkqZEA",
    "Fotosinteze": "",
    "Genetika": "https://forms.gle/svNaWLFDnzGtCiLZ7",
    "Imunologija": "https://forms.gle/SmZiFGGbxvCbzJjL8",
    "Kraujotaka": "https://forms.gle/C3B7iTzn8wcHp5Mo8",
    "Lastelinis kvepavimas": "https://forms.gle/P3Jj4UfMGBsFfJX4A",
    "Lasteles ciklas": "https://forms.gle/zCEZ8tJCSBV6HhCr7",
    "Limfotaka": "https://forms.gle/9huTDiSgMWuB5aH89",
    "Lytine sistema": "https://forms.gle/8YvJpfPJJGs4STCy5",
    "Membranos": "https://forms.gle/UgjUS1qXtmnvWtHZ6",
    "Nervu sistema": "https://forms.gle/v7xCy1ca1D6dT1Xy6",
    "Virskinimas": "https://forms.gle/LhXroRgbLyjEJET59",
    "Salinimas": "https://forms.gle/xLCTrXBEbfrtgjWp8",
}

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
            testas_url = testai.get(tema_vardas, "#")  # gali pakeisti pagal temą
            
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
