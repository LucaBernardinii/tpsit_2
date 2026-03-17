import socket

class UDPClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffer_size = 1024
        
    def send_and_receive(self, message):
        """Invia un messaggio al server e riceve la risposta"""
        # Prepara il messaggio e invia al server
        self.socket.sendto(message.encode('utf-8'), (self.server_address, self.server_port))
        
        # Riceve la risposta dal server
        response, server_address = self.socket.recvfrom(self.buffer_size)
        return response.decode('utf-8')
    
    def close(self):
        """Chiude il socket del client"""
        self.socket.close()
    
    def run(self):
        """Loop principale per la comunicazione interattiva"""
        try:
            while True:
                # Chiedi all'utente di inserire un messaggio
                message = input("Inserisci un dato da inviare: ")
                
                # Invia il messaggio e riceve la risposta
                response = self.send_and_receive(message)
                print(f"dal SERVER: {response}")
                
                # Se l'utente inserisce "fine", il client termina
                if message.lower() == "fine":
                    break
                    
        except Exception as e:
            print(f"Errore: {e}")
        finally:
            self.close()
