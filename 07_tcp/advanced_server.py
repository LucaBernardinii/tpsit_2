import socket
import threading

class InetAddress:
    """Classe per gestire gli indirizzi IP"""
    def __init__(self, host):
        self.host = host
        try:
            self.ip = socket.gethostbyname(host)
            self.hostname = socket.gethostbyaddr(self.ip)[0]
        except:
            self.ip = None
            self.hostname = None
    
    def get_host_address(self):
        return self.ip
    
    def get_host_name(self):
        return self.hostname


class ServerSocket:
    """Server avanzato con analisi stringhe"""
    def __init__(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
    
    def bind(self):
        self.server_socket.bind(('localhost', self.port))
    
    def listen(self):
        self.server_socket.listen(1)
        print(f"Server avanzato in ascolto sulla porta {self.port}")
    
    def accept(self):
        client_socket, client_address = self.server_socket.accept()
        print(f"Client connesso: {client_address}")
        return client_socket, client_address
    
    def close(self):
        self.server_socket.close()


def analizza_stringa(testo):
    """Analizza una stringa in dettaglio"""
    lunghezza = len(testo)
    maiuscolo = testo.upper()
    minuscolo = testo.lower()
    inversa = testo[::-1]
    parole = len(testo.split())
    vocali = sum(1 for c in testo.lower() if c in 'aeiou')
    
    return f"""
ANALISI STRINGA:
- Originale: '{testo}'
- Lunghezza: {lunghezza} caratteri
- Maiuscolo: {maiuscolo}
- Minuscolo: {minuscolo}
- Inversa: {inversa}
- Parole: {parole}
- Vocali: {vocali}
"""


def handle_client(client_socket, client_address):
    """Gestisce la comunicazione con un client"""
    addr = InetAddress(client_address[0])
    
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8').strip()
            print(f"Ricevuto da {client_address}: {message}")
            
            if message.lower() == 'info':
                response = f"IP: {addr.get_host_address()}\nHostname: {addr.get_host_name()}"
            else:
                response = analizza_stringa(message)
            
            client_socket.send(response.encode('utf-8'))
        except:
            break
    
    client_socket.close()
    print(f"Client {client_address} disconnesso")


if __name__ == "__main__":
    server = ServerSocket(5001)
    server.bind()
    server.listen()
    
    try:
        while True:
            client_socket, client_address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\nServer stoppato")
    finally:
        server.close()
