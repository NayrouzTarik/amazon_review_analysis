FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers de l'application
COPY . .

# Rendre le fichier app.py exécutable
RUN chmod +x app.py

# Exposer le port
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
