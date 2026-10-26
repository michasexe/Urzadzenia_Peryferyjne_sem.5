import socket

# 0.0.0.0 oznacza, że PC nasłuchuje na wszystkich swoich interfejsach sieciowych
HOST = '0.0.0.0'
PORT = 65432  # Wybrany wolny port

def start_server():
    print("Aktywacja urządzenia: uruchamianie nasłuchiwania...")
    
    # b). uruchomienie oprogramowania realizującego transmisję (przygotowanie socketu TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serwer nasłuchuje na porcie {PORT}. Czekam na Raspberry Pi...")
        
        # Oczekiwanie na połączenie od klienta
        conn, addr = s.accept()
        with conn:
            print(f"Nawiązano połączenie z: {addr}")
            while True:
                # Odbieranie przesłanych danych
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Otrzymano dane przez WiFi: {data.decode('utf-8')}")
                
    print("Dezaktywacja urządzenia: serwer wyłączony.")

if __name__ == "__main__":
    start_server()
