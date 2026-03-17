from client import UDPClient

if __name__ == "__main__":
    client = UDPClient('localhost', 6789)
    client.run()
