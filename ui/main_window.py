"""
ui/main_window.py - Ventana principal con menú lateral
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os, threading, datetime

BG_DARK   = "#0D1117"
BG_CARD   = "#161B22"
BG_SIDEBAR= "#010409"
ACCENT    = "#00D4FF"
ACCENT2   = "#238636"
TEXT      = "#E6EDF3"
TEXT_DIM  = "#8B949E"
WARNING   = "#D29922"
DANGER    = "#FF4C4C"
SUCCESS   = "#3FB950"
BORDER    = "#30363D"


class MainWindow:
    def __init__(self, root, db, user):
        self.root = root
        self.db = db
        self.user = user
        self.active_module = None

        root.title("Sistema de Inventario Industrial")
        root.configure(bg=BG_DARK)
        w, h = 1280, 780
        x = (root.winfo_screenwidth() - w) // 2
        y = (root.winfo_screenheight() - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.minsize(1100, 680)

        self._build_layout()
        self._load_module("dashboard")
        self._schedule_backup()

    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=BG_SIDEBAR, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / brand
        brand = tk.Frame(self.sidebar, bg=BG_SIDEBAR, pady=20)
        brand.pack(fill="x")
        tk.Label(brand, text="⚙ INVENTARIO", font=("Arial", 13, "bold"),
                 bg=BG_SIDEBAR, fg=ACCENT).pack()
        tk.Label(brand, text="Sistema Industrial", font=("Arial", 8),
                 bg=BG_SIDEBAR, fg=TEXT_DIM).pack()

        sep = tk.Frame(self.sidebar, bg=BORDER, height=1)
        sep.pack(fill="x", padx=10, pady=8)

        # Nav items
        self.nav_buttons = {}
        nav_items = [
            ("📊", "Dashboard",     "dashboard"),
            ("📥", "Entradas",      "entradas"),
            ("📤", "Salidas",       "salidas"),
            ("📦", "Inventario",    "inventario"),
            ("🔔", "Alertas",       "alertas"),
            ("📈", "Reportes",      "reportes"),
        ]
        for icon, label, key in nav_items:
            btn = self._sidebar_btn(icon, label, key)
            self.nav_buttons[key] = btn

        sep2 = tk.Frame(self.sidebar, bg=BORDER, height=1)
        sep2.pack(fill="x", padx=10, pady=8, side="bottom")

        # User info at bottom
        user_frame = tk.Frame(self.sidebar, bg=BG_SIDEBAR, pady=10)
        user_frame.pack(side="bottom", fill="x")
        tk.Label(user_frame, text=f"👤 {self.user['nombre']}", font=("Arial", 9),
                 bg=BG_SIDEBAR, fg=TEXT).pack()
        tk.Label(user_frame, text=self.user['rol'].upper(), font=("Arial", 8),
                 bg=BG_SIDEBAR, fg=TEXT_DIM).pack()
        tk.Button(user_frame, text="Cerrar Sesión", font=("Arial", 8),
                  bg=BORDER, fg=TEXT_DIM, relief="flat", command=self._logout,
                  cursor="hand2").pack(pady=(6,0))

        # Main content area
        self.content = tk.Frame(self.root, bg=BG_DARK)
        self.content.pack(side="right", fill="both", expand=True)

        # Top bar
        topbar = tk.Frame(self.content, bg=BG_CARD, height=50)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        self.lbl_section = tk.Label(topbar, text="Dashboard", font=("Arial", 14, "bold"),
                                    bg=BG_CARD, fg=TEXT)
        self.lbl_section.pack(side="left", padx=20)

        self.lbl_time = tk.Label(topbar, text="", font=("Arial", 9), bg=BG_CARD, fg=TEXT_DIM)
        self.lbl_time.pack(side="right", padx=20)
        self._update_clock()

        self.alert_badge = tk.Label(topbar, text="", font=("Arial", 9, "bold"),
                                    bg=DANGER, fg="white", padx=8, pady=2)
        # Se muestra solo si hay alertas

        # Module frame
        self.module_frame = tk.Frame(self.content, bg=BG_DARK)
        self.module_frame.pack(fill="both", expand=True, padx=16, pady=12)

    def _sidebar_btn(self, icon, label, key):
        frame = tk.Frame(self.sidebar, bg=BG_SIDEBAR, cursor="hand2")
        frame.pack(fill="x", padx=8, pady=1)

        lbl = tk.Label(frame, text=f"  {icon}  {label}", font=("Arial", 10),
                       bg=BG_SIDEBAR, fg=TEXT_DIM, anchor="w", padx=8, pady=10)
        lbl.pack(fill="x")

        def on_click(k=key, f=frame, l=lbl):
            self._load_module(k)

        def on_enter(e, f=frame, l=lbl):
            if self.active_module != key:
                f.config(bg="#1C2128")
                l.config(bg="#1C2128")

        def on_leave(e, k=key, f=frame, l=lbl):
            if self.active_module != k:
                f.config(bg=BG_SIDEBAR)
                l.config(bg=BG_SIDEBAR)

        frame.bind("<Button-1>", lambda e, k=key: self._load_module(k))
        lbl.bind("<Button-1>", lambda e, k=key: self._load_module(k))
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)

        return (frame, lbl)

    def _load_module(self, key):
        # Reset previous active
        if self.active_module and self.active_module in self.nav_buttons:
            f, l = self.nav_buttons[self.active_module]
            f.config(bg=BG_SIDEBAR)
            l.config(bg=BG_SIDEBAR, fg=TEXT_DIM)

        self.active_module = key

        # Highlight active
        f, l = self.nav_buttons[key]
        f.config(bg="#1C2128")
        l.config(bg="#1C2128", fg=ACCENT)

        # Clear module frame
        for w in self.module_frame.winfo_children():
            w.destroy()

        # Section title
        titles = {
            "dashboard": "📊 Dashboard",
            "entradas": "📥 Entradas de Inventario",
            "salidas": "📤 Salidas de Inventario",
            "inventario": "📦 Inventario General",
            "alertas": "🔔 Alertas del Sistema",
            "reportes": "📈 Reportes y Analíticas",
        }
        self.lbl_section.config(text=titles.get(key, key))

        # Load the module
        if key == "dashboard":
            from modules.dashboard import DashboardModule
            DashboardModule(self.module_frame, self.db, self)
        elif key == "entradas":
            from modules.entradas import EntradasModule
            EntradasModule(self.module_frame, self.db, self.user)
        elif key == "salidas":
            from modules.salidas import SalidasModule
            SalidasModule(self.module_frame, self.db, self.user)
        elif key == "inventario":
            from modules.inventario import InventarioModule
            InventarioModule(self.module_frame, self.db, self.user)
        elif key == "alertas":
            from modules.alertas import AlertasModule
            AlertasModule(self.module_frame, self.db)
        elif key == "reportes":
            from modules.reportes import ReportesModule
            ReportesModule(self.module_frame, self.db)

    def _update_clock(self):
        now = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
        self.lbl_time.config(text=now)
        self.root.after(1000, self._update_clock)

    def _schedule_backup(self):
        """Backup automático cada 30 minutos."""
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db.hacer_backup(os.path.join(base, "backups"))
        self.root.after(1800000, self._schedule_backup)

    def _logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Desea cerrar sesión?"):
            self.root.destroy()

    def refresh_alerts_badge(self):
        count = self.db.get_stats()["alertas_pendientes"]
        if count > 0:
            self.alert_badge.config(text=f"🔔 {count} alertas")
            self.alert_badge.pack(side="right", padx=(0, 10))
        else:
            self.alert_badge.pack_forget()
