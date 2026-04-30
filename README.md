# Academiscan

Academiscan est une plateforme web développée avec **Flask** (Python) dédiée à l'observation de l'éducation, à l'analyse des données universitaires, du marché de l'emploi et de l'insertion professionnelle au Cameroun.

## Fonctionnalités Principales

1. **Questionnaires Dynamiques** : Création de questionnaires personnalisés (texte, QCM, échelles, dates) et recueil de réponses avec des liens publics partageables.
2. **Dashboard Administrateur et Public** : 
   - Statistiques globales publiques accessibles sans connexion.
   - Graphiques interactifs (taux de réponse, insertion professionnelle, etc.) générés via **Plotly**.
3. **Scraping Automatisé** : Collecte automatisée et quotidienne de données externes (offres d'emploi, actualités éducatives, classements universitaires) à l'aide de **BeautifulSoup4** et **APScheduler**.
4. **Centre d'Exportation** : Téléchargement des réponses aux questionnaires aux formats **CSV**, **Excel (.xlsx)** et **PDF**.

## Prérequis

- Python 3.8+
- (Optionnel) PostgreSQL si vous ne souhaitez pas utiliser la base de données SQLite par défaut.

## Installation

1. **Cloner ou télécharger le dépôt**

2. **Créer un environnement virtuel et l'activer :**
   ```bash
   # Sur Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Sur Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration :**
   Le projet inclut un fichier de configuration `.env` et utilise la librairie `python-decouple`. Par défaut, le projet est configuré pour tourner en mode Développement (avec une base **SQLite** locale `app.db`).

## Initialisation de la Base de Données

Avant le premier lancement, vous devez initialiser les tables et créer le compte administrateur. Exécutez la commande suivante :

```bash
flask init-db
```
*Note : Un compte administrateur par défaut sera créé :*
- **Email** : `admin@academiscan.local`
- **Mot de passe** : `admin123`

## Lancement de l'Application

Démarrez le serveur de développement :

```bash
flask run
```
*(ou `python app.py`)*

L'application sera accessible depuis votre navigateur à l'adresse : **http://127.0.0.1:5000**

## Automatisation (Scraping)

Le module de scraping est configuré avec **APScheduler** et lance automatiquement ses requêtes (emplois, classements, actualités) chaque jour à partir de 06h00.
Vous pouvez forcer une exécution manuelle en tant qu'administrateur via le menu **Scraping** > **Lancer manuellement**.

## Déploiement en Production

Pour la production, le fichier `Procfile` est déjà inclus pour un déploiement sur des services comme Heroku ou Render :
```
web: gunicorn app:app
```
Assurez-vous de configurer la variable d'environnement `FLASK_ENV=production` et d'ajuster `DATABASE_URL` pour pointer vers votre base de données PostgreSQL.
