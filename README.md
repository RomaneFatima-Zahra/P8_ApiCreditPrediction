# 🧠 API de Prédiction de Solvabilité Client

Cette API permet d’évaluer la **solvabilité d’un client** pour statuer sur une demande de prêt.  
Elle s’appuie sur un modèle de **Machine Learning** (`model.pkl`) pour prédire si un client est **solvable** ou **défaillant**, à partir de ses données personnelles,  socio-économiques et de son profil.

## Contexte : 

Ce projet consiste à déployer en production un modèle de scoring de crédit via une API, avec monitoring et CI/CD automatisé.

Objectifs principaux :

Créer une API FastAPI fonctionnelle
Conteneuriser avec Docker
Mettre en place un pipeline CI/CD
Monitorer le modèle en production (Data Drift)
Optimiser les performances

---

## 🚀 Fonctionnalités

- ✅ **Endpoint principal `/predict`** pour obtenir une prédiction de solvabilité.  
- 🧩 **Validation stricte des données** via des modèles `Pydantic`.  
- 🧾 **Logs structurés en JSON** dans `logs/api_logger.log`.  
- 🧪 **Tests unitaires et d’intégration** (via `pytest`).  
- 🐳 **Image Docker** prête à être déployée.

---

## 🧱 Structure du projet

```
📦 ApiCreditPrediction
├── API_Fastapi.py
├── model.pkl
├── requirements.txt
├── test_unitaires.py
├── test_integration.py
├── Dockerfile
├── app_monitoring.py
├── data_drift_analysis.ipynb
├── api_performance_analysis.py
└── logs/
    └── api_logger.log
```

---

## ⚙️ Installation et exécution locale

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/RomaneFatima-Zahra/P8_ApiCreditPrediction
cd P8_ApiCreditPrediction
```

### 2️⃣ Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate   # Windows
```

### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4️⃣ Lancer l’API
```bash
uvicorn API_Fastapi:app --reload --port 7860
```

L’API sera disponible sur :  
👉 [http://localhost:7860](http://localhost:7860)

---

## 🧩 Endpoints disponibles

| Méthode | Route        | Description |
|----------|--------------|-------------|
| `GET`    | `/`          | Page d’accueil |
| `POST`   | `/predict`   | Prédiction de solvabilité |
| `GET`    | `/logs`      | Lecture des logs |
| `GET`    | `/favicon.ico` | Ignoré |

---

## 📤 Exemple d’appel à l’API

```bash
curl -X 'POST' \
  'http://127.0.0.1:7860/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
"NAME_CONTRACT_TYPE": "Revolving loans",
    "CODE_GENDER": "F",
    "FLAG_OWN_CAR": "N",
    "FLAG_OWN_REALTY": "Y",
    "CNT_CHILDREN": 0,
    "AMT_INCOME_TOTAL": 121500.0,
    "AMT_CREDIT": 180000.0,
    "AMT_ANNUITY": 9000.0,
    "AMT_GOODS_PRICE": 180000.0,
    "NAME_TYPE_SUITE": "Unaccompanied",
    "NAME_INCOME_TYPE": "Working",
    "NAME_EDUCATION_TYPE": "Incomplete higher",
    "NAME_FAMILY_STATUS": "Separated",
    "NAME_HOUSING_TYPE": "House / apartment",
    "REGION_POPULATION_RELATIVE": 0.022625,
    "DAYS_BIRTH": -10335,
    "DAYS_EMPLOYED": -484,
    "DAYS_REGISTRATION": -2322.0,
    "DAYS_ID_PUBLISH": -2468,
    "FLAG_EMP_PHONE": 1,
    "FLAG_WORK_PHONE": 1,
    "FLAG_PHONE": 1,
    "FLAG_EMAIL": 0,
    "OCCUPATION_TYPE": "Laborers",
    "CNT_FAM_MEMBERS": 1.0,
    "REGION_RATING_CLIENT": 2,
    "REGION_RATING_CLIENT_W_CITY": 2,
    "WEEKDAY_APPR_PROCESS_START": "WEDNESDAY",
    "HOUR_APPR_PROCESS_START": 12,
    "REG_REGION_NOT_LIVE_REGION": 0,
    "REG_REGION_NOT_WORK_REGION": 0,
    "LIVE_REGION_NOT_WORK_REGION": 0,
    "REG_CITY_NOT_LIVE_CITY": 0,
    "REG_CITY_NOT_WORK_CITY": 0,
    "LIVE_CITY_NOT_WORK_CITY": 0,
    "ORGANIZATION_TYPE": "Industry: type 3",
    "FLOORSMAX_AVG": 0.3333,
    "LIVINGAREA_AVG": 0.2647,
    "YEARS_BEGINEXPLUATATION_MODE": 0.994,
    "OBS_30_CNT_SOCIAL_CIRCLE": 0.0,
    "DEF_30_CNT_SOCIAL_CIRCLE": 0.0,
    "DAYS_LAST_PHONE_CHANGE": -542.0,
    "PREVIOUS_LOANS_COUNT": 4.0,
    "CREDIT_INCOME_PERCENT": 1.4814814814814814,
    "ANNUITY_INCOME_PERCENT": 0.074074074074074,
    "CREDIT_TERM": 0.05,
    "DAYS_EMPLOYED_PERCENT": 0.0468311562651185
}'

```
Exemple de réponse :
```json

{
  "prediction": "Défaillant",
  "probabilité_defaut": 0.5101
}

```

---

## 🧪 Tests  

Les tests unitaires et d’intégration sont gérés avec **pytest** et **pytest-cov** afin de garantir la fiabilité du modèle et de mesurer la couverture du code.  

### ▶️ Lancer la suite de tests (depuis la racine du projet)  
```bash
pytest -v
```

### 📊 Générer le rapport de couverture  
```bash
pytest --cov=. --cov-report=term-missing
```

### 🌐 Générer un rapport HTML détaillé  
```bash
pytest --cov=. --cov-report=html
```
Le rapport sera disponible dans le dossier `htmlcov/` :  
`htmlcov/index.html` (ouvrable avec votre navigateur).  

---

### 🧱 Structure des tests  

Les tests sont répartis en deux fichiers :  
- **`test_unitaires.py`** → vérifie les modèles Pydantic et les endpoints unitaires.  
- **`test_integration.py`** → teste le comportement global de l’API et les scénarios complets de prédiction.  

---

### ✅ Tests implémentés  

| Catégorie | Test | Description |
|------------|------|-------------|
| **Unitaires (Pydantic & endpoints)** | `test_client_data_valid` | Vérifie la création d’un objet `ClientData` valide. |
|  | `test_client_data_invalid_values` | Vérifie la validation des contraintes et des erreurs. |
|  | `test_enum_values` | Vérifie les valeurs possibles des énumérations (`CODE_GENDER`, `NAME_CONTRACT_TYPE`). |
|  | `test_home_endpoint` | Vérifie la route racine `/`. |
|  | `test_predict_endpoint_success` | Vérifie l’endpoint `/predict` avec un client valide (mock du modèle). |
|  | `test_predict_endpoint_defaillant` | Vérifie le comportement pour un client défaillant. |
|  | `test_predict_endpoint_invalid_data` | Vérifie la gestion d’entrées invalides (422). |
|  | `test_predict_endpoint_model_not_loaded` | Vérifie le message d’erreur si le modèle n’est pas chargé (500). |
| **Intégration (workflow complet)** | `test_complete_workflow` | Vérifie le parcours complet `/ → predict`. |
|  | `test_multiple_predictions` | Vérifie plusieurs prédictions consécutives avec des clients différents. |
|  | `test_error_handling` | Vérifie la robustesse face à des erreurs de validation. |
|  | `test_enum_validation` | Vérifie les erreurs sur valeurs d’énumération invalides. |
|  | `test_response_format` | Vérifie la structure et les types de données de la réponse JSON. |

---

## 🧰 Dockerisation

La dockerisation permet d’encapsuler l’API FastAPI et son modèle de Machine Learning dans un conteneur léger et portable.
Cela garantit une exécution identique sur tous les environnements (local, cloud, CI/CD) et simplifie le déploiement.

### 🎯 Objectif

Faciliter le déploiement de l’API sans dépendances locales.

Garantir un environnement reproductible entre les machines de développement, test et production.

Simplifier le scaling horizontal (plusieurs instances conteneurisées derrière un load balancer).

```bash

docker build -t api_default_prediction:latest .
```
📦 Crée une image à partir du Dockerfile à la racine du projet.

```bash
docker run -d -p 7860:7860 --name test-api api_default_prediction:latest
```
🚀 Exécute le conteneur en arrière-plan (-d) et mappe le port 7860 du conteneur sur le port 7860 de la machine hôte.
L’API devient accessible à l’adresse : http://localhost:7860

### Dockerfile 

FROM python:3.12.2-slim → image Python optimisée, légère, adaptée à la production.

WORKDIR /app → définit le dossier de travail du conteneur.

COPY . /app → copie le code source, y compris model.pkl, dans le conteneur.

RUN apt-get ... → installe les outils nécessaires pour compiler d’éventuelles dépendances (scikit-learn, numpy, etc.).

RUN pip install ... → installe les dépendances Python du projet listées dans requirements.txt.

EXPOSE 7860 → indique le port sur lequel l’API sera disponible à l’extérieur du conteneur.

CMD [...] → commande exécutée au démarrage : lance le serveur Uvicorn pour exécuter l’API FastAPI.
---

## 🪵 Logs et monitoring

La journalisation (logging) permet de suivre l’activité de l’API, diagnostiquer les erreurs, et surveiller les performances en production.
Les logs sont structurés et enregistrés automatiquement dans le dossier :
```
logs/api_logger.log
```
### 🎯 Objectif

Assurer une traçabilité complète des requêtes et réponses.

Identifier rapidement les erreurs ou anomalies.

Faciliter le debugging, l’analyse post-déploiement et la supervision (monitoring).

### 🧩 Contenu des logs

Chaque entrée du fichier api_logger.log contient les informations suivantes :

🕒 **Timestamp**	: Date et heure de l’événement (format ISO 8601).
⚙️ **Niveau** : 	Niveau de gravité (INFO, WARNING, ERROR, CRITICAL).
🧩 **Module/Fonction**	: Emplacement du log dans le code (ex : predict, startup_event).
🧠 **Message** : 	Détail du message (ex : “Requête reçue pour un client solvable”).

--

## ⚙️ Pipeline CI/CD (GitHub Actions)

### 🎯 Objectif  
Automatiser les **tests**, la **construction Docker** et la **validation du code** à chaque modification du dépôt GitHub.  
Ce pipeline assure une intégration continue fiable et reproductible, garantissant la stabilité avant tout déploiement.

---

### 🧩 Déclenchement du pipeline  
Le workflow GitHub Actions s’exécute automatiquement :  
- à chaque **push** sur la branche `main`,  
- et à chaque **pull request** vers `main`.

---

### 🧱 Structure du pipeline  

Le pipeline est composé de **deux jobs principaux**, exécutés dans cet ordre :  

| Étape | Nom du job | Objectif principal |
|--------|-------------|--------------------|
| 🧪 **Job 1** | `test` | Exécuter les tests unitaires et d’intégration |
| 🐳 **Job 2** | `build` | Construire et valider l’image Docker de l’API |


> 🔄 En cas d’échec sur les tests, la phase de build est automatiquement interrompue (`needs: test`).  

---

### 🧪 Job 1 — Tests automatisés  

**Nom complet :** `Run Tests unitaires et intégration`  
**Environnement :** `ubuntu-latest`  
**Durée moyenne :** ~2 minutes  

#### Étapes clés :  
1. **Checkout du code** → récupération du dépôt (`actions/checkout@v4`)  
2. **Installation de Python 3.12** → via `actions/setup-python@v4`  
3. **Installation des dépendances** → depuis `requirements.txt`  
4. **Exécution des tests** :
   ```bash
   python -m pytest test_unit.py -v
   python -m pytest test_integration.py -v
   ```
5. **Résultat attendu :**
   - ✅ Tous les tests passent avant d’autoriser le build  
   - ❌ En cas d’échec → le pipeline s’arrête immédiatement  

---

### 🐳 Job 2 — Build de l’image Docker  

**Nom complet :** `Build de Docker Image`  
**Condition d’exécution :** uniquement si le job `test` est réussi (`needs: test`)  
**Durée moyenne :** ~3 à 4 minutes  

#### Étapes clés :  
1. **Re-clonage du dépôt**  
2. **Configuration de l’environnement Docker Buildx** (`docker/setup-buildx-action@v3`)  
3. **Construction de l’image** :  
   ```bash
   docker build -t api_default_prediction:latest .
   ```
4. **Test de l’image construite** :  
   Lancement temporaire du conteneur et test du endpoint `/` :  
   ```bash
   docker run -d -p 7860:7860 --name test-api api_default_prediction:latest
   sleep 10
   curl -f http://localhost:7860/ || exit 1
   docker stop test-api
   ```
5. **Sauvegarde de l’image Docker** :  
   ```bash
   docker save api_default_prediction:latest -o image.tar
   ```
6. **Upload de l’artefact Docker** (fichier `image.tar`) via :  
   ```yaml
   uses: actions/upload-artifact@v4
   ```
   → Retenu 1 jour pour vérification manuelle.  

---

### 📊 Résumé des points de contrôle  

| Élément | Vérification | Statut attendu |
|----------|--------------|----------------|
| ✅ Tests unitaires | 100% des tests passent | 🟢 OK |
| 🧱 Build Docker | Image construite et testée | 🟢 OK |
| 📦 Artefact Docker | Uploadé avec succès | 🟢 OK |
| 🔔 Notifications | En cas d’échec | 🟠 Automatique via GitHub Actions |

---

### 🏆 Bonnes pratiques mises en œuvre  

- ✅ **Séparation claire des responsabilités** : un job pour les tests, un autre pour le build  
- ✅ **Dépendance explicite** entre jobs (`needs: test`)  
- ✅ **Actions officielles** :  
  - `actions/checkout@v4`  
  - `actions/setup-python@v4`  
  - `docker/setup-buildx-action@v3`  
  - `actions/upload-artifact@v4`  
- ✅ **Validation Docker automatisée** (vérification de disponibilité du service via `curl`)  
- ✅ **Reproductibilité** : chaque run CI/CD est isolé et cohérent  

---

### 🧭 Résumé global du workflow  

| Étape | Description | Durée estimée |
|--------|--------------|---------------|
| 🧪 Tests | Validation du code et du modèle | ~2 min |
| 🐳 Build Docker | Construction + test du conteneur | ~3 min |
| 📦 Upload artefact | Sauvegarde de l’image Docker | ~1 min |

> 🔄 Total : environ **6 minutes** du push au build complet.

--

# 📊 Monitoring et Analyse Avancée

Le projet comprend **des modules complémentaires** pour superviser les performances, la qualité des données et la fiabilité du modèle.

---

## 🖥️ 1. `app_monitoring.py` – Tableau de bord Streamlit

Une interface **Streamlit** interactive pour :  
- Visualiser les prédictions et métriques de performance  
- Suivre les taux d’erreurs, la latence, les pics de charge  
- Générer des rapports visuels

```bash
streamlit run app_monitoring.py
```

Accessible sur : [http://localhost:8501](http://localhost:8501)

---

## 📈 2. `data_drift_analysis.ipynb` – Analyse de dérive des données

Basée sur **Evidently AI**, elle compare les distributions entre données historiques et récentes pour détecter la **data drift**.

```bash
python data_drift_analysis.py
```

Sorties :  
- Rapport : `drift_report_temp.html`  
- Stats globales (latence, erreurs, dérive)

---
## ⚡ 3. `api_performance_analysis.py` – Profilage et benchmark du modèle

Permet de mesurer les performances du modèle (`predict`, `predict_proba`) et d’identifier les goulots d’étranglement.

```bash
python api_performance_analysis.py
```

Résultats :  
- `performance_results/cprofile_predict.txt`  
- `performance_results/bottlenecks.json`  
- `performance_results/benchmark.log`

### Méthodologie appliquée  

L’analyse de performance a consisté à évaluer différentes stratégies de gestion du modèle de Machine Learning afin d’**optimiser la vitesse de prédiction** et la **réactivité globale** de l’API.  

#### Étapes de la démarche  
1. **Benchmark de référence (version naïve)** — mesure des performances initiales.  
2. **Profilage `cProfile`** — identification des fonctions les plus coûteuses dans le pipeline scikit-learn.  
3. **Optimisation ciblée** — mise en place de correctifs visant à réduire la latence.  
4. **Mesure d’impact** — comparaison quantitative avant / après optimisation.  

#### ⚡ Optimisation principale : préchargement du modèle  
- **Problème identifié :** le modèle (~2,1 MB) était rechargé depuis le disque à **chaque requête**, générant une latence inutile.  
- **Solution implémentée :** utilisation du mécanisme **`lifespan` de FastAPI** pour charger le modèle **une seule fois au démarrage** du serveur, puis le conserver en mémoire pour toutes les prédictions ultérieures.  

#### 📊 Résultats du benchmark  

| Indicateur | Chargement à chaque requête | Modèle préchargé | Gain |
|-------------|-----------------------------|------------------|------|
| Temps moyen (ms) | 4.938 | 1.366 | 🔽 **−72.3 %** |
| P95 (ms) | 5.425 | 1.483 | 🔽 **−72.6 %** |

#### 🧠 Analyse du profilage `cProfile`  
- ✅ **Goulot principal identifié :** `joblib.load()` représentant **72 % du temps total d’exécution**.  
- ✅ **Optimisation confirmée :** suppression de ce rechargement récurrent = gain direct de performance.  
- 📄 **Résultats détaillés :** disponibles dans `performance_results/` (`cprofile_predict.txt`, `cprofile_proba.txt`, `profiling_results.txt`).  

#### 🚀 Impact global  
- Temps de réponse API réduit de **plus de 70 %**.  
- Stabilité améliorée (latence plus constante).  
- Aucune perte de précision ni modification du comportement du modèle. 

#### ❌  Stratégies d’optimisation non retenues — résumé

Plusieurs autres pistes d’optimisation ont été explorées mais écartées après expérimentation :

**Conversion en format ONNX** → incompatible avec certaines étapes du pipeline scikit-learn (ColumnTransformer, Encoder) et gain marginal (<10%).

**Rechargement asynchrone du modèle** → inutile car le modèle est déjà préchargé via le lifespan FastAPI et les prédictions sont non asynchrones.

**Parallélisation (multiprocessing / ThreadPool)** → redondante avec le parallélisme interne de scikit-learn (n_jobs=-1), ajoutant de la complexité sans gain réel.

**Mise en cache des prédictions** → inapplicable, car chaque client possède des données uniques, rendant le cache inefficace et risqué pour la confidentialité.

**Accélération GPU**  → non pertinente : scikit-learn ne tire pas parti du GPU et le modèle est trop léger pour compenser la latence d’E/S GPU.

----

## 👨‍💻 Auteur

**Nom :** Fatima-Zahra BARHOU  
**Version :** 3.0  
**Licence :** MIT
