# Correction Audit – NoXoZ_job

PDF companion: `correction_audit.pdf`.

## Objectif
Corriger les incohérences, réduire les duplications, fiabiliser les chemins de données, et clarifier les scripts/artefacts.

## Corrections recommandées (par thème)

### 1) Unification des chemins de données (SQLite/Chroma)
- **Aligner tous les chemins SQLite** :
  - `services/vector_store.py` utilise `3_Data/Metadata/metadata.db`.
  - `8_Scripts/8.1_Init/init_sqlite.sh` crée `.../noxoz_metadata.db`.
  - `api/monitor.py` pointe `.../sqlite/noxoz_metadata.db`.
  - **Correction** : choisir un seul nom et un seul emplacement (ex. `3_Data/Metadata/noxoz_metadata.db` via symlink), puis mettre à jour `vector_store.py`, `status.py`, `monitor.py`, `init_sqlite.sh`.
- **Uniformiser la persistance Chroma** :
  - `vector_store.py` utilise `3_Data/3.1_Vectors/chroma_link`.
  - `monitor.py` et `fastapi_full_monitor.py` pointent `/mnt/data1_100g/.../vectors`.
  - **Correction** : standardiser sur `3_Data/3.1_Vectors/chroma_link` (symlink) pour éviter la divergence.

### 2) Nettoyage des duplications / fichiers obsolètes
- **Supprimer ou archiver** :
  - `2_Sources/2.1_Python/api/endpoints/status.ORI.py` (duplicat).
  - `2_Sources/2.1_Python/api/endpoints/fastapi_full_monitor.py` (app FastAPI autonome redondante).
  - `temp.py` (racine) et `2_Sources/2.1_Python/temp.py` si non utilisés.
- **Clarifier `check_all_web_python.sh`** : le renommer en `.md` ou `.txt` si c’est une note.

### 3) Conflit de routes FastAPI
- Deux routes `/api/monitor/health` déclarées (monitor + status_web).
- **Correction** :
  - Renommer l’un des endpoints (ex. `/api/monitor/web_health`),
  - ou fusionner dans un seul endpoint unique.

### 4) Scripts vides / historiques
- `2_Sources/2.2_Bash/create_structure.sh` et `8_Scripts/8.1_Init/create-repo.sh` sont vides.
- **Correction** : soit les supprimer, soit ajouter une README indiquant qu’ils sont placeholders.

### 5) Artefacts dans le repo
- PID et logs présents dans l’arborescence (`fastapi.pid`, `10_Runs/*.pid`, `4_Logs/*`).
- **Correction** :
  - Ajouter un `.gitignore` pour `4_Logs/`, `10_Runs/`, `5_Outputs/`, `6_Results/`.
  - Nettoyer les artefacts existants du repo.

### 6) Dossier utils contenant des fichiers PS
- `8_Scripts/8.2_Utils/argparse`, `datetime`, `json`, `requests`, `sys` sont des fichiers PostScript exportés par ImageMagick.
- **Correction** :
  - déplacer ces fichiers dans un dossier `assets/` ou `docs/` s’ils sont utiles,
  - ou les supprimer si ce sont des exports temporaires.

### 7) Documentation
- Le README inclut une arborescence qui ne correspond plus exactement au repo actuel.
- **Correction** :
  - mettre à jour la section arborescence,
  - mentionner explicitement les chemins réels utilisés (symlinks, volumes).

## Corrections techniques détaillées (propositions)

1. **Harmoniser les chemins SQLite**
   - Choix recommandé : `3_Data/Metadata/noxoz_metadata.db` (symlink vers `/mnt/.../sqlite`).
   - Modifier :
     - `services/vector_store.py` → `METADATA_DB` vers `noxoz_metadata.db`.
     - `api/monitor.py` → `SQLITE_DB` vers le même chemin.
     - `api/endpoints/status.py` → utilise `METADATA_DB` unifié.

2. **Conflit `monitor/health`**
   - Renommer `status_web.py` endpoint health en `/api/monitor/web_health`.
   - Ou supprimer le health de `status_web.py` et garder celui de `monitor.py`.

3. **Réduction des scripts d’init**
   - Converger vers `config_paths.sh` + `init_sqlite.sh` comme sources de vérité.
   - Marquer `init_fastapi.sh` comme historique si non utilisé.

4. **Nettoyage Git**
   - Ajouter `.gitignore` pour logs/outputs/pids.
   - Supprimer les artefacts présents.

---

*Ce fichier liste des corrections à appliquer sur la base de l’audit.*
