"""
modules/entradas.py - Módulo de entradas de inventario
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime, shutil, os

BG_DARK  = "#0D1117"
BG_CARD  = "#161B22"
BG_INPUT = "#21262D"
ACCENT   = "#00D4FF"
TEXT     = "#E6EDF3"
TEXT_DIM = "#8B949E"
SUCCESS  = "#3FB950"
DANGER   = "#FF4C4C"
BORDER   = "#30363D"


def label(parent, text, row, col, **kw):
    tk.Label(parent, text=text, font=("Arial", 9), bg=BG_CARD,
             fg=TEXT_DIM, **kw).grid(row=row, column=col, sticky="w", padx=(0, 8), pady=3)


def entry(parent, row, col, width=28, **kw):
    e = tk.Entry(parent, font=("Arial", 10), bg=BG_INPUT, fg=TEXT,
                 insertbackground=TEXT, relief="flat", bd=6, width=width, **kw)
    e.grid(row=row, column=col, sticky="ew", pady=3, padx=(0, 12))
    return e


class EntradasModule:
    def __init__(self, parent, db, user):
        self.parent = parent
        self.db = db
        self.user = user
        self.imagen_path = None
        self._build()

    def _build(self):
        # Title row
        top = tk.Frame(self.parent, bg=BG_DARK)
        top.pack(fill="x", pady=(0, 12))
        tk.Label(top, text="Registrar entrada de material al inventario",
                 font=("Arial", 10), bg=BG_DARK, fg=TEXT_DIM).pack(side="left")

        main = tk.Frame(self.parent, bg=BG_DARK)
        main.pack(fill="both", expand=True)

        # ─── Formulario ─────────────────────────────────────────────────────
        form_frame = tk.Frame(main, bg=BG_CARD, padx=24, pady=20)
        form_frame.pack(side="left", fill="y", padx=(0, 12))

        tk.Label(form_frame, text="📥 NUEVA ENTRADA", font=("Arial", 11, "bold"),
                 bg=BG_CARD, fg=ACCENT).grid(row=0, columnspan=2, sticky="w", pady=(0, 12))

        fields = [
            ("Fabricante *", "fab"),
            ("Referencia *", "ref"),
            ("Descripción", "desc"),
            ("Cantidad *", "cant"),
            ("Valor Unitario", "valor"),
            ("Ubicación", "ubic"),
            ("Máquina / Área", "maq"),
            ("Stock Mínimo", "smin"),
            ("Stock Crítico", "scrit"),
        ]
        self.entries = {}
        for i, (lbl_text, key) in enumerate(fields, start=1):
            label(form_frame, lbl_text, i, 0)
            self.entries[key] = entry(form_frame, i, 1)

        # Fecha
        label(form_frame, "Fecha", len(fields)+1, 0)
        self.entry_fecha = entry(form_frame, len(fields)+1, 1)
        self.entry_fecha.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        # Observaciones
        label(form_frame, "Observaciones", len(fields)+2, 0)
        self.txt_obs = tk.Text(form_frame, font=("Arial", 10), bg=BG_INPUT, fg=TEXT,
                               insertbackground=TEXT, relief="flat", bd=6,
                               width=28, height=3)
        self.txt_obs.grid(row=len(fields)+2, column=1, sticky="ew", pady=3)

        # Imagen
        img_row = len(fields) + 3
        label(form_frame, "Imagen", img_row, 0)
        img_frame = tk.Frame(form_frame, bg=BG_CARD)
        img_frame.grid(row=img_row, column=1, sticky="ew", pady=3)

        self.lbl_img = tk.Label(img_frame, text="Sin imagen", font=("Arial", 9),
                                bg=BG_CARD, fg=TEXT_DIM)
        self.lbl_img.pack(side="left")
        tk.Button(img_frame, text="📎 Seleccionar", font=("Arial", 8),
                  bg=BORDER, fg=TEXT, relief="flat", cursor="hand2",
                  command=self._select_image).pack(side="right", padx=4)

        # Botones
        btn_row = img_row + 1
        btn_frame = tk.Frame(form_frame, bg=BG_CARD)
        btn_frame.grid(row=btn_row, columnspan=2, pady=16)

        tk.Button(btn_frame, text="✅  REGISTRAR ENTRADA", font=("Arial", 10, "bold"),
                  bg=SUCCESS, fg=BG_DARK, relief="flat", cursor="hand2",
                  command=self._submit, pady=8, padx=20).pack(side="left", padx=4)
        tk.Button(btn_frame, text="🗑 Limpiar", font=("Arial", 9),
                  bg=BORDER, fg=TEXT, relief="flat", cursor="hand2",
                  command=self._clear).pack(side="left", padx=4)

        self.lbl_status = tk.Label(form_frame, text="", font=("Arial", 9),
                                   bg=BG_CARD, fg=SUCCESS)
        self.lbl_status.grid(row=btn_row+1, columnspan=2)

        # ─── Historial ────────────────────────────────────────────────────
        hist_frame = tk.Frame(main, bg=BG_CARD, padx=12, pady=12)
        hist_frame.pack(side="right", fill="both", expand=True)

        tk.Label(hist_frame, text="📋 HISTORIAL DE ENTRADAS", font=("Arial", 10, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(0, 8))

        cols = ("Fecha", "Fabricante", "Referencia", "Cantidad", "Valor Unit.", "Total", "Usuario")
        self.tree = ttk.Treeview(hist_frame, columns=cols, show="headings", height=20)

        style = ttk.Style()
        style.configure("Treeview", background=BG_CARD, foreground=TEXT,
                         fieldbackground=BG_CARD, rowheight=26, borderwidth=0)
        style.configure("Treeview.Heading", background="#21262D", foreground=TEXT_DIM,
                         font=("Arial", 9, "bold"))
        style.map("Treeview", background=[("selected", "#1F6FEB")])

        widths = [130, 100, 110, 70, 90, 90, 90]
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w)

        sb = ttk.Scrollbar(hist_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._load_historial()

    def _load_historial(self):
        self.tree.delete(*self.tree.get_children())
        rows = self.db.get_entradas()
        for r in rows:
            self.tree.insert("", "end", values=(
                r["fecha"][:16], r["fabricante"], r["referencia"],
                r["cantidad"], f"${r['valor_unitario']:,.0f}",
                f"${r['valor_total']:,.0f}", r["usuario"]
            ))

    def _select_image(self):
        path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Todos", "*.*")]
        )
        if path:
            self.imagen_path = path
            self.lbl_img.config(text=os.path.basename(path))

    def _submit(self):
        data = {
            "fabricante": self.entries["fab"].get().strip(),
            "referencia": self.entries["ref"].get().strip(),
            "descripcion": self.entries["desc"].get().strip(),
            "cantidad": self.entries["cant"].get().strip(),
            "valor_unitario": self.entries["valor"].get().strip(),
            "ubicacion": self.entries["ubic"].get().strip(),
            "maquina": self.entries["maq"].get().strip(),
            "stock_minimo": self.entries["smin"].get().strip() or "2",
            "stock_critico": self.entries["scrit"].get().strip() or "1",
            "observaciones": self.txt_obs.get("1.0", "end").strip(),
            "fecha": self.entry_fecha.get().strip(),
        }

        # Validación
        if not data["fabricante"] or not data["referencia"] or not data["cantidad"]:
            self.lbl_status.config(text="⚠ Fabricante, Referencia y Cantidad son obligatorios", fg=DANGER)
            return
        try:
            data["cantidad"] = float(data["cantidad"])
            data["valor_unitario"] = float(data["valor_unitario"]) if data["valor_unitario"] else 0
            data["stock_minimo"] = float(data["stock_minimo"])
            data["stock_critico"] = float(data["stock_critico"])
        except ValueError:
            self.lbl_status.config(text="⚠ Cantidad y valores deben ser numéricos", fg=DANGER)
            return

        # Copiar imagen
        if self.imagen_path:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            img_dest_dir = os.path.join(base, "imagenes")
            os.makedirs(img_dest_dir, exist_ok=True)
            ext = os.path.splitext(self.imagen_path)[1]
            img_dest = os.path.join(img_dest_dir, f"{data['referencia'].replace(' ','_')}{ext}")
            shutil.copy2(self.imagen_path, img_dest)
            data["imagen_path"] = img_dest
        else:
            data["imagen_path"] = ""

        try:
            self.db.registrar_entrada(data, self.user["username"])
            self.lbl_status.config(text=f"✅ Entrada registrada: {data['referencia']}", fg=SUCCESS)
            self._clear()
            self._load_historial()
        except Exception as e:
            self.lbl_status.config(text=f"❌ Error: {e}", fg=DANGER)

    def _clear(self):
        for e in self.entries.values():
            e.delete(0, "end")
        self.txt_obs.delete("1.0", "end")
        self.imagen_path = None
        self.lbl_img.config(text="Sin imagen")
        self.entry_fecha.delete(0, "end")
        self.entry_fecha.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.entries["smin"].insert(0, "2")
        self.entries["scrit"].insert(0, "1")
