# Guide de Déploiement sur Google Cloud Run / Firebase

Ce guide vous explique comment déployer le backend BloodLink sur Google Cloud Run via Firebase.

## Prérequis

1. **Compte Google Cloud / Firebase**
   - Créez un compte sur [console.cloud.google.com](https://console.cloud.google.com)
   - Ou utilisez [console.firebase.google.com](https://console.firebase.google.com)

2. **Installation des outils CLI**
   ```bash
   # Installer Google Cloud SDK
   # Windows: Téléchargez depuis https://cloud.google.com/sdk/docs/install
   # Linux/Mac:
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL

   # Installer Firebase CLI
   npm install -g firebase-tools
   ```

3. **Projet Firebase/Google Cloud**
   - Créez un nouveau projet sur Firebase Console
   - Notez l'ID du projet (PROJECT_ID)

## Méthode 1: Déploiement Manuel (Recommandé pour débuter)

### Étape 1: Configuration initiale

```bash
# Se connecter à Google Cloud
gcloud auth login

# Configurer le projet
gcloud config set project VOTRE_PROJECT_ID

# Activer les APIs nécessaires
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Étape 2: Générer une clé secrète Django

```bash
# Sur Windows (PowerShell)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Sur Linux/Mac
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiez la clé générée, vous en aurez besoin pour la suite.

### Étape 3: Configuration des variables d'environnement

Créez un fichier `.env.yaml` à la racine du projet:

```yaml
SECRET_KEY: "votre-cle-secrete-generee-a-l-etape-2"
DEBUG: "False"
ALLOWED_HOSTS: "*.run.app,127.0.0.1,localhost"
```

**IMPORTANT:** N'ajoutez JAMAIS ce fichier à Git! Il est déjà dans `.gitignore`.

### Étape 4: Construire et déployer

```bash
# Définir la région (choisissez celle la plus proche)
# europe-west1 (Belgique) - Recommandé pour l'Afrique/Europe
# us-central1 (Iowa) - USA
# asia-east1 (Taïwan) - Asie
REGION="europe-west1"

# Construire l'image Docker et déployer sur Cloud Run
gcloud run deploy bloodlink-backend \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --env-vars-file .env.yaml
```

Le déploiement prendra 5-10 minutes. À la fin, vous obtiendrez une URL du type:
```
https://bloodlink-backend-xxxxxxxxxx-ew.a.run.app
```

### Étape 5: Mettre à jour ALLOWED_HOSTS

Après le premier déploiement, mettez à jour votre `.env.yaml`:

```yaml
SECRET_KEY: "votre-cle-secrete"
DEBUG: "False"
ALLOWED_HOSTS: "bloodlink-backend-xxxxxxxxxx-ew.a.run.app,*.run.app,127.0.0.1,localhost"
```

Redéployez:
```bash
gcloud run deploy bloodlink-backend \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --env-vars-file .env.yaml
```

### Étape 6: Tester l'API

```bash
# Remplacez URL_DE_VOTRE_APP par l'URL obtenue
curl https://URL_DE_VOTRE_APP/apiBloodlink/
```

## Méthode 2: Déploiement via Cloud Build (Automatisé)

### Configuration initiale

```bash
# Activer Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Configurer les variables d'environnement dans Cloud Run
gcloud run services update bloodlink-backend \
  --region europe-west1 \
  --update-env-vars SECRET_KEY="votre-cle-secrete" \
  --update-env-vars DEBUG="False" \
  --update-env-vars ALLOWED_HOSTS="*.run.app,127.0.0.1,localhost"
```

### Déploiement automatique

```bash
# Utiliser le fichier cloudbuild.yaml
gcloud builds submit --config cloudbuild.yaml .
```

## Méthode 3: Configuration avec Base de Données Cloud SQL (Production)

Pour une utilisation en production, utilisez Cloud SQL PostgreSQL au lieu de SQLite.

### Créer une instance Cloud SQL

```bash
# Créer l'instance PostgreSQL
gcloud sql instances create bloodlink-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=europe-west1

# Créer la base de données
gcloud sql databases create bloodlink --instance=bloodlink-db

# Créer un utilisateur
gcloud sql users create bloodlink-user \
  --instance=bloodlink-db \
  --password=CHOISISSEZ_UN_MOT_DE_PASSE_FORT
```

### Mettre à jour .env.yaml

```yaml
SECRET_KEY: "votre-cle-secrete"
DEBUG: "False"
ALLOWED_HOSTS: "*.run.app,127.0.0.1,localhost"
DATABASE_URL: "postgresql://bloodlink-user:VOTRE_MOT_DE_PASSE@//cloudsql/VOTRE_PROJECT_ID:europe-west1:bloodlink-db/bloodlink"
```

### Redéployer avec Cloud SQL

```bash
gcloud run deploy bloodlink-backend \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --port 8080 \
  --env-vars-file .env.yaml \
  --add-cloudsql-instances VOTRE_PROJECT_ID:europe-west1:bloodlink-db
```

## Gestion des Migrations

Après chaque déploiement, exécutez les migrations:

```bash
# Connexion à Cloud Run pour exécuter les migrations
gcloud run jobs create bloodlink-migrate \
  --image gcr.io/VOTRE_PROJECT_ID/bloodlink-backend:latest \
  --region europe-west1 \
  --env-vars-file .env.yaml \
  --command python \
  --args manage.py,migrate

# Exécuter la migration
gcloud run jobs execute bloodlink-migrate --region europe-west1
```

Ou via Cloud Shell:

```bash
# Ouvrir Cloud Shell depuis la console
# Puis exécuter:
docker run --rm \
  -e SECRET_KEY="votre-cle" \
  gcr.io/VOTRE_PROJECT_ID/bloodlink-backend:latest \
  python manage.py migrate
```

## Configuration du Domaine Personnalisé (Optionnel)

Si vous avez un nom de domaine:

```bash
# Mapper le domaine
gcloud run domain-mappings create \
  --service bloodlink-backend \
  --domain api.votre-domaine.com \
  --region europe-west1
```

Suivez les instructions pour configurer les enregistrements DNS.

## Surveillance et Logs

### Voir les logs

```bash
# Logs en temps réel
gcloud run logs tail bloodlink-backend --region europe-west1

# Logs dans la console
# https://console.cloud.google.com/run/detail/REGION/SERVICE/logs
```

### Monitoring

Accédez au monitoring:
```
https://console.cloud.google.com/run/detail/REGION/bloodlink-backend/metrics
```

## Mise à Jour de l'Application

Pour mettre à jour l'application après des modifications:

```bash
# 1. Committez vos changements
git add .
git commit -m "Description des modifications"

# 2. Redéployez
gcloud run deploy bloodlink-backend \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --port 8080 \
  --env-vars-file .env.yaml
```

## Variables d'Environnement Disponibles

| Variable | Description | Obligatoire | Valeur par défaut |
|----------|-------------|-------------|-------------------|
| `SECRET_KEY` | Clé secrète Django | Oui | - |
| `DEBUG` | Mode debug | Non | False |
| `ALLOWED_HOSTS` | Hôtes autorisés (séparés par virgule) | Non | *.run.app,localhost |
| `DATABASE_URL` | URL de connexion PostgreSQL | Non | SQLite |
| `PORT` | Port d'écoute | Non | 8080 |

## Sécurité

### Bonnes pratiques:

1. **Utilisez toujours une SECRET_KEY unique et complexe**
2. **Ne commitez JAMAIS .env.yaml ou .env dans Git**
3. **Utilisez Cloud SQL pour la production, pas SQLite**
4. **Activez HTTPS (activé par défaut sur Cloud Run)**
5. **Limitez l'accès avec IAM si nécessaire**

### Activer l'authentification (optionnel)

Pour désactiver l'accès public:

```bash
gcloud run services update bloodlink-backend \
  --region europe-west1 \
  --no-allow-unauthenticated
```

## Dépannage

### Erreur "ALLOWED_HOSTS"
- Vérifiez que l'URL Cloud Run est dans ALLOWED_HOSTS
- Utilisez `*.run.app` pour accepter tous les sous-domaines

### Erreur "SECRET_KEY"
- Générez une nouvelle clé avec la commande Python fournie
- Vérifiez que .env.yaml est bien chargé

### L'application ne démarre pas
- Vérifiez les logs: `gcloud run logs tail bloodlink-backend`
- Assurez-vous que le port 8080 est utilisé

### Migrations non appliquées
- Exécutez les migrations manuellement (voir section Gestion des Migrations)

## Coûts Estimés

- **Cloud Run (Gratuit jusqu'à):**
  - 2 millions de requêtes/mois
  - 360 000 GB-secondes de RAM
  - 180 000 vCPU-secondes

- **Cloud SQL (db-f1-micro):**
  - ~7-10 USD/mois (instance la moins chère)
  - Alternative: Utilisez SQLite pour le développement

- **Container Registry:**
  - Gratuit jusqu'à 1 GB
  - ~0.026 USD/GB/mois au-delà

## Support

- **Documentation Cloud Run:** https://cloud.google.com/run/docs
- **Documentation Firebase:** https://firebase.google.com/docs
- **Support Google Cloud:** https://cloud.google.com/support

## Auteur

Idriss TAGNY
Université de Yaoundé I
