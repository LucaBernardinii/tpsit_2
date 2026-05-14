from flask import Flask, request
import urllib.request
import xml.etree.ElementTree as ET

app = Flask(__name__)

# SOAP service URL - usa il WSDL endpoint
SOAP_URL = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

def soap_request(method, iso_code=None):
    """
    Invia una richiesta SOAP al servizio e restituisce la risposta in XML
    """
    if method == "ListOfCountryNamesByCode":
        body = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ListOfCountryNamesByCode xmlns="http://www.oorsprong.org/websamples.countryinfo"/>
  </soap:Body>
</soap:Envelope>'''
    
    elif method == "CapitalCity":
        body = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CapitalCity xmlns="http://www.oorsprong.org/websamples.countryinfo">
      <sCountryISOCode>{iso_code}</sCountryISOCode>
    </CapitalCity>
  </soap:Body>
</soap:Envelope>'''
    
    elif method == "CountryIntPhoneCode":
        body = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CountryIntPhoneCode xmlns="http://www.oorsprong.org/websamples.countryinfo">
      <sCountryISOCode>{iso_code}</sCountryISOCode>
    </CountryIntPhoneCode>
  </soap:Body>
</soap:Envelope>'''
    
    elif method == "FullCountryInfo":
        body = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <FullCountryInfo xmlns="http://www.oorsprong.org/websamples.countryinfo">
      <sCountryISOCode>{iso_code}</sCountryISOCode>
    </FullCountryInfo>
  </soap:Body>
</soap:Envelope>'''
    
    else:
        return None
    
    try:
        req = urllib.request.Request(
            SOAP_URL,
            data=body.encode('utf-8'),
            headers={
                'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': f'http://www.oorsprong.org/websamples.countryinfo/{method}'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    
    except Exception as e:
        return f"Errore: {str(e)}"

def parse_countries_list(xml_response):
    """
    Estrae la lista dei paesi dalla risposta XML
    """
    try:
        root = ET.fromstring(xml_response)
        
        # Namespace
        ns = {'tns': 'http://www.oorsprong.org/websamples.countryinfo'}
        
        countries = []
        for tCountryCodeAndName in root.findall('.//tns:tCountryCodeAndName', ns):
            iso_code = tCountryCodeAndName.findtext('tns:sISOCode', '', ns)
            name = tCountryCodeAndName.findtext('tns:sName', '', ns)
            if iso_code and name:
                countries.append({'code': iso_code, 'name': name})
        
        return countries
    except Exception as e:
        return []

def parse_capital_city(xml_response):
    """
    Estrae la capitale dalla risposta XML
    """
    try:
        if not xml_response or isinstance(xml_response, str) and xml_response.startswith("Errore"):
            return xml_response
        root = ET.fromstring(xml_response)
        capital = root.findtext('.//{http://www.oorsprong.org/websamples.countryinfo}CapitalCityResult', '')
        return capital if capital else "Non trovato"
    except Exception as e:
        return f"Errore nel parsing: {str(e)}"

def parse_phone_code(xml_response):
    """
    Estrae il codice telefonico dalla risposta XML
    """
    try:
        if not xml_response or isinstance(xml_response, str) and xml_response.startswith("Errore"):
            return xml_response
        root = ET.fromstring(xml_response)
        code = root.findtext('.//{http://www.oorsprong.org/websamples.countryinfo}CountryIntPhoneCodeResult', '')
        return code if code else "Non trovato"
    except Exception as e:
        return f"Errore nel parsing: {str(e)}"

def parse_full_info(xml_response):
    """
    Estrae le informazioni complete dalla risposta XML
    """
    try:
        if not xml_response or isinstance(xml_response, str) and xml_response.startswith("Errore"):
            return xml_response
        root = ET.fromstring(xml_response)
        ns = {'tns': 'http://www.oorsprong.org/websamples.countryinfo'}
        
        info = root.find('.//tns:FullCountryInfoResult', ns)
        if info is None:
            return "Non trovato"
        
        result = {}
        for child in info:
            tag = child.tag.split('}')[-1]
            result[tag] = child.text
        
        return result
    except Exception as e:
        return f"Errore nel parsing: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    countries = []
    response = None
    result = None
    iso_code = None
    service_used = None
    
    # Carica la lista dei paesi
    countries_xml = soap_request("ListOfCountryNamesByCode")
    if countries_xml:
        countries = parse_countries_list(countries_xml)
    
    # Gestisce le richieste POST
    if request.method == "POST":
        iso_code = request.form.get("isocode", "").strip().upper()
        service = request.form.get("service", "CapitalCity")
        
        if not iso_code:
            result = "Inserire un codice ISO"
        else:
            response_xml = soap_request(service, iso_code)
            
            if service == "CapitalCity":
                response = parse_capital_city(response_xml)
                service_used = "CapitalCity"
            elif service == "CountryIntPhoneCode":
                response = parse_phone_code(response_xml)
                service_used = "CountryIntPhoneCode"
            elif service == "FullCountryInfo":
                response = parse_full_info(response_xml)
                service_used = "FullCountryInfo"
    
    # Genera l'HTML
    html = generate_html(countries, response, result, iso_code, service_used)
    return html

def generate_html(countries, response, result, iso_code, service_used):
    """
    Genera l'HTML della pagina
    """
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Countries SOAP Services</title>
</head>
<body>
    <h1>Countries SOAP Services</h1>
    """
    
    if response is not None or result:
        html += "<h2>Risultato</h2>"
        
        if result:
            html += f"<p>{result}</p>"
        else:
            html += f"<p>Servizio: {service_used}</p>"
            html += f"<p>Codice ISO: {iso_code}</p>"
            html += "<p>Risultato:</p>"
            
            if isinstance(response, dict):
                html += "<table border='1'><tr><th>Proprietà</th><th>Valore</th></tr>"
                for key, value in response.items():
                    html += f"<tr><td>{key}</td><td>{value if value else 'N/A'}</td></tr>"
                html += "</table>"
            elif isinstance(response, list):
                html += "<pre>"
                for item in response:
                    html += f"{item}\n"
                html += "</pre>"
            else:
                html += f"<pre>{response}</pre>"
        
        html += "<hr>"
    
    html += """
    <h2>Richiesta</h2>
    <form method="POST">
        <label for="isocode">Codice ISO:</label>
        <input type="text" name="isocode" placeholder="es. IT, US, BR" required>
        
        <label for="service">Servizio:</label>
        <select name="service" required>
            <option value="CapitalCity">CapitalCity</option>
            <option value="CountryIntPhoneCode">CountryIntPhoneCode</option>
            <option value="FullCountryInfo">FullCountryInfo</option>
        </select>
        
        <button type="submit">Invia</button>
    </form>
    """
    
    if countries:
        html += """
    <h2>Lista Paesi</h2>
    <table border="1">
        <tr><th>Codice ISO</th><th>Paese</th></tr>
        """
        
        for country in countries:
            html += f"<tr><td>{country['code']}</td><td>{country['name']}</td></tr>"
        
        html += "</table>"
    
    html += """
</body>
</html>
    """
    
    return html

if __name__ == "__main__":
    app.run(debug=True)