"""
SISTEMA DE INVENTARIO INDUSTRIAL
Aplicación principal - Entry point
"""
import sys
import os

# Asegurar que las carpetas necesarias existen
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for folder in ["reportes", "imagenes", "backups", "excel", "data"]:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

import tkinter as tk
from tkinter import messagebox
from ui.login_window import LoginWindow
from core.database import Database


def main():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal temporalmente
    
    # Inicializar base de datos
    db = Database(os.path.join(BASE_DIR, "data", "inventario.db"))
    db.initialize()
    db.migrate_excel(os.path.join(BASE_DIR, "..", "Macro_prueba.xlsm"))
    
    # Mostrar login
    login = LoginWindow(root, db)
    root.wait_window(login)
    
    if login.authenticated:
        root.deiconify()
        from ui.main_window import MainWindow
        app = MainWindow(root, db, login.current_user)
        root.mainloop()
    else:
        root.destroy()


if __name__ == "__main__":
    main()
