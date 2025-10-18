# -------------------------
# Dockerfile pour API FastAPI
# -------------------------

# Image de base
FROM python:3.12.2-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tous les fichiers du projet dans le conteneur
COPY . /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l’API
EXPOSE 7860

# Commande de démarrage de l’API
CMD ["uvicorn", "API_Fastapi:app", "--host", "0.0.0.0", "--port", "7860"]
