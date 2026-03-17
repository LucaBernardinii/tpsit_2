import socket
import sys

class Client:
    def __init__(self, host="127.0.0.1", porta=6789):
        self.host = host
        self.porta = porta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        try:
            self.socket.connect((self.host, self.porta))
            print(f"Connesso al server {self.host}:{self.porta}")
        except Exception as e:
            print(f"Errore di connessione: {e}")
            sys.exit(1)
    
    def communicate(self):
        try:
            while True:
                # Legge input dell'utente
                messaggio = input("Inserisci un messaggio (o 'FINE' per terminare): ")
                
                # Invia il messaggio al server
                self.socket.send(messaggio.encode('utf-8'))
                
                # Se l'utente digita FINE, termina
                if messaggio.upper() == "FINE":
                    print("Chiusura della connessione...")
                    break
                
                # Riceve la risposta dal server
                risposta = self.socket.recv(1024).decode('utf-8')
                print(f"Risposta dal server: {risposta}")
        
        except Exception as e:
            print(f"Errore durante la comunicazione: {e}")
        
        finally:
            self.socket.close()
            print("Connessione chiusa")


if __name__ == "__main__":
    client = Client()
    client.connect()
    client.communicate()
