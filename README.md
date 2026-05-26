# ⚙ SISTEMA DE INVENTARIO INDUSTRIAL
### Software de Gestión de Repuestos y Materiales Industriales

---

## 📋 DESCRIPCIÓN

Sistema completo de inventario industrial desarrollado en Python con interfaz gráfica moderna (tema oscuro profesional). Importa automáticamente el inventario del archivo Excel `Macro_prueba.xlsm` y gestiona entradas, salidas, alertas y reportes.

---

## 🗂 ESTRUCTURA DEL PROYECTO

```
inventario_industrial/
│
├── main.py                    # Punto de entrada principal
├── requirements.txt           # Dependencias Python
├── build_exe.bat              # Script para generar EXE en Windows
│
├── core/
│   └── database.py            # Gestión SQLite: inventario, entradas, salidas, alertas
│
├── ui/
│   ├── login_window.py        # Pantalla de inicio de sesión
│   └── main_window.py         # Ventana principal + sidebar de navegación
│
├── modules/
│   ├── dashboard.py           # Panel principal con estadísticas y tarjetas
│   ├── entradas.py            # Formulario de entradas + historial
│   ├── salidas.py             # Formulario de salidas + historial
│   ├── inventario.py          # Vista completa del inventario con filtros
│   ├── alertas.py             # Alertas de stock bajo/crítico/agotado
│   └── reportes.py            # Reportes PDF y Excel con filtros de fecha
│
├── data/
│   └── inventario.db          # Base de datos SQLite (auto-generada)
│
├── backups/                   # Copias de seguridad automáticas (cada 30 min)
├── imagenes/                  # Imágenes de productos
├── reportes/                  # PDFs y Excel generados
└── excel/                     # Exportaciones Excel
```

---

## 🚀 INSTALACIÓN Y USO

### Opción 1: Ejecutar en Python (desarrollo)
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
python main.py
```

### Opción 2: Generar ejecutable EXE (producción Windows)
```bash
# En Windows, ejecutar el script:
build_exe.bat

# El ejecutable estará en:
dist/InventarioIndustrial.exe
```

---

## 🔐 CREDENCIALES POR DEFECTO
| Campo     | Valor     |
|-----------|-----------|
| Usuario   | `admin`   |
| Contraseña| `admin123`|

---

## 📦 MÓDULOS DEL SISTEMA

### 📊 Dashboard
- Tarjetas de estadísticas en tiempo real
- Lista de productos críticos y agotados
- Consumo por máquina/área
- Actualización manual con botón Refresh

### 📥 Entradas
- Formulario completo para agregar stock
- Si el producto ya existe → **suma al stock actual**
- Cálculo automático de valor total
- Carga de imágenes del producto
- Historial completo de entradas

### 📤 Salidas
- Búsqueda rápida de referencia
- Validación de stock antes de restar
- Cálculo automático de costo consumido
- **Impide salidas si no hay stock suficiente**
- Historial completo de salidas

### 📦 Inventario General
- Tabla completa con búsqueda en tiempo real
- Filtro por estado (Normal / Bajo / Crítico / Agotado)
- Panel lateral con detalle del producto e imagen
- Doble clic para editar producto
- Exportación directa a Excel
- Código de colores por estado de stock

### 🔔 Alertas
- Tarjetas resumen: agotados, críticos, bajos
- Historial completo de alertas
- Marcar como leídas
- Lista de productos que requieren reposición

### 📈 Reportes
- Filtro por rango de fechas
- Resumen ejecutivo con top 10 más consumidos
- Consumo por máquina/área
- Historial de entradas y salidas
- Lista de críticos
- **Exportar a PDF** (formato profesional)
- **Exportar a Excel** (múltiples hojas)

---

## 🏷 ESTADOS DE STOCK

| Estado   | Color     | Condición                          |
|----------|-----------|------------------------------------|
| Normal   | Blanco    | cantidad > stock_mínimo            |
| Bajo     | Naranja   | cantidad ≤ stock_mínimo            |
| Crítico  | Amarillo  | cantidad ≤ stock_crítico           |
| Agotado  | Rojo      | cantidad = 0                       |

---

## 🔧 TECNOLOGÍAS USADAS

| Tecnología  | Uso                              |
|-------------|----------------------------------|
| Python 3.x  | Lenguaje principal               |
| Tkinter     | Interfaz gráfica (incluido)      |
| SQLite      | Base de datos local (incluido)   |
| openpyxl    | Lectura/escritura Excel          |
| reportlab   | Generación de PDF                |
| Pillow      | Manejo de imágenes (opcional)    |
| PyInstaller | Compilación a .EXE               |

---

## 💾 BACKUP AUTOMÁTICO
El sistema realiza **copias de seguridad automáticas** de la base de datos SQLite cada **30 minutos**, almacenadas en la carpeta `backups/` con timestamp en el nombre.

---

## 🔄 MIGRACIÓN DEL EXCEL
Al iniciar por primera vez, el sistema detecta el archivo `Macro_prueba.xlsm` y **migra automáticamente** todos los productos de la hoja `INVENTARIO` a la base de datos SQLite.

---

## 📈 MEJORAS FUTURAS PROPUESTAS

1. **Módulo de Usuarios**: gestión de múltiples usuarios con roles (admin, operador, visualizador)
2. **Notificaciones por Email**: alertas automáticas por correo cuando el stock es crítico
3. **Código de Barras / QR**: escaneo para entrada/salida rápida
4. **Integración ERPs**: conectar con SAP, Odoo, etc.
5. **App Móvil**: versión responsive o app complementaria
6. **Dashboard con Gráficos**: matplotlib/plotly integrado para visualizaciones
7. **API REST**: exponer datos para integraciones externas
8. **Multi-bodega**: gestionar múltiples almacenes o ubicaciones
9. **Órdenes de Compra**: generación automática cuando el stock es bajo
10. **Modo Red**: servidor SQLite compartido en red local (SQLite → PostgreSQL)

---

## 📞 SOPORTE
Ante cualquier error, revise:
- Python 3.8+ instalado
- Dependencias instaladas (`pip install -r requirements.txt`)
- Permisos de escritura en la carpeta de instalación
