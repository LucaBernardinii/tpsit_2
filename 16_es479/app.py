from flask import Flask, request
import urllib.request
import xml.etree.ElementTree as ET

app = Flask(__name__)

SOAP_URL = "http://www.dneonline.com/calculator.asmx"

def soap_request(method, num1=None, num2=None):
    if method == "Add":
        body = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Add xmlns="http://tempuri.org/">
      <intA>{int(num1)}</intA>
      <intB>{int(num2)}</intB>
    </Add>
  </soap:Body>
</soap:Envelope>'''
    elif method == "Subtract":
        body = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Subtract xmlns="http://tempuri.org/">
      <intA>{int(num1)}</intA>
      <intB>{int(num2)}</intB>
    </Subtract>
  </soap:Body>
</soap:Envelope>'''
    elif method == "Multiply":
        body = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Multiply xmlns="http://tempuri.org/">
      <intA>{int(num1)}</intA>
      <intB>{int(num2)}</intB>
    </Multiply>
  </soap:Body>
</soap:Envelope>'''
    elif method == "Divide":
        body = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Divide xmlns="http://tempuri.org/">
      <intA>{int(num1)}</intA>
      <intB>{int(num2)}</intB>
    </Divide>
  </soap:Body>
</soap:Envelope>'''
    else:
        return None
    
    try:
        req = urllib.request.Request(SOAP_URL, data=body.encode('utf-8'), headers={'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': f'http://tempuri.org/{method}'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Errore SOAP: {e}")
        return None

def parse_result(xml_response):
    try:
        if not xml_response:
            return "Errore di connessione"
        root = ET.fromstring(xml_response)
        for elem in root.iter():
            if 'Result' in elem.tag and elem.text:
                return elem.text
        return "Non trovato"
    except:
        return "Errore parsing"

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    result = None
    operand1 = None
    operand2 = None
    operation_used = None
    
    if request.method == "POST":
        try:
            operand1 = request.form.get("operand1", "").strip()
            operand2 = request.form.get("operand2", "").strip()
            operation = request.form.get("operation", "Add")
            
            if not operand1 or not operand2:
                result = "Inserire entrambi gli operandi"
            else:
                num1 = int(operand1)
                num2 = int(operand2)
                if operation == "Divide" and num2 == 0:
                    result = "Errore: Divisione per zero"
                else:
                    response_xml = soap_request(operation, num1, num2)
                    response = parse_result(response_xml)
                    operation_used = operation
        except ValueError:
            result = "Errore: Operandi devono essere numeri interi"
    
    return generate_html(response, result, operand1, operand2, operation_used)

def generate_html(response, result, operand1, operand2, operation_used):
    html = "<html><body><h1>Calculator</h1>"
    if response is not None or result:
        html += "<h2>Risultato</h2>"
        if result:
            html += f"<p>{result}</p>"
        else:
            html += f"<p>Op: {operation_used} | {operand1} e {operand2} = <strong>{response}</strong></p>"
        html += "<hr>"
    html += "<h2>Calcola</h2><form method='POST'>"
    html += "Op1: <input type='text' name='operand1' required>"
    html += " Op2: <input type='text' name='operand2' required>"
    html += " <select name='operation'><option>Add</option><option>Subtract</option><option>Multiply</option><option>Divide</option></select>"
    html += " <button>Calcola</button></form></body></html>"
    return html

if __name__ == "__main__":
    app.run(debug=True, port=5000)
