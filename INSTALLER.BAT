@echo off
chcp 65001 >nul
title Installation - Outil Segmentation FAE
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║     🚀  INSTALLATION - OUTIL SEGMENTATION FAE 2026  🚀       ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo ⏳ Installation en cours... Veuillez patienter
echo.

REM Vérifier si Python est déjà installé
if exist "python-3.14.3\python.exe" (
    echo ✅ Python portable détecté
) else (
    echo ❌ Erreur : Python portable introuvable
    echo    Vérifiez que le dossier python-3.14.3 est présent
    pause
    exit /b 1
)

REM Mise à jour de pip
echo.
echo 📦 Mise à jour de pip...
python-3.14.3\python.exe -m pip install --upgrade pip --quiet

REM Installation des dépendances
echo.
echo 📦 Installation des modules Python (cela peut prendre 2-3 minutes)...
python-3.14.3\python.exe -m pip install -r app\requirements.txt --quiet

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors de l'installation des dépendances
    echo    Vérifiez votre connexion internet
    pause
    exit /b 1
)

echo.
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║              ✅  INSTALLATION TERMINÉE AVEC SUCCÈS  ✅        ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 🎯 Pour lancer l'outil, double-cliquez sur : LANCER_OUTIL.bat
echo.
pause