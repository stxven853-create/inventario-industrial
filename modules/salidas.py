"""
modules/salidas.py - Módulo de salidas de inventario
"""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

BG_DARK  = "#0D1117"
BG_CARD  = "#161B22"
BG_INPUT = "#21262D"
ACCENT   = "#00D4FF"
TEXT     = "#E6EDF3"
TEXT_DIM = "#8B949E"
SUCCESS  = "#3FB950"
DANGER   = "#FF4C4C"
WARNING  = "#D29922"
BORDER   = "#30363D"


def label(parent, text, row, col):
    tk.Label(parent, text=text, font=("Arial", 9), bg=BG_CARD,
             fg=TEXT_DIM).grid(row=row, column=col, sticky="w", padx=(0, 8), pady=3)


def entry(parent, row, col, width=28):
    e = tk.Entry(parent, font=("Arial", 10), bg=BG_INPUT, fg=TEXT,
                 insertbackground=TEXT, relief="flat", bd=6, width=width)
    e.grid(row=row, column=col, sticky="ew", pady=3, padx=(0, 12))
    return e


class SalidasModule:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self._build()

    def _build(self):
        main = tk.Frame(self.parent, bg=BG_DARK)
        main.pack(fill="both", expand=True)

        # ─── Formulario ─────────────────────────────────────────────────────
        form_frame = tk.Frame(main, bg=BG_CARD, padx=24, pady=20)
        form_frame.pack(side="left", fill="y", padx=(0, 12))

        tk.Label(form_frame, text="📤 NUEVA SALIDA", font=("Arial", 11, "bold"),
                 bg=BG_CARD, fg=WARNING).grid(row=0, columnspan=2, sticky="w", pady=(0, 12))

        # Búsqueda rápida
        tk.Label(form_frame, text="Buscar Referencia", font=("Arial", 9),
                 bg=BG_CARD, fg=TEXT_DIM).grid(row=1, column=0, sticky="w", padx=(0,8), pady=3)

        search_frame = tk.Frame(form_frame, bg=BG_CARD)
        search_frame.grid(row=1, column=1, sticky="ew", pady=3)

        self.entry_search = tk.Entry(search_frame, font=("Arial", 10), bg=BG_INPUT, fg=TEXT,
                                     insertbackground=TEXT, relief="flat", bd=6, width=22)
        self.entry_search.pack(side="left")
        tk.Button(search_frame, text="🔍", font=("Arial", 10), bg=BORDER, fg=TEXT,
                  relief="flat", cursor="hand2",
                  command=self._buscar).pack(side="left", padx=4)

        # Info del producto encontrado
        self.lbl_info = tk.Label(form_frame, text="", font=("Arial", 9, "italic"),
                                  bg=BG_CARD, fg=ACCENT)
        self.lbl_info.grid(row=2, columnspan=2, sticky="w", pady=(0, 8))

        fields = [
            ("Fabricante *", "fab"),
            ("Referencia *", "ref"),
            ("Cantidad Retirada *", "cant"),
            ("Máquina donde se usó", "maq"),
            ("Área", "area"),
            ("Técnico Responsable", "tecnico"),
            ("Motivo del Uso", "motivo"),
        ]
        self.entries = {}
        for i, (lbl_text, key) in enumerate(fields, start=3):
            label(form_frame, lbl_text, i, 0)
            self.entries[key] = entry(form_frame, i, 1)

        label(form_frame, "Fecha", len(fields)+3, 0)
        self.entry_fecha = entry(form_frame, len(fields)+3, 1)
        self.entry_fecha.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        label(form_frame, "Observaciones", len(fields)+4, 0)
        self.txt_obs = tk.Text(form_frame, font=("Arial", 10), bg=BG_INPUT, fg=TEXT,
                               insertbackground=TEXT, relief="flat", bd=6, width=28, height=3)
        self.txt_obs.grid(row=len(fields)+4, column=1, sticky="ew", pady=3)

        # Costo calculado
        self.lbl_costo = tk.Label(form_frame, text="Costo estimado: $0",
                                   font=("Arial", 10, "bold"), bg=BG_CARD, fg=WARNING)
        self.lbl_costo.grid(row=len(fields)+5, columnspan=2, sticky="w", pady=6)

        self.entries["cant"].bind("<KeyRelease>", self._calc_costo)

        btn_frame = tk.Frame(form_frame, bg=BG_CARD)
        btn_frame.grid(row=len(fields)+6, columnspan=2, pady=12)

        tk.Button(btn_frame, text="📤  REGISTRAR SALIDA", font=("Arial", 10, "bold"),
                  bg=WARNING, fg=BG_DARK, relief="flat", cursor="hand2",
                  command=self._submit, pady=8, padx=20).pack(side="left", padx=4)
        tk.Button(btn_frame, text="🗑 Limpiar", font=("Arial", 9),
                  bg=BORDER, fg=TEXT, relief="flat", cursor="hand2",
                  command=self._clear).pack(side="left", padx=4)

        self.lbl_status = tk.Label(form_frame, text="", font=("Arial", 9),
                                   bg=BG_CARD, fg=SUCCESS)
        self.lbl_status.grid(row=len(fields)+7, columnspan=2)

        # ─── Historial ────────────────────────────────────────────────────
        hist_frame = tk.Frame(main, bg=BG_CARD, padx=12, pady=12)
        hist_frame.pack(side="right", fill="both", expand=True)

        tk.Label(hist_frame, text="📋 HISTORIAL DE SALIDAS", font=("Arial", 10, "bold"),
                 bg=BG_CARD, fg=WARNING).pack(anchor="w", pady=(0, 8))

        cols = ("Fecha", "Fabricante", "Referencia", "Cant.", "Costo", "Máquina", "Técnico", "Usuario")
        self.tree = ttk.Treeview(hist_frame, columns=cols, show="headings", height=20)

        style = ttk.Style()
        style.configure("Treeview", background=BG_CARD, foreground=TEXT,
                         fieldbackground=BG_CARD, rowheight=26)
        style.configure("Treeview.Heading", background="#21262D", foreground=TEXT_DIM,
                         font=("Arial", 9, "bold"))
        style.map("Treeview", background=[("selected", "#1F6FEB")])

        widths = [130, 90, 100, 55, 90, 100, 90, 80]
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w)

        sb = ttk.Scrollbar(hist_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._load_historial()
        self._current_valor = 0

    def _buscar(self):
        ref = self.entry_search.get().strip()
        if not ref:
            return
        conn = self.db.get_conn()
        row = conn.execute(
            "SELECT * FROM inventario WHERE LOWER(referencia) LIKE LOWER(?) AND activo=1 LIMIT 1",
            (f"%{ref}%",)
        ).fetchone()
        if row:
            self.entries["fab"].delete(0, "end")
            self.entries["fab"].insert(0, row["fabricante"])
            self.entries["ref"].delete(0, "end")
            self.entries["ref"].insert(0, row["referencia"])
            self._current_valor = row["valor_unitario"]
            self.lbl_info.config(
                text=f"✅ Encontrado: {row['fabricante']} | Stock: {row['cantidad']} uds | "
                     f"Valor: ${row['valor_unitario']:,.0f}",
                fg=SUCCESS
            )
        else:
            self.lbl_info.config(text="❌ Referencia no encontrada", fg=DANGER)
            self._current_valor = 0

    def _calc_costo(self, event=None):
        try:
            cant = float(self.entries["cant"].get())
            costo = cant * self._current_valor
            self.lbl_costo.config(text=f"Costo estimado: ${costo:,.0f}")
        except ValueError:
            self.lbl_costo.config(text="Costo estimado: $0")

    def _load_historial(self):
        self.tree.delete(*self.tree.get_children())
        rows = self.db.get_salidas()
        for r in rows:
            self.tree.insert("", "end", values=(
                r["fecha"][:16], r["fabricante"], r["referencia"],
                r["cantidad"], f"${r['costo_consumido']:,.0f}",
                r["maquina"], r["tecnico"], r["usuario"]
            ))

    def _submit(self):
        data = {
            "fabricante": self.entries["fab"].get().strip(),
            "referencia": self.entries["ref"].get().strip(),
            "cantidad": self.entries["cant"].get().strip(),
            "maquina": self.entries["maq"].get().strip(),
            "area": self.entries["area"].get().strip(),
            "tecnico": self.entries["tecnico"].get().strip(),
            "motivo": self.entries["motivo"].get().strip(),
            "observaciones": self.txt_obs.get("1.0", "end").strip(),
            "fecha": self.entry_fecha.get().strip(),
        }

        if not data["fabricante"] or not data["referencia"] or not data["cantidad"]:
            self.lbl_status.config(text="⚠ Fabricante, Referencia y Cantidad son obligatorios", fg=DANGER)
            return
        try:
            data["cantidad"] = float(data["cantidad"])
            if data["cantidad"] <= 0:
                raise ValueError
        except ValueError:
            self.lbl_status.config(text="⚠ Cantidad debe ser un número positivo", fg=DANGER)
            return

        try:
            self.db.registrar_salida(data, self.user["username"])
            self.lbl_status.config(text=f"✅ Salida registrada: {data['referencia']}", fg=SUCCESS)
            self._clear()
            self._load_historial()
        except ValueError as e:
            self.lbl_status.config(text=f"❌ {e}", fg=DANGER)

    def _clear(self):
        for e in self.entries.values():
            e.delete(0, "end")
        self.txt_obs.delete("1.0", "end")
        self.entry_search.delete(0, "end")
        self.lbl_info.config(text="")
        self.lbl_costo.config(text="Costo estimado: $0")
        self._current_valor = 0
        self.entry_fecha.delete(0, "end")
        self.entry_fecha.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
