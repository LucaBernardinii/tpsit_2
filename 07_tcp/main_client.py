from client import Socket

if __name__ == "__main__":
    client = Socket()
    client.connect('localhost', 5000)
    
    try:
        while True:
            message = input("Inserisci messaggio (exit per uscire): ")
            
            if message.lower() == 'exit':
                break
            
            client.send(message)
            response = client.receive()
            print(f"Risposta: {response}\n")
    except KeyboardInterrupt:
        print("\nInterruzione")
    finally:
        client.close()
