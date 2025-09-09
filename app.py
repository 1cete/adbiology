from flask import Flask, render_template
import os
import re

app = Flask(__name__)

testai = {
    "augalai": [
        ("Audiniai/organai", "https://forms.gle/KDucLNTPh1qvzmmF8"),
        ("Dauginimasis", "https://forms.gle/HQAtTbXFDdwyUmU86"),
    ],
    "bakterijos": "https://forms.gle/zJbxUaGXTE3R72wE9",
    "baltymų_sintezė": "https://forms.gle/ktcJ4NcaE7SuoJzg6",
    "cheminiai_junginiai": [
        ("Cheminiai junginiai", "https://forms.gle/s4jEAtbY1BFtqrvD7"),
        ("Baltymai", "https://forms.gle/WvNimTfXPPczcZ8s6"),
    ],
    "citologija": "https://forms.gle/CN5bD8AbjZ9MqAA86",
    "ekologija": "https://forms.gle/Wk52Gfrgd36qL8Nt9",
    "endokrininė_sistema": "https://forms.gle/7ZfdZ6GeeHimM1Rg8",
    "evoliucija": "https://forms.gle/2437SXj7gNNkkqZEA",
    "fotosintezė": "https://forms.gle/DcMfVm2nRUoBpmcs9",
    "genetika": "https://forms.gle/svNaWLFDnzGtCiLZ7",
    "imunologija": "https://forms.gle/SmZiFGGbxvCbzJjL8",
    "kraujotaka": "https://forms.gle/C3B7iTzn8wcHp5Mo8",
    "lastelinis_kvėpavimas": "https://forms.gle/P3Jj4UfMGBsFfJX4A",
    "lastelės_ciklas": "https://forms.gle/zCEZ8tJCSBV6HhCr7",
    "limfotaka": "https://forms.gle/9huTDiSgMWuB5aH89",
    "lytinė_sistema": "https://forms.gle/8YvJpfPJJGs4STCy5",
    "membranos": "https://forms.gle/UgjUS1qXtmnvWtHZ6",
    "nervų_sistema": "https://forms.gle/v7xCy1ca1D6dT1Xy6",
    "virškinimas": "https://forms.gle/LhXroRgbLyjEJET59",
    "šalinimas": "https://forms.gle/xLCTrXBEbfrtgjWp8",
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
