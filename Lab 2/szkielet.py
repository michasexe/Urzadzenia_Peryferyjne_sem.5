import tkinter as tk
from tkinter import ttk, scrolledtext

def otworz_port():
    global ser
    
    # Sprawdzenie, czy port nie jest przypadkiem już otwarty
    if ser is not None and ser.is_open:
        logi.insert(tk.END, "[INFO] Port jest już otwarty.\n")
        logi.see(tk.END)
        return
        
    try:
        # Odczytywanie wartości bezpośrednio z interfejsu (lewa ramka)
        wybrany_port = pola_wyboru["Port COM:"].get()
        wybrana_predkosc = int(pola_wyboru["Prędkość:"].get())
        
        # Odczyt bitów danych (pyserial używa do tego specjalnych stałych)
        bity = pola_wyboru["Bity danych:"].get()
        if bity == "8":
            rozmiar_bajtu = serial.EIGHTBITS
        elif bity == "7":
            rozmiar_bajtu = serial.SEVENBITS
        elif bity == "6":
            rozmiar_bajtu = serial.SIXBITS
        else:
            rozmiar_bajtu = serial.FIVEBITS
            
        # Nawiązywanie połączenia
        ser = serial.Serial(
            port=wybrany_port,
            baudrate=wybrana_predkosc,
            bytesize=rozmiar_bajtu,
            timeout=1
        )
        
        # Wypisanie komunikatu w głównym oknie logów
        logi.insert(tk.END, f"[SUKCES] Otwarto {wybrany_port} z prędkością {wybrana_predkosc} bd.\n")
        logi.see(tk.END)
        
    except serial.SerialException as e:
        # Przechwycenie błędu (np. gdy port jest zajęty lub nie istnieje)
        logi.insert(tk.END, f"[BŁĄD PORTU] {e}\n")
        logi.see(tk.END)
    except Exception as e:
        logi.insert(tk.END, f"[BŁĄD] {e}\n")
        logi.see(tk.END)

okno = tk.Tk()
okno.title("Komunikator Modemowy")
okno.geometry("750x550")
okno.configure(padx=10, pady=10)

ramka_port = tk.LabelFrame(okno, text="Konfiguracja Połączenia", padx=10, pady=10)
ramka_port.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

ustawienia = [
    ("Port COM:", ["COM1", "COM2", "COM3", "COM4"]),
    ("Prędkość:", ["300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]),
    ("Bity danych:", ["5", "6", "7", "8"]),
    ("Bity stopu:", ["1", "1.5", "2"]),
    ("Parzystość:", ["None", "Even", "Odd", "Mark", "Space"]),
    ("Przepływ:", ["None", "XOnXOff", "RequestToSend", "RequestToSendXOnXOff"])
]

# generowanie pól ustawień z listy
pola_wyboru = {}
for i, (etykieta_tekst, wartosci) in enumerate(ustawienia):
    tk.Label(ramka_port, text=etykieta_tekst).grid(row=i, column=0, sticky="w", pady=2)
    cb = ttk.Combobox(ramka_port, values=wartosci, width=20, state="readonly")
    cb.current(0) # ustawienie domyślnej wartości
    cb.grid(row=i, column=1, padx=5, pady=2)
    pola_wyboru[etykieta_tekst] = cb

# łączenie z portem
tk.Button(ramka_port, text="Otwórz Port", command=otworz_port, width=12).grid(row=6, column=0, pady=10)
tk.Button(ramka_port, text="Zamknij Port", command=otworz_port, width=12).grid(row=6, column=1, pady=10)

# sterowanie modemem
ramka_sterowanie = tk.LabelFrame(okno, text="Sterowanie Modemem", padx=10, pady=10)
ramka_sterowanie.grid(row=0, column=1, sticky="ne", padx=5, pady=5)

tk.Label(ramka_sterowanie, text="Numer (Modem B):").grid(row=0, column=0, sticky="w", pady=2)
pole_numer = tk.Entry(ramka_sterowanie, width=15)
pole_numer.grid(row=0, column=1, padx=5, pady=2)

tk.Button(ramka_sterowanie, text="Zadzwoń (ATD)", command=akcja_testowa, width=15).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(ramka_sterowanie, text="Odbierz (ATA)", command=akcja_testowa, width=15).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(ramka_sterowanie, text="Zerwij (+++ / ATH)", command=akcja_testowa, width=15).grid(row=3, column=0, columnspan=2, pady=5)


ramka_czat = tk.LabelFrame(okno, text="Wymiana Wiadomości", padx=10, pady=10)
ramka_czat.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

okno.grid_columnconfigure(1, weight=1)
okno.grid_rowconfigure(1, weight=1)
ramka_czat.grid_columnconfigure(0, weight=1)
ramka_czat.grid_rowconfigure(1, weight=1)

# pasek wysyłania wiadomości
ramka_wysylanie = tk.Frame(ramka_czat)
ramka_wysylanie.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

tk.Label(ramka_wysylanie, text="Wiadomość:").pack(side=tk.LEFT)
pole_wiadomosc = tk.Entry(ramka_wysylanie)
pole_wiadomosc.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

przycisk_wyslij = tk.Button(ramka_wysylanie, text="Wyślij", command=akcja_testowa, width=10)
przycisk_wyslij.pack(side=tk.RIGHT)

przycisk_plik = tk.Button(ramka_wysylanie, text="Wyślij plik (XModem)", command=akcja_testowa, width=18)
przycisk_plik.pack(side=tk.RIGHT, padx=5)

# okno logów
tk.Label(ramka_czat, text="Pełny Log:").grid(row=1, column=0, sticky="nw")
logi = scrolledtext.ScrolledText(ramka_czat, height=12, font=("Consolas", 9))
logi.grid(row=2, column=0, columnspan=2, sticky="nsew")
logi.insert(tk.END, " Aplikacja uruchomiona \n")

okno.mainloop()
