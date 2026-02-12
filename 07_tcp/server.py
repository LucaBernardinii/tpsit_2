import socket
import threading

class InetAddress:
    """Classe per gestire gli indirizzi IP"""
    def __init__(self, host):
        self.host = host
        try:
            self.ip = socket.gethostbyname(host)
        except:
            self.ip = None
    
    def get_host_address(self):
        return self.ip


class ServerSocket:
    """Classe ServerSocket per la comunicazione lato server"""
    def __init__(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
    
    def bind(self):
        self.server_socket.bind(('localhost', self.port))
    
    def listen(self):
        self.server_socket.listen(1)
        print(f"Server in ascolto sulla porta {self.port}")
    
    def accept(self):
        client_socket, client_address = self.server_socket.accept()
        print(f"Client connesso: {client_address}")
        return client_socket, client_address
    
    def close(self):
        self.server_socket.close()


def handle_client(client_socket):
    """Gestisce la comunicazione con un client"""
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"Ricevuto: {message}")
            
            # Analizza la stringa
            response = f"Lunghezza: {len(message)} | Maiuscolo: {message.upper()}"
            
            client_socket.send(response.encode('utf-8'))
        except:
            break
    
    client_socket.close()


if __name__ == "__main__":
    server = ServerSocket(5000)
    server.bind()
    server.listen()
    
    try:
        while True:
            client_socket, client_address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\nServer stoppato")
    finally:
        server.close()
