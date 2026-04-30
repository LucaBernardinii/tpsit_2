from flask import Flask, request, Response
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)

# Database di prodotti di esempio
prodotti = {
    '123ABC': {
        'prezzo': '299.99',
        'marca': 'Samsung',
        'modello': 'Galaxy S21'
    },
    '456DEF': {
        'prezzo': '899.99',
        'marca': 'Apple',
        'modello': 'iPhone 13'
    },
    '789GHI': {
        'prezzo': '599.99',
        'marca': 'Sony',
        'modello': 'Xperia 5'
    },
    '101JKL': {
        'prezzo': '199.99',
        'marca': 'Xiaomi',
        'modello': 'Redmi 9'
    },
    '202MNO': {
        'prezzo': '1299.99',
        'marca': 'Dell',
        'modello': 'XPS 13'
    },
    '303PQR': {
        'prezzo': '750.00',
        'marca': 'Lenovo',
        'modello': 'ThinkPad X1'
    },
    '404STU': {
        'prezzo': '399.99',
        'marca': 'Google',
        'modello': 'Pixel 6'
    },
    '505VWX': {
        'prezzo': '1199.99',
        'marca': 'MacBook',
        'modello': 'Pro 16"'
    }
}

# Regex pattern: 3 numeri + 3 caratteri alfanumerici
code_pattern = re.compile(r'^[0-9]{3}[A-Za-z0-9]{3}$')

@app.route('/')
def index():
    """Serve la pagina HTML principale"""
    return app.send_static_file('index.html')

@app.route('/search', methods=['GET'])
def search_product():
    """Ricerca il prodotto e restituisce XML"""
    code = request.args.get('code', '').strip().upper()
    
    # Valida il formato del codice
    if not code or not code_pattern.match(code):
        return Response('Invalid code format', status=400)
    
    # Cerca il prodotto nel database
    if code not in prodotti:
        return Response('Product not found', status=404)
    
    # Crea la risposta XML
    prodotto = prodotti[code]
    
    root = ET.Element('prodotto')
    
    prezzo = ET.SubElement(root, 'prezzo')
    prezzo.text = prodotto['prezzo']
    
    marca = ET.SubElement(root, 'marca')
    marca.text = prodotto['marca']
    
    modello = ET.SubElement(root, 'modello')
    modello.text = prodotto['modello']
    
    # Genera XML come stringa
    xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_string += ET.tostring(root, encoding='unicode')
    
    return Response(xml_string, mimetype='application/xml; charset=UTF-8')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
