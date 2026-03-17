from server import UDPServer

if __name__ == "__main__":
    server = UDPServer(6789)
    server.run()
