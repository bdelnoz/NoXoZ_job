# FILENAME: correction_audit.md
# COMPLETE PATH: audit/correction_audit.md
# Auteur: Bruno DELNOZ
# Email: bruno.delnoz@protonmail.com
# Version: v1.0
# Date: 2026-02-08 00:10:31

| Problem | Impact | Files | Proposed fix | Effort | Risk |
| --- | --- | --- | --- | --- | --- |
| Collision /api/monitor/health défini deux fois | Ambiguïté route et comportement non déterministe | 2_Sources/2.1_Python/api/monitor.py; 2_Sources/2.1_Python/api/endpoints/status_web.py | Renommer un endpoint (ex: /api/monitor/web_health) et mettre à jour la page HTML | Low | Low |
| Chemins absolus hardcodés (/mnt/data1_100g, /mnt/data2_78g) | Déploiement non portable | 2_Sources/2.1_Python/api/monitor.py; 2_Sources/2.1_Python/services/vector_store.py; 8_Scripts/8.1_Init/* | Introduire variables d’environnement + fichier config paths | Med | Med |
| Fichier legacy status.ORI.py | Duplication et confusion | 2_Sources/2.1_Python/api/endpoints/status.ORI.py | Supprimer ou déplacer vers dossier legacy; garder status.py comme source unique | Low | Low |
| fastapi_full_monitor.py non branché | Code mort / confusion | 2_Sources/2.1_Python/api/endpoints/fastapi_full_monitor.py | Documenter usage séparé ou intégrer via router | Low | Low |
| Scripts shell sans usage explicite | Onboarding difficile | 8_Scripts/8.1_Init/*.sh | Ajouter --help et commentaires d’usage | Low | Low |
| Certificats TLS versionnés | Risque de fuite | certs/cert.pem; certs/key.pem | Remplacer par templates + générer via script | Med | High |
