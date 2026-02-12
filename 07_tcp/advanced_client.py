import socket

class Socket:
    """Client avanzato per l'analisi stringhe"""
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
    
    def receive(self):
        if self.connected:
            data = self.socket.recv(2048)
            return data.decode('utf-8')
        return None
    
    def close(self):
        self.socket.close()
        self.connected = False


if __name__ == "__main__":
    client = Socket()
    client.connect('localhost', 5001)
    
    print("Comandi: inserisci stringa per analisi, 'info' per info server, 'exit' per uscire\n")
    
    try:
        while True:
            message = input("Comando: ")
            
            if message.lower() == 'exit':
                break
            
            client.send(message)
            response = client.receive()
            print(response)
    except KeyboardInterrupt:
        print("\nInterruzione")
    finally:
        client.close()
