# FILENAME: TESTING.md
# COMPLETE PATH: audit/TESTING.md
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.0
# Date: 2026-02-08 00:10:31

## Langages détectés
- Python
- Bash

## Frameworks de test
- Aucun framework de test automatisé détecté.

## Tests existants
- Scripts manuels: test_sentence_transfomers.py, test_db_huffing.py.

## Commandes exactes
```
python 2_Sources/2.1_Python/test_sentence_transfomers.py
python 2_Sources/2.1_Python/test_db_huffing.py
```

## Tests unitaires
- Aucun test unitaire automatisé.

## Tests d’intégration
- Aucun test d’intégration automatisé.

## Tests manuels
- Vérifier API via curl (voir USAGE.md).

## Résultats observés
- Aucun test exécuté dans cet audit.

## Couverture estimée
- UNKNOWN (non mesurée).

## Recommandations
- Ajouter pytest + tests API.
- Ajouter tests de services (vector_store, generation).
