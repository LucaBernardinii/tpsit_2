import socket

class UDPServer:
    def __init__(self, port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('localhost', port))
        self.buffer_size = 1024
        
    def receive_and_respond(self):
        """Riceve messaggi dal client e invia risposte"""
        print(f"Server in ascolto sulla porta {self.port}...")
        
        while True:
            # Ricevi il messaggio dal client
            data, client_address = self.socket.recvfrom(self.buffer_size)
            
            # Decodifica il messaggio ricevuto
            message = data.decode('utf-8')
            print(f"Messaggio ricevuto da {client_address}: {message}")
            
            # Se il client invia "fine", il server esce dal ciclo
            if message.lower() == "fine":
                response = "SERVER IN CHIUSURA. Buona serata."
                self.socket.sendto(response.encode('utf-8'), client_address)
                print("Connessione chiusa dal client.")
                break
            
            # Trasforma il messaggio in maiuscolo e invia la risposta
            response = message.upper()
            self.socket.sendto(response.encode('utf-8'), client_address)
            
    def close(self):
        """Chiude il socket del server"""
        self.socket.close()
    
    def run(self):
        """Avvia il server"""
        try:
            self.receive_and_respond()
        except KeyboardInterrupt:
            print("\nServer interrotto.")
        finally:
            self.close()
