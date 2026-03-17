import socket
import threading

class ServerThread(threading.Thread):
    def __init__(self, socket_client):
        super().__init__()
        self.socket_client = socket_client
        self.daemon = True
    
    def run(self):
        try:
            while True:
                messaggio = self.socket_client.recv(1024).decode('utf-8')
                
                if messaggio.upper() == "FINE":
                    print(f"Client disconnesso")
                    break
                
                print(f"Echo dal server: {messaggio}")
                self.socket_client.send(f"Echo: {messaggio}".encode('utf-8'))
        
        except Exception as e:
            print(f"Errore durante la comunicazione: {e}")
        
        finally:
            self.socket_client.close()


class MultiServer:
    def __init__(self, porta=6789):
        self.porta = porta
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def start(self):
        try:
            self.server_socket.bind(("127.0.0.1", self.porta))
            self.server_socket.listen(5)
            print(f"Server avviato sulla porta {self.porta}")
            
            client_count = 0
            while True:
                socket_client, indirizzo = self.server_socket.accept()
                client_count += 1
                print(f"Client #{client_count} connesso da {indirizzo}")
                
                server_thread = ServerThread(socket_client)
                server_thread.start()
        
        except Exception as e:
            print(f"Errore nel server: {e}")
        
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    server = MultiServer()
    server.start()
