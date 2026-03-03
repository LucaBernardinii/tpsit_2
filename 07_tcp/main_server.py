from server import ServerSocket

if __name__ == "__main__":
    server = ServerSocket(5000)
    server.bind()
    server.listen()
    
    while True:
        client_socket, client_address = server.accept()
        server.handle_client(client_socket)
