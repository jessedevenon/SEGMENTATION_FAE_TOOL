"""
LAUNCHER - Outil Segmentation Clientèle
Lance automatiquement l'application Streamlit
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Chemin vers main.py
    app_path = Path(__file__).parent / "app" / "main.py"
    
    if not app_path.exists():
        print("❌ Erreur : Fichier main.py introuvable")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    print("🚀 Lancement de l'outil de segmentation...")
    print("📊 L'application va s'ouvrir dans votre navigateur...")
    print("")
    print("💡 Pour arrêter l'application, fermez cette fenêtre.")
    print("")
    
    try:
        # Lancer Streamlit
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.headless=true"
        ])
    except KeyboardInterrupt:
        print("\n✅ Application arrêtée")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()