# Déploiement Rapide sur Google Cloud Run / Firebase

## Méthode Rapide (Recommandée)

### 1. Prérequis
- Installez [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- Créez un projet sur [Firebase Console](https://console.firebase.google.com)

### 2. Authentification
```bash
gcloud auth login
```

### 3. Déploiement en une commande

**Sur Windows:**
```cmd
deploy.bat VOTRE_PROJECT_ID
```

**Sur Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh VOTRE_PROJECT_ID
```

Remplacez `VOTRE_PROJECT_ID` par l'ID de votre projet Firebase.

### 4. C'est tout!

Votre API sera accessible à l'URL fournie à la fin du déploiement:
```
https://bloodlink-backend-xxxxx-ew.a.run.app/apiBloodlink/
```

## Options Avancées

### Spécifier une région différente

**Régions disponibles:**
- `europe-west1` - Belgique (par défaut, recommandé pour l'Afrique/Europe)
- `us-central1` - Iowa, USA
- `asia-east1` - Taïwan
- `us-east1` - Caroline du Sud
- Voir toutes les régions: https://cloud.google.com/run/docs/locations

**Exemple:**
```bash
./deploy.sh mon-projet us-central1
```

### Utiliser Cloud SQL PostgreSQL (Production)

Consultez `DEPLOYMENT.md` section "Méthode 3" pour la configuration complète.

## Fichiers Créés

- `Dockerfile` - Configuration Docker pour containeriser l'app
- `.dockerignore` - Fichiers à exclure du conteneur
- `cloudbuild.yaml` - Configuration Cloud Build (déploiement automatisé)
- `.env.yaml.example` - Template de configuration
- `deploy.sh` / `deploy.bat` - Scripts de déploiement rapide
- `DEPLOYMENT.md` - Guide complet de déploiement

## Variables d'Environnement

Éditez `.env.yaml` pour configurer:
```yaml
SECRET_KEY: "votre-cle-secrete"
DEBUG: "False"
ALLOWED_HOSTS: "votre-app.run.app,*.run.app,127.0.0.1,localhost"
```

## Commandes Utiles

```bash
# Voir les logs
gcloud run logs tail bloodlink-backend --region europe-west1

# Redéployer après modifications
./deploy.sh VOTRE_PROJECT_ID

# Supprimer le service
gcloud run services delete bloodlink-backend --region europe-west1
```

## Documentation Complète

Consultez `DEPLOYMENT.md` pour:
- Configuration détaillée
- Utilisation de Cloud SQL
- Gestion des migrations
- Configuration d'un domaine personnalisé
- Dépannage

## Support

Pour plus d'aide, consultez:
- [Documentation Cloud Run](https://cloud.google.com/run/docs)
- [Documentation Django](https://docs.djangoproject.com/)
