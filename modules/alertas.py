"""
modules/alertas.py - Módulo de alertas del sistema
"""
import tkinter as tk
from tkinter import ttk

BG_DARK  = "#0D1117"
BG_CARD  = "#161B22"
ACCENT   = "#00D4FF"
TEXT     = "#E6EDF3"
TEXT_DIM = "#8B949E"
SUCCESS  = "#3FB950"
DANGER   = "#FF4C4C"
WARNING  = "#D29922"
ORANGE   = "#FFA500"
BORDER   = "#30363D"


class AlertasModule:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self._build()

    def _build(self):
        top = tk.Frame(self.parent, bg=BG_DARK)
        top.pack(fill="x", pady=(0, 10))

        tk.Label(top, text="Alertas activas del inventario — productos que requieren atención",
                 font=("Arial", 10), bg=BG_DARK, fg=TEXT_DIM).pack(side="left")

        tk.Button(top, text="✅ Marcar Todas como Leídas", font=("Arial", 9),
                  bg=SUCCESS, fg=BG_DARK, relief="flat", cursor="hand2",
                  command=self._mark_all_read, padx=10).pack(side="right")

        tk.Button(top, text="🔄 Actualizar", font=("Arial", 9),
                  bg=BORDER, fg=TEXT_DIM, relief="flat", cursor="hand2",
                  command=self._load, padx=8).pack(side="right", padx=6)

        # Summary cards
        stats = self.db.get_stats()
        cards_frame = tk.Frame(self.parent, bg=BG_DARK)
        cards_frame.pack(fill="x", pady=(0, 12))

        for label, val, color in [
            ("AGOTADOS", stats["agotados"], DANGER),
            ("CRÍTICOS", stats["criticos"], WARNING),
            ("STOCK BAJO", stats["bajos"], ORANGE),
            ("ALERTAS PENDIENTES", stats["alertas_pendientes"], ACCENT),
        ]:
            f = tk.Frame(cards_frame, bg=BG_CARD, padx=18, pady=14)
            f.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(f, text=str(val), font=("Arial", 28, "bold"), bg=BG_CARD, fg=color).pack()
            tk.Label(f, text=label, font=("Arial", 9), bg=BG_CARD, fg=TEXT_DIM).pack()
            tk.Frame(f, bg=color, height=3).pack(fill="x", side="bottom", pady=(8,0))

        # Tabla alertas
        frame = tk.Frame(self.parent, bg=BG_CARD, padx=8, pady=8)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="🔔 HISTORIAL DE ALERTAS", font=("Arial", 10, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(0, 8))

        cols = ("Fecha", "Tipo", "Fabricante", "Referencia", "Mensaje", "Leída")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=14)

        style = ttk.Style()
        style.configure("Treeview", background=BG_CARD, foreground=TEXT,
                         fieldbackground=BG_CARD, rowheight=26)
        style.configure("Treeview.Heading", background="#21262D", foreground=TEXT_DIM,
                         font=("Arial", 9, "bold"))
        style.map("Treeview", background=[("selected", "#1F6FEB")])

        self.tree.tag_configure("AGOTADO", foreground=DANGER)
        self.tree.tag_configure("CRITICO", foreground=WARNING)
        self.tree.tag_configure("BAJO", foreground=ORANGE)
        self.tree.tag_configure("leida", foreground=TEXT_DIM)

        widths = [140, 80, 100, 110, 280, 60]
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w)

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Productos agotados/críticos
        bottom = tk.Frame(self.parent, bg=BG_CARD, padx=8, pady=8)
        bottom.pack(fill="x", pady=(8, 0))

        tk.Label(bottom, text="📋 PRODUCTOS QUE REQUIEREN REPOSICIÓN", font=("Arial", 10, "bold"),
                 bg=BG_CARD, fg=DANGER).pack(anchor="w", pady=(0, 6))

        cols2 = ("Fabricante", "Referencia", "Stock Actual", "Stock Mínimo", "Stock Crítico", "Estado")
        tree2 = ttk.Treeview(bottom, columns=cols2, show="headings", height=6)
        tree2.tag_configure("agotado", foreground=DANGER)
        tree2.tag_configure("critico", foreground=WARNING)
        tree2.tag_configure("bajo", foreground=ORANGE)

        for c in cols2:
            tree2.heading(c, text=c)
            tree2.column(c, width=130)

        items = self.db.get_inventario()
        for row in items:
            qty = row["cantidad"]
            if qty == 0:
                tag, estado = "agotado", "AGOTADO"
            elif qty <= row["stock_critico"]:
                tag, estado = "critico", "CRÍTICO"
            elif qty <= row["stock_minimo"]:
                tag, estado = "bajo", "BAJO"
            else:
                continue
            tree2.insert("", "end", tags=(tag,),
                         values=(row["fabricante"], row["referencia"],
                                 qty, row["stock_minimo"], row["stock_critico"], estado))

        sb2 = ttk.Scrollbar(bottom, orient="vertical", command=tree2.yview)
        tree2.configure(yscrollcommand=sb2.set)
        tree2.pack(side="left", fill="both", expand=True)
        sb2.pack(side="right", fill="y")

        self._load()

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        alertas = self.db.get_alertas(solo_no_leidas=False)
        for a in alertas:
            tag = a["tipo"] if not a["leida"] else "leida"
            self.tree.insert("", "end", tags=(tag,), values=(
                a["fecha"][:16], a["tipo"],
                a["fabricante"] or "", a["referencia"] or "",
                a["mensaje"], "Sí" if a["leida"] else "No"
            ))

    def _mark_all_read(self):
        self.db.marcar_alertas_leidas()
        self._load()
