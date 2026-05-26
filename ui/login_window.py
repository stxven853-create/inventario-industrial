"""
ui/login_window.py - Ventana de inicio de sesión
"""
import tkinter as tk
from tkinter import ttk, messagebox

# Paleta de colores
BG_DARK = "#0D1117"
BG_CARD = "#161B22"
ACCENT = "#00D4FF"
TEXT = "#E6EDF3"
TEXT_DIM = "#8B949E"
ERROR = "#FF4C4C"
SUCCESS = "#3FB950"


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.authenticated = False
        self.current_user = None

        self.title("SISTEMA DE INVENTARIO INDUSTRIAL")
        self.geometry("480x560")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 480) // 2
        y = (self.winfo_screenheight() - 560) // 2
        self.geometry(f"480x560+{x}+{y}")

        self._build_ui()
        self.grab_set()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", pady=(40, 20))

        tk.Label(header, text="⚙", font=("Arial", 48), bg=BG_DARK, fg=ACCENT).pack()
        tk.Label(header, text="INVENTARIO INDUSTRIAL", font=("Arial", 18, "bold"),
                 bg=BG_DARK, fg=TEXT).pack()
        tk.Label(header, text="Sistema de Gestión de Repuestos", font=("Arial", 10),
                 bg=BG_DARK, fg=TEXT_DIM).pack(pady=(4, 0))

        # Card
        card = tk.Frame(self, bg=BG_CARD, padx=40, pady=30)
        card.pack(fill="x", padx=40)

        tk.Label(card, text="INICIAR SESIÓN", font=("Arial", 13, "bold"),
                 bg=BG_CARD, fg=TEXT).pack(pady=(0, 20))

        # Usuario
        tk.Label(card, text="Usuario", font=("Arial", 10), bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.entry_user = tk.Entry(card, font=("Arial", 12), bg="#21262D", fg=TEXT,
                                   insertbackground=TEXT, relief="flat", bd=8)
        self.entry_user.pack(fill="x", pady=(4, 14), ipady=6)
        self.entry_user.insert(0, "admin")

        # Contraseña
        tk.Label(card, text="Contraseña", font=("Arial", 10), bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.entry_pass = tk.Entry(card, font=("Arial", 12), bg="#21262D", fg=TEXT,
                                   insertbackground=TEXT, relief="flat", bd=8, show="●")
        self.entry_pass.pack(fill="x", pady=(4, 20), ipady=6)
        self.entry_pass.insert(0, "admin123")

        # Mensaje error
        self.lbl_error = tk.Label(card, text="", font=("Arial", 9), bg=BG_CARD, fg=ERROR)
        self.lbl_error.pack()

        # Botón
        btn = tk.Button(card, text="INGRESAR AL SISTEMA", font=("Arial", 11, "bold"),
                        bg=ACCENT, fg=BG_DARK, relief="flat", cursor="hand2",
                        command=self._login, pady=10)
        btn.pack(fill="x", pady=(10, 0))

        self.entry_pass.bind("<Return>", lambda e: self._login())
        self.entry_user.bind("<Return>", lambda e: self.entry_pass.focus())

        # Footer
        tk.Label(self, text="v1.0 — Sistema Industrial de Inventario",
                 font=("Arial", 8), bg=BG_DARK, fg=TEXT_DIM).pack(side="bottom", pady=20)

    def _login(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get().strip()
        if not user or not pwd:
            self.lbl_error.config(text="Complete todos los campos")
            return
        result = self.db.login(user, pwd)
        if result:
            self.authenticated = True
            self.current_user = result
            self.destroy()
        else:
            self.lbl_error.config(text="Usuario o contraseña incorrectos")
            self.entry_pass.delete(0, "end")

    def _on_close(self):
        self.authenticated = False
        self.destroy()
