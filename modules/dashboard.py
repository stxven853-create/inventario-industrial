"""
modules/dashboard.py - Panel principal con estadísticas
"""
import tkinter as tk
from tkinter import ttk

BG_DARK  = "#0D1117"
BG_CARD  = "#161B22"
ACCENT   = "#00D4FF"
TEXT     = "#E6EDF3"
TEXT_DIM = "#8B949E"
WARNING  = "#D29922"
DANGER   = "#FF4C4C"
SUCCESS  = "#3FB950"
BORDER   = "#30363D"


def card(parent, title, value, subtitle, color, icon):
    f = tk.Frame(parent, bg=BG_CARD, padx=20, pady=18)
    f.pack(side="left", fill="both", expand=True, padx=6)

    top = tk.Frame(f, bg=BG_CARD)
    top.pack(fill="x")
    tk.Label(top, text=icon, font=("Arial", 22), bg=BG_CARD, fg=color).pack(side="left")
    tk.Label(top, text=title, font=("Arial", 9), bg=BG_CARD, fg=TEXT_DIM).pack(side="right", anchor="ne", pady=4)

    tk.Label(f, text=str(value), font=("Arial", 28, "bold"), bg=BG_CARD, fg=color).pack(anchor="w", pady=(6,0))
    tk.Label(f, text=subtitle, font=("Arial", 9), bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")

    # Bottom accent line
    tk.Frame(f, bg=color, height=3).pack(fill="x", side="bottom", pady=(10, 0))


class DashboardModule:
    def __init__(self, parent, db, main_win):
        self.parent = parent
        self.db = db
        self.main_win = main_win
        self._build()

    def _build(self):
        stats = self.db.get_stats()

        # ─── Fila de tarjetas ──────────────────────────────────────────────
        row1 = tk.Frame(self.parent, bg=BG_DARK)
        row1.pack(fill="x", pady=(0, 12))

        card(row1, "TOTAL PRODUCTOS", stats["total_items"], "Referencias en inventario", ACCENT, "📦")
        card(row1, "VALOR TOTAL", f"${stats['valor_total']:,.0f}", "Valorización del inventario", SUCCESS, "💰")
        card(row1, "STOCK BAJO", stats["bajos"], "Productos con stock bajo", WARNING, "⚠️")
        card(row1, "CRÍTICOS / AGOTADOS", f"{stats['criticos']} / {stats['agotados']}", "Requieren reposición urgente", DANGER, "🚨")

        # ─── Sección inferior ────────────────────────────────────────────
        bottom = tk.Frame(self.parent, bg=BG_DARK)
        bottom.pack(fill="both", expand=True)

        # Productos críticos
        left = tk.Frame(bottom, bg=BG_CARD, padx=12, pady=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        tk.Label(left, text="🚨 PRODUCTOS CRÍTICOS / AGOTADOS", font=("Arial", 10, "bold"),
                 bg=BG_CARD, fg=DANGER).pack(anchor="w", pady=(0, 8))

        cols = ("Fabricante", "Referencia", "Cantidad", "Estado")
        tree = ttk.Treeview(left, columns=cols, show="headings", height=12)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG_CARD, foreground=TEXT,
                         fieldbackground=BG_CARD, rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background="#21262D", foreground=TEXT_DIM,
                         font=("Arial", 9, "bold"))
        style.map("Treeview", background=[("selected", "#1F6FEB")])

        tree.tag_configure("agotado", foreground=DANGER)
        tree.tag_configure("critico", foreground=WARNING)
        tree.tag_configure("bajo", foreground="#FFA500")

        items = self.db.get_inventario()
        for row in items:
            qty = row["cantidad"]
            sc = row["stock_critico"]
            sm = row["stock_minimo"]
            if qty == 0:
                tag, estado = "agotado", "AGOTADO"
            elif qty <= sc:
                tag, estado = "critico", "CRÍTICO"
            elif qty <= sm:
                tag, estado = "bajo", "BAJO"
            else:
                continue
            tree.insert("", "end", values=(row["fabricante"], row["referencia"], qty, estado), tags=(tag,))

        tree.pack(fill="both", expand=True)

        # Consumo por máquina
        right = tk.Frame(bottom, bg=BG_CARD, padx=12, pady=12)
        right.pack(side="right", fill="both", expand=True, padx=(6, 0))

        tk.Label(right, text="🔧 CONSUMO POR MÁQUINA / ÁREA", font=("Arial", 10, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(0, 8))

        maquinas = self.db.get_consumo_por_maquina()
        if not maquinas:
            tk.Label(right, text="Sin datos de salidas aún.\nRegistre salidas para ver estadísticas.",
                     font=("Arial", 10), bg=BG_CARD, fg=TEXT_DIM, justify="center").pack(expand=True)
        else:
            cols2 = ("Máquina / Área", "Costo Consumido", "Movimientos")
            t2 = ttk.Treeview(right, columns=cols2, show="headings", height=12)
            for c in cols2:
                t2.heading(c, text=c)
                t2.column(c, width=100)
            for row in maquinas:
                t2.insert("", "end", values=(row["maquina"], f"${row['total_costo']:,.0f}", row["n_movimientos"]))
            t2.pack(fill="both", expand=True)

        # Botón actualizar
        tk.Button(self.parent, text="🔄 Actualizar Dashboard", font=("Arial", 9),
                  bg=BG_CARD, fg=TEXT_DIM, relief="flat", cursor="hand2",
                  command=self._refresh).pack(pady=(10, 0))

    def _refresh(self):
        for w in self.parent.winfo_children():
            w.destroy()
        self._build()
