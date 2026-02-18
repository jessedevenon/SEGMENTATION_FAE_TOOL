@echo off
chcp 65001 >nul
title Outil Segmentation FAE - Cabinet Expert-Comptable
color 0B

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║         📊  OUTIL SEGMENTATION FAE 2026 - LANCEMENT  📊      ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo ⏳ Démarrage de l'application...
echo.
echo 🌐 L'outil va s'ouvrir dans votre navigateur dans quelques secondes
echo.
echo ⚠️  NE FERMEZ PAS CETTE FENÊTRE tant que vous utilisez l'outil
echo.
echo ─────────────────────────────────────────────────────────────────
echo.

REM Lancer Streamlit
python-3.14.3\python.exe -m streamlit run app\main.py

echo.
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║                     OUTIL FERMÉ                               ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
pause