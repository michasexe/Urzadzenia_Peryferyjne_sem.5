import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import serial
import threading
import time
import os
from xmodem import XMODEM

# zmienne globalne
ser = None
flaga_nasluchu = False

# funkcje pomocnicze dla XModem
def getc(size, timeout=1):
    ser.timeout = timeout
    return ser.read(size) or None

def putc(data, timeout=1):
    return ser.write(data)

def wyslij_plik_xmodem():
    if not ser or not ser.is_open:
        logi.insert(tk.END, "[BŁĄD] Brak połączenia z portem!\n")
        return

    sciezka = filedialog.askopenfilename(title="Wybierz plik do wysłania")
    if not sciezka:
        return

    def proces_wysylania():
        global flaga_nasluchu
        flaga_nasluchu = False
        time.sleep(0.5)
        
        okno.after(0, lambda: aktualizuj_logi(f"[XMODEM] Wysyłanie: {os.path.basename(sciezka)}...\n"))
        
        try:
            modem = XMODEM(getc, putc)
            with open(sciezka, 'rb') as stream:
                status = modem.send(stream)
                
            if status:
                okno.after(0, lambda: aktualizuj_logi("[XMODEM] Plik wysłany pomyślnie!\n"))
            else:
                okno.after(0, lambda: aktualizuj_logi("[XMODEM] Nie udało się wysłać pliku.\n"))
        except Exception as e:
            okno.after(0, lambda: aktualizuj_logi(f"[XMODEM BŁĄD] {e}\n"))
        finally:

            flaga_nasluchu = True
            threading.Thread(target=nasluchuj_port, daemon=True).start()

    threading.Thread(target=proces_wysylania, daemon=True).start()

def odbierz_plik_xmodem():
    if not ser or not ser.is_open:
        logi.insert(tk.END, "[BŁĄD] Brak połączenia z portem!\n")
        return

    sciezka = filedialog.asksaveasfilename(title="Gdzie zapisać odebrany plik?")
    if not sciezka:
        return

    def proces_odbierania():
        global flaga_nasluchu
        flaga_nasluchu = False
        time.sleep(0.5)
        
        okno.after(0, lambda: aktualizuj_logi("[XMODEM] Oczekiwanie na plik od drugiego modemu...\n"))
        
        try:
            modem = XMODEM(getc, putc)
            with open(sciezka, 'wb') as stream:
                status = modem.recv(stream)
                
            if status:
                okno.after(0, lambda: aktualizuj_logi(f"[XMODEM] Plik odebrany i zapisany jako {os.path.basename(sciezka)}!\n"))
            else:
                okno.after(0, lambda: aktualizuj_logi("[XMODEM] Błąd podczas odbierania pliku.\n"))
        except Exception as e:
            okno.after(0, lambda: aktualizuj_logi(f"[XMODEM BŁĄD] {e}\n"))
        finally:
            flaga_nasluchu = True
            threading.Thread(target=nasluchuj_port, daemon=True).start()

    threading.Thread(target=proces_odbierania, daemon=True).start()

def otworz_port():
    global ser, flaga_nasluchu
    if ser is not None and ser.is_open:
        logi.insert(tk.END, "[SYSTEM] Port jest już otwarty.\n")
        return
        
    try:
        wybrany_port = pola_wyboru["Port COM:"].get()
        wybrana_predkosc = int(pola_wyboru["Prędkość:"].get())
        
        bity_danych = pola_wyboru["Bity danych:"].get()
        rozmiar_bajtu = serial.EIGHTBITS if bity_danych == "8" else serial.SEVENBITS
        
        parzystosc_wybor = pola_wyboru["Parzystość:"].get()
        if parzystosc_wybor == "None": parzystosc = serial.PARITY_NONE
        elif parzystosc_wybor == "Even": parzystosc = serial.PARITY_EVEN
        elif parzystosc_wybor == "Odd": parzystosc = serial.PARITY_ODD
        else: parzystosc = serial.PARITY_NONE
            
        stop_wybor = pola_wyboru["Bity stopu:"].get()
        if stop_wybor == "1": bity_stopu = serial.STOPBITS_ONE
        elif stop_wybor == "2": bity_stopu = serial.STOPBITS_TWO
        else: bity_stopu = serial.STOPBITS_ONE_POINT_FIVE

        ser = serial.Serial(
            port=wybrany_port,
            baudrate=wybrana_predkosc,
            bytesize=rozmiar_bajtu,
            parity=parzystosc,
            stopbits=bity_stopu,
            timeout=1
        )
        
        logi.insert(tk.END, f"[SYSTEM] Połączono z portem {wybrany_port}\n")
        logi.see(tk.END)
        
        flaga_nasluchu = True
        watek = threading.Thread(target=nasluchuj_port, daemon=True)
        watek.start()
        
    except Exception as e:
        logi.insert(tk.END, f"[BŁĄD PORTU] {e}\n")

def zamknij_port():
    global ser, flaga_nasluchu
    if ser is not None and ser.is_open:
        flaga_nasluchu = False
        time.sleep(0.5) 
        ser.close()
        logi.insert(tk.END, "[SYSTEM] Rozłączono z portem.\n")
        logi.see(tk.END)

def nasluchuj_port():
    global ser, flaga_nasluchu
    while flaga_nasluchu:
        if ser and ser.is_open and ser.in_waiting > 0:
            try:
                dane = ser.read(ser.in_waiting).decode('ascii', errors='ignore')
                okno.after(0, lambda d=dane: aktualizuj_logi(d))
            except Exception:
                pass
        time.sleep(0.1)

def aktualizuj_logi(tekst):
    logi.insert(tk.END, tekst)
    logi.see(tk.END)

def dzwon_atd():
    if ser and ser.is_open:
        numer = pole_numer.get()
        komenda = f"ATD{numer}\r\n"
        ser.write(komenda.encode('ascii'))
        logi.insert(tk.END, f"[SYSTEM] Nawiązywanie połączenia z {numer}...\n")
        logi.see(tk.END)
    else:
        logi.insert(tk.END, "[BŁĄD] Brak połączenia z portem!\n")

def odbierz_ata():
    if ser and ser.is_open:
        ser.write(b"ATA\r\n")
        logi.insert(tk.END, "[SYSTEM] Odbieranie...\n")
        logi.see(tk.END)

def zerwij_ath():
    if ser and ser.is_open:
        ser.write(b"+++")
        time.sleep(1)
        ser.write(b"ATH\r\n")
        time.sleep(0.5)
        ser.write(b"ATH\r\n")
        logi.insert(tk.END, "[SYSTEM] Połączenie zakończone\n")
        logi.see(tk.END)

def wyslij_wiadomosc():
    if ser and ser.is_open:
        wiadomosc = pole_wiadomosc.get()
        if wiadomosc:
            komenda = wiadomosc + "\r\n"
            ser.write(komenda.encode('ascii'))
            logi.insert(tk.END, f"-> {wiadomosc}\n")
            pole_wiadomosc.delete(0, tk.END)
            logi.see(tk.END)
    else:
        logi.insert(tk.END, "[BŁĄD] Brak połączenia z portem!\n")

okno = tk.Tk()
okno.title("Komunikator Modemowy")
okno.geometry("800x550")
okno.configure(padx=10, pady=10)

# ustawienia portu
ramka_port = tk.LabelFrame(okno, text="Konfiguracja Połączenia", padx=10, pady=10)
ramka_port.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

ustawienia = [
    ("Port COM:", ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6"]),
    ("Prędkość:", ["300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]),
    ("Bity danych:", ["5", "6", "7", "8"]),
    ("Bity stopu:", ["1", "1.5", "2"]),
    ("Parzystość:", ["None", "Even", "Odd", "Mark", "Space"]),
    ("Przepływ:", ["None", "XOnXOff", "RequestToSend", "RequestToSendXOnXOff"])
]

pola_wyboru = {}
for i, (etykieta_tekst, wartosci) in enumerate(ustawienia):
    tk.Label(ramka_port, text=etykieta_tekst).grid(row=i, column=0, sticky="w", pady=2)
    cb = ttk.Combobox(ramka_port, values=wartosci, width=22, state="readonly")
    if etykieta_tekst == "Prędkość:": cb.current(4) 
    elif etykieta_tekst == "Bity danych:": cb.current(3) 
    else: cb.current(0)
    cb.grid(row=i, column=1, padx=5, pady=2)
    pola_wyboru[etykieta_tekst] = cb

tk.Button(ramka_port, text="Otwórz Port", command=otworz_port, width=12, bg="lightgreen").grid(row=6, column=0, pady=10)
tk.Button(ramka_port, text="Zamknij Port", command=zamknij_port, width=12, bg="salmon").grid(row=6, column=1, pady=10)

# sterowanie modemem
ramka_sterowanie = tk.LabelFrame(okno, text="Sterowanie Modemem", padx=10, pady=10)
ramka_sterowanie.grid(row=0, column=1, sticky="ne", padx=5, pady=5)

tk.Label(ramka_sterowanie, text="Numer (Modem B):").grid(row=0, column=0, sticky="w", pady=2)
pole_numer = tk.Entry(ramka_sterowanie, width=15)
pole_numer.grid(row=0, column=1, padx=5, pady=2)

tk.Button(ramka_sterowanie, text="Zadzwoń (ATD)", command=dzwon_atd, width=15).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(ramka_sterowanie, text="Odbierz (ATA)", command=odbierz_ata, width=15).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(ramka_sterowanie, text="Zerwij (+++ / ATH)", command=zerwij_ath, width=15).grid(row=3, column=0, columnspan=2, pady=5)

# komunikacja i logi
ramka_czat = tk.LabelFrame(okno, text="Wymiana Wiadomości i Plików", padx=10, pady=10)
ramka_czat.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

okno.grid_columnconfigure(1, weight=1)
okno.grid_rowconfigure(1, weight=1)
ramka_czat.grid_columnconfigure(0, weight=1)
ramka_czat.grid_rowconfigure(1, weight=1)

ramka_wysylanie = tk.Frame(ramka_czat)
ramka_wysylanie.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

tk.Label(ramka_wysylanie, text="Wiadomość:").pack(side=tk.LEFT)
pole_wiadomosc = tk.Entry(ramka_wysylanie)
pole_wiadomosc.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

okno.bind('<Return>', lambda event: wyslij_wiadomosc())
przycisk_wyslij = tk.Button(ramka_wysylanie, text="Wyślij Teks", command=wyslij_wiadomosc, width=10)
przycisk_wyslij.pack(side=tk.LEFT, padx=5)

przycisk_wyslij_plik = tk.Button(ramka_wysylanie, text="Wyślij Plik", command=wyslij_plik_xmodem, width=10)
przycisk_wyslij_plik.pack(side=tk.LEFT, padx=5)

przycisk_odbierz_plik = tk.Button(ramka_wysylanie, text="Odbierz Plik", command=odbierz_plik_xmodem, width=10)
przycisk_odbierz_plik.pack(side=tk.LEFT, padx=5)

tk.Label(ramka_czat, text="Pełny Log:").grid(row=1, column=0, sticky="nw")
logi = scrolledtext.ScrolledText(ramka_czat, height=12, font=("Consolas", 9))
logi.grid(row=2, column=0, columnspan=2, sticky="nsew")
logi.insert(tk.END, "--- Aplikacja gotowa do pracy (Wsparcie XModem dodane) ---\n")

def zamknij_aplikacje():
    zamknij_port()
    okno.destroy()

okno.protocol("WM_DELETE_WINDOW", zamknij_aplikacje)
okno.mainloop()
