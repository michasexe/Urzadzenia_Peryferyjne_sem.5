import socket

# Podaj adres IP przypisany do interfejsu Ethernet komputera PC
SERVER_IP = '192.168.1.X'  # Zmień na właściwe IP komputera
PORT = 65432               # Musi zgadzać się z portem na serwerze

def start_client():
    print("Aktywacja urządzenia: Start aplikacji klienta...")
    
    # b). uruchomić oprogramowanie realizujące transmisję WiFi
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # c). realizacja połączenia z wybranym urządzeniem WiFi (z Serwerem PC)
            s.connect((SERVER_IP, PORT))
            print(f"Połączono z serwerem {SERVER_IP} na porcie {PORT}.")
            
            dane_do_wyslania = "Witaj! To sa testowe dane wyslane z Raspberry Pi przez interfejs WiFi."
            
            # c). przesłanie danych za pomocą WiFi
            s.sendall(dane_do_wyslania.encode('utf-8'))
            print("Przesłano dane poprawnie.")
            
        except ConnectionRefusedError:
            print("Nie można się połączyć. Upewnij się, że skrypt serwera na PC jest włączony i IP jest poprawne.")

    # a). wyłączenie urządzenia (automatycznie na wyjściu z bloku with następuje zamknięcie)
    print("Wyjście z programu - dezaktywacja transmisji.")

if __name__ == "__main__":
    start_client()
