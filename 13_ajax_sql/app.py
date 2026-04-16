from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

def parse_sql_file(filename):
    """
    Legge il file SQL e estrae i dati degli INSERT
    Priorità:
    1. Formato completo (il database reale con migliaia di comuni)
    2. Formato semplice (di fallback)
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"Errore: {filepath} non trovato!")
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        comuni = []
        
        # Primo tentativo: formato completo (il database reale ha più comuni)
        # Pattern per: (1, 'AglieÃ¨', 'aglie', '45.3681', '7.7681', '001', '001', '001001', 0, 0)
        # Usa un pattern più flessibile
        pattern_completo = r"\(\s*\d+\s*,\s*'([^']*)',\s*'[^']*',\s*'([\d.]+)',\s*'([\d.]+)',\s*'[^']*',\s*'[^']*',\s*'[^']*',\s*[01]\s*,\s*[01]\s*\)"
        
        # Trova TUTTE le occorrenze
        matches_completo = re.findall(pattern_completo, content)
        
        if len(matches_completo) > 100:  # Se ne trova molti, usa questi (database reale)
            for nome, lat, lng in matches_completo:
                try:
                    comuni.append((nome, float(lat), float(lng), '', ''))
                except (ValueError, IndexError):
                    pass
            print(f"Caricati {len(comuni)} comuni dal database completo")
            return comuni
        
        # Se non ha trovato abbastanza, prova il formato semplice
        pattern_semplice = r"\('([^']*)',\s*([\d.]+),\s*([\d.]+),\s*'([^']*)',\s*'([^']*)'\)"
        matches_semplice = re.findall(pattern_semplice, content)
        
        if matches_semplice:
            for nome, lat, lon, prov, reg in matches_semplice:
                comuni.append((nome, float(lat), float(lon), prov, reg))
            print(f"✓ Caricati {len(comuni)} comuni dal formato semplice")
            return comuni
        
        print(f"Nessun comune trovato nel file SQL")
        return []
    
    except Exception as e:
        print(f"Errore durante il parsing di {filename}: {e}")
        import traceback
        traceback.print_exc()
        return []

# Carica i dati dal file SQL (con percorso assoluto)
COMUNI_DATA = parse_sql_file('localita.sql')

@app.route('/get_comuni', methods=['GET'])
def get_comuni():
    """
    Endpoint AJAX: Ricerca comuni in base al parametro stringa
    Parametro GET: stringa (iniziali del nome della città)
    Restituisce: Tabella HTML con i risultati
    """
    stringa = request.args.get('stringa', '').strip()
    
    if not stringa:
        return ''
    
    if not COMUNI_DATA:
        return '<p style="color: red;">Errore: Dati non caricati</p>'
    
    # Filtra i comuni che iniziano con la stringa fornita (case-insensitive)
    risultati = [c for c in COMUNI_DATA if c[0].lower().startswith(stringa.lower())]
    
    # Se nessun risultato
    if not risultati:
        return '<p style="color: #ff9800;">Nessuna città trovata con iniziali "<strong>' + stringa + '</strong>"</p>'
    
    # Costruisci l'HTML per i risultati
    html = '<table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">'
    html += '<tr><th>Città</th><th>Latitudine</th><th>Longitudine</th><th>Provincia</th><th>Regione</th></tr>'
    
    for nome, lat, lon, prov, reg in risultati:
        html += f'<tr><td>{nome}</td><td>{lat}</td><td>{lon}</td><td>{prov}</td><td>{reg}</td></tr>'
    
    html += '</table>'
    
    return html

@app.route('/')
def index():
    """Serve la pagina HTML principale con il form di ricerca"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ricerca Comuni AJAX</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 30px; 
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                max-width: 900px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 10px;
            }
            input { 
                padding: 10px; 
                font-size: 16px; 
                width: 400px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            input:focus {
                outline: none;
                border: 1px solid #4CAF50;
                box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
            }
            #risposta { 
                margin-top: 20px; 
                padding: 10px;
                background-color: #f9f9f9;
                border-radius: 4px;
            }
            table { 
                border-collapse: collapse; 
                margin-top: 10px; 
                width: 100%;
            }
            th, td { 
                border: 1px solid #ddd; 
                padding: 12px; 
                text-align: left;
            }
            th { 
                background-color: #4CAF50; 
                color: white;
                font-weight: bold;
            }
            tr:nth-child(even) { 
                background-color: #f9f9f9; 
            }
            tr:hover {
                background-color: #f0f0f0;
            }
            .info {
                color: #1976d2;
                font-style: italic;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Ricerca Comuni Italiani</h1>
            <p><b>Scrivi le iniziali del nome della città per cercare nel database:</b></p>
            <form onsubmit="return false;">
                Nome: <input type="text" id="inputCitta" onkeyup="mostra(this.value)" 
                       placeholder="Es: Mi, Ro, Na, Ve...">
            </form>
            <p class="info">Risultati:</p>
            <div id="risposta"></div>
        </div>

        <script>
            function mostra(str) {
                // Se la stringa è vuota, svuota il div risposta
                if (str.length == 0) {
                    document.getElementById("risposta").innerHTML = "";
                    return;
                }
                
                // Crea l'oggetto XMLHttpRequest
                if (window.XMLHttpRequest) {
                    xmlhttp = new XMLHttpRequest();
                } else {
                    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
                }
                
                // Funzione callback quando la risposta è pronta
                xmlhttp.onreadystatechange = function() {
                    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                        document.getElementById("risposta").innerHTML = xmlhttp.responseText;
                    }
                }
                
                // Invia la richiesta GET al server
                xmlhttp.open("GET", "/get_comuni?stringa=" + encodeURIComponent(str), true);
                xmlhttp.send();
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Server AJAX per ricerca comuni")
    print("="*60)
    print(f"Comuni caricati: {len(COMUNI_DATA)}")
    print("Accedi a: http://localhost:5000")
    print("="*60 + "\n")
    app.run(debug=True, host='localhost', port=5000)
