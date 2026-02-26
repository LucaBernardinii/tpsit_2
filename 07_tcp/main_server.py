import threading
from server import ServerSocket, handle_client

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
