@echo off
REM ═══════════════════════════════════════════════════════════════
REM  BUILD.BAT - Compilar Sistema de Inventario Industrial a .EXE
REM  Ejecutar este archivo en Windows con Python instalado
REM ═══════════════════════════════════════════════════════════════

echo Instalando dependencias...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Compilando ejecutable...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name "InventarioIndustrial" ^
  --icon=assets\icon.ico ^
  --add-data "assets;assets" ^
  --hidden-import openpyxl ^
  --hidden-import reportlab ^
  --hidden-import PIL ^
  --hidden-import sqlite3 ^
  main.py

echo.
echo ✅ Ejecutable generado en: dist\InventarioIndustrial.exe
echo Copie la carpeta 'dist' completa al equipo destino.
pause
