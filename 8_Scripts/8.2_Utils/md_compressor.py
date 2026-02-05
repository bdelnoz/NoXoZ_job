#!/usr/bin/env python3
# /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/8_Scripts/8.2_Utils/md_compressor.py
# Author: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.1.0 - Date: 2025-05-22
#
# Target usage: Compresses Markdown files to a specific character range using Ollama models.
#
# Changelog:
# v1.0.0 - 2025-05-22 - Initial version with V115 compliance.
# v1.1.0 - 2025-05-22 - Added --charmin, --charmax and detailed help examples. Improved arg parsing.

import argparse
import sys
import os
import json
import requests
import datetime

def log_message(message, script_name, version):
    """14.11 LOGS DÉTAILLÉS"""
    log_dir = "./logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/log.{script_name}.{timestamp}.{version}.log"

    with open(log_file, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")

def show_progress(step, total, description):
    """14.5.8 AFFICHAGE ETAT AVANCEMENT"""
    print(f"[PROGRESS] {description} ({step}/{total})")

def display_help():
    """14.7 HELP & 14.7.3 VALEURS PAR DEFAUT"""
    help_text = """
### MD COMPRESSOR - HELP MENU
Author: Bruno DELNOZ
Version: v1.1.0

USAGE:
  python3 md_compressor.py [ARGUMENTS]

ARGUMENTS OBLIGATOIRES:
  --exec, -exe        : Exécuter le script principal
  --file, -f [PATH]   : Chemin du fichier Markdown à compresser

ARGUMENTS DE CONFIGURATION:
  --charmin [INT]     : Limite MIN de caractères (Défaut: 7900)
  --charmax [INT]     : Limite MAX de caractères (Défaut: 8000)
  --model, -m [STR]   : Modèle Ollama à utiliser (Défaut: deepseek-r1:8b)

ARGUMENTS SYSTEME:
  --help, -h          : Afficher cette aide complète
  --prerequis, -pr    : Vérifier la connexion à Ollama
  --install, -i       : (Simulé) Installer les dépendances (requests)
  --simulate, -s      : Mode dry-run (aucune modification réelle)
  --changelog, -ch    : Afficher l'historique des modifications

EXEMPLES:
  1. Compression standard:
     python3 md_compressor.py --exec --file notes.md
  2. Plage personnalisée avec simulation:
     python3 md_compressor.py --exec --file notes.md --charmin 5000 --charmax 5100 --simulate
  3. Utiliser un modèle spécifique:
     python3 md_compressor.py --exec --file doc.md --model mistral:7b
    """
    print(help_text)

def main():
    script_name = "md_compressor"
    version = "v1.1.0"

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", "-h", action="store_true")
    parser.add_argument("--exec", "-exe", action="store_true")
    parser.add_argument("--prerequis", "-pr", action="store_true")
    parser.add_argument("--install", "-i", action="store_true")
    parser.add_argument("--simulate", "-s", action="store_true")
    parser.add_argument("--changelog", "-ch", action="store_true")
    parser.add_argument("--file", "-f", type=str)
    parser.add_argument("--model", "-m", type=str, default="deepseek-r1:8b")
    parser.add_argument("--charmin", type=int, default=7900)
    parser.add_argument("--charmax", type=int, default=8000)

    args = parser.parse_args()

    # 14.7.2 Help par défaut
    if args.help or len(sys.argv) == 1:
        display_help()
        sys.exit(0)

    # 14.20 CHANGELOG DANS LES SCRIPTS
    if args.changelog:
        print(f"--- CHANGELOG {script_name} ---")
        print("v1.0.0 - 2025-05-22 - Initial version.")
        print("v1.1.0 - 2025-05-22 - Added --charmin, --charmax, and improved help.")
        sys.exit(0)

    # 14.9 PRÉREQUIS
    if args.prerequis:
        show_progress(1, 1, "Checking Ollama Connection")
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=5)
            if r.status_code == 200:
                print("Status: Ollama is ONLINE")
            else:
                print("Status: Ollama returned an ERROR")
        except Exception as e:
            print(f"Status: Ollama is OFFLINE ({e})")
        sys.exit(0)

    # 14.8 EXECUTION
    if args.exec:
        if not args.file:
            print("Erreur: L'argument --file est obligatoire avec --exec.")
            sys.exit(1)

        actions = []

        show_progress(1, 4, f"Lecture de {args.file}")
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            actions.append(f"Fichier source lu ({len(content)} chars)")
        except Exception as e:
            print(f"Erreur lecture: {e}")
            sys.exit(1)

        # Construction du prompt dynamique avec les nouvelles limites
        prompt = f"""### MISSION:
        Compress the following Markdown content to stay within {args.charmin} and {args.charmax} characters.

        ### CONSTRAINTS:
        - Language: ENGLISH only.
        - Rules: Remove fluff, use abbreviations, keep numbering.
        - Output: ONE single Markdown code block.

        ### INPUT:
        {content}"""

        if args.simulate:
            show_progress(2, 4, "Simulation de l'appel API (Mode Dry-Run)")
            actions.append(f"Simulation API avec modèle {args.model}")
            print(f"[SIMULATE] CharMin: {args.charmin} | CharMax: {args.charmax}")
        else:
            show_progress(2, 4, f"Envoi vers Ollama ({args.model})")
            payload = {"model": args.model, "prompt": prompt, "stream": False}
            try:
                response = requests.post("http://localhost:11434/api/generate", json=payload)
                result = response.json().get("response", "")
                actions.append(f"Réponse reçue de {args.model}")

                show_progress(3, 4, "Sauvegarde du résultat")
                res_dir = "./results"
                if not os.path.exists(res_dir): os.makedirs(res_dir)

                output_path = f"{res_dir}/compressed.{args.charmin}_{args.charmax}.md"
                with open(output_path, "w", encoding='utf-8') as wf:
                    wf.write(result)
                actions.append(f"Fichier sauvegardé: {output_path} (Taille: {len(result)} chars)")
            except Exception as e:
                print(f"Erreur API: {e}")
                sys.exit(1)

        # 14.10 AFFICHAGE POST-EXÉCUTION
        show_progress(4, 4, "Terminé")
        print("\nACTIONS REALISEES:")
        for i, a in enumerate(actions, 1):
            print(f"{i}. {a}")
            log_message(a, script_name, version)

if __name__ == "__main__":
    main()
