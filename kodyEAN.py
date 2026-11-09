import tkinter as tk
from tkinter import messagebox
from barcode import EAN13
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import io
import os

def generuj_kod():
    wprowadzone_dane = entry_dane.get().strip()
    
    # EAN13 wymaga 12 początkowych cyfr (13. jest generowana automatycznie jako kontrolna)
    if not wprowadzone_dane.isdigit():
        messagebox.showerror("Błąd", "Wprowadź tylko cyfry!")
        return
        
    if len(wprowadzone_dane) not in [12, 13]:
        messagebox.showerror("Błąd", "Kod EAN-13 wymaga 12 cyfr (13. obliczy się sama) lub podania 13 cyfr.")
        return
    
    # Do biblioteki przekazujemy tylko pierwsze 12 cyfr
    dane_bazowe = wprowadzone_dane[:12]
    
    try:
        # Tworzenie obiektu kodu kreskowego z pisarzem zapisującym jako obraz (ImageWriter)
        moj_kod = EAN13(dane_bazowe, writer=ImageWriter())
        
        # Zapis fizyczny pliku na dysku (bez rozszerzenia, biblioteka doda .png)
        nazwa_pliku = "kod_ean13"
        moj_kod.save(nazwa_pliku)
        
        # Wyświetlanie w interfejsie graficznym przy użyciu wirtualnego bufora
        bufor = io.BytesIO()
        moj_kod.write(bufor)
        bufor.seek(0)
        
        obraz = Image.open(bufor)
        obraz = obraz.resize((350, 200)) # Skalowanie by zmieścił się w oknie
        zdjecie_tk = ImageTk.PhotoImage(obraz)
        
        label_obraz.config(image=zdjecie_tk)
        label_obraz.image = zdjecie_tk # Utrzymanie referencji, by Garbage Collector nie wyczyścił obrazka
        
        label_status.config(text=f"Sukces! Plik zapisany jako: {nazwa_pliku}.png w folderze programu.", fg="green")
        
    except Exception as e:
        messagebox.showerror("Błąd krytyczny", f"Wystąpił błąd: {e}")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Generator Kodów EAN-13")
root.geometry("450x400")

# Elementy GUI
label_instrukcja = tk.Label(root, text="Wprowadź 12 cyfr dla kodu EAN-13:", font=("Arial", 12))
label_instrukcja.pack(pady=10)

entry_dane = tk.Entry(root, font=("Arial", 14), width=20, justify="center")
entry_dane.pack(pady=10)

btn_generuj = tk.Button(root, text="Generuj Kod", font=("Arial", 12, "bold"), command=generuj_kod, bg="#4CAF50", fg="white")
btn_generuj.pack(pady=15)

label_status = tk.Label(root, text="", font=("Arial", 10), wraplength=400)
label_status.pack(pady=5)

label_obraz = tk.Label(root)
label_obraz.pack(pady=10)

# Uruchomienie pętli okna
root.mainloop()
