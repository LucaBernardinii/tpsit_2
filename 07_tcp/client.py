import socket

class Socket:
    """Classe Socket per la comunicazione lato client"""
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
    
    def connect(self, host, port):
        try:
            self.socket.connect((host, port))
            self.connected = True
            print(f"Connesso a {host}:{port}")
        except Exception as e:
            print(f"Errore di connessione: {e}")
    
    def send(self, message):
        if self.connected:
            self.socket.send(message.encode('utf-8'))
            print(f"Inviato: {message}")
    
    def receive(self):
        if self.connected:
            data = self.socket.recv(1024)
            return data.decode('utf-8')
        return None
    
    def close(self):
        self.socket.close()
        self.connected = False
        print("Disconnesso")
