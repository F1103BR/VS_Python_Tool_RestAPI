import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import webbrowser

def send_request():
    method = method_var.get()
    url = url_entry.get()
    
    if not url:
        messagebox.showwarning("Eingabefehler", "Bitte geben Sie eine URL ein.")
        return

    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url)

        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            webbrowser.open(url)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Die Antwort ist HTML. Die Seite wurde im Browser geöffnet.\n\nStatus Code: {response.status_code}")
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Status Code: {response.status_code}\n\n{response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Fehler", f"Fehler bei der Anfrage: {e}")

def on_enter_key(event):
    send_request()

# Hauptfenster erstellen
root = tk.Tk()
root.title("HTTP Client")
root.geometry("800x600")

# Stil setzen
style = ttk.Style(root)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TCombobox", font=("Helvetica", 12))

# Eingabeframe
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# HTTP Methode Auswahl
method_var = tk.StringVar(value="GET")
method_combobox = ttk.Combobox(input_frame, textvariable=method_var, values=["GET", "POST"], width=10)
method_combobox.grid(row=0, column=0, padx=5, pady=5)

# URL Eingabefeld
url_entry = ttk.Entry(input_frame, width=70)
url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
url_entry.bind("<Return>", on_enter_key)

# Senden Button
send_button = ttk.Button(input_frame, text="Senden", command=send_request)
send_button.grid(row=0, column=2, padx=5, pady=5)
send_button.bind("<Return>", on_enter_key)

# Ergebnis Frame
result_frame = ttk.LabelFrame(root, text="Antwort", padding="10")
result_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

result_text = scrolledtext.ScrolledText(result_frame, height=30)
result_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Grid Konfiguration
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Hauptschleife starten
root.mainloop()
