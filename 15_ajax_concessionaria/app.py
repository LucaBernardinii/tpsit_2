from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

def carica_auto():
    """Carica il file JSON con le auto disponibili"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, 'auto.json')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        auto = json.load(f)
    
    return auto

def filtra_auto(auto, marca, modello, alimentazione, colore):
    """Filtra le auto in base ai parametri ricevuti"""
    risultati = []
    
    for a in auto:
        # Se il parametro è vuoto, non viene considerato nel filtro
        if marca and a['marca'].lower() != marca.lower():
            continue
        if modello and a['modello'].lower() != modello.lower():
            continue
        if alimentazione and a['alimentazione'].lower() != alimentazione.lower():
            continue
        if colore and a['colore'].lower() != colore.lower():
            continue
        
        risultati.append(a)
    
    return risultati

@app.route('/')
def index():
    """Serve la pagina HTML"""
    return open('15_ajax_concessionaria/index.html', 'r', encoding='utf-8').read()

@app.route('/cerca')
def cerca():
    """Elabora la ricerca e restituisce i risultati in JSON"""
    marca = request.args.get('marca', '')
    modello = request.args.get('modello', '')
    alimentazione = request.args.get('alimentazione', '')
    colore = request.args.get('colore', '')
    
    auto = carica_auto()
    risultati = filtra_auto(auto, marca, modello, alimentazione, colore)
    
    return jsonify(risultati)

if __name__ == '__main__':
    app.run(debug=True)
