import tkinter as tk
import socket
import subprocess

def wlacz_wifi():
    # Odblokowuje kartę sieciową w systemach Linux (Raspberry Pi)
    try:
        subprocess.run(["rfkill", "unblock", "wifi"], check=True)
        status.config(text="WiFi włączone", fg="green")
    except Exception as e:
        status.config(text=f"Błąd włączania WiFi: {e}", fg="red")

def wylacz_wifi():
    # Blokuje kartę sieciową w systemach Linux
    try:
        subprocess.run(["rfkill", "block", "wifi"], check=True)
        status.config(text="WiFi wyłączone", fg="orange")
    except Exception as e:
        status.config(text=f"Błąd wyłączania WiFi: {e}", fg="red")

def polacz_i_wyslij():
    ip = pole_ip.get()
    port = int(pole_port.get())
    wiadomosc = pole_wiadomosc.get()
    
    # Tworzenie gniazda TCP i wysyłanie danych
    try:
        klient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        klient.connect((ip, port))
        klient.send(wiadomosc.encode('utf-8'))
        klient.close()
        status.config(text="Połączono i wysłano pomyślnie!", fg="green")
    except Exception as e:
        status.config(text=f"Błąd połączenia: {e}", fg="red")

# Tworzenie głównego okna GUI
root = tk.Tk()
root.title("Transmisja WiFi - CW 14")
root.geometry("300x350")

tk.Label(root, text="Sterowanie WiFi").pack(pady=5)
tk.Button(root, text="Włącz WiFi", command=wlacz_wifi, width=15).pack()
tk.Button(root, text="Wyłącz WiFi", command=wylacz_wifi, width=15).pack()

tk.Label(root, text="\nIP docelowe:").pack()
pole_ip = tk.Entry(root)
pole_ip.pack()
pole_ip.insert(0, "192.168.1.100") # Przykładowe IP do zmiany

tk.Label(root, text="Port docelowy:").pack()
pole_port = tk.Entry(root)
pole_port.pack()
pole_port.insert(0, "5000") # Przykładowy port

tk.Label(root, text="Wiadomość:").pack()
pole_wiadomosc = tk.Entry(root)
pole_wiadomosc.pack()
pole_wiadomosc.insert(0, "Test transmisji WiFi")

tk.Label(root, text="").pack()
tk.Button(root, text="Połącz i Wyślij", command=polacz_i_wyslij, bg="lightblue").pack(pady=10)

status = tk.Label(root, text="Oczekiwanie...", fg="gray")
status.pack(pady=10)

root.mainloop()