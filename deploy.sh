#!/bin/bash

# Script de déploiement automatique sur Google Cloud Run
# Usage: ./deploy.sh [PROJECT_ID] [REGION]

set -e  # Arrêter en cas d'erreur

# Couleurs pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERREUR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[ATTENTION]${NC} $1"
}

# Vérifier les arguments
PROJECT_ID=${1:-""}
REGION=${2:-"europe-west1"}
SERVICE_NAME="bloodlink-backend"

if [ -z "$PROJECT_ID" ]; then
    print_error "Veuillez fournir l'ID du projet Google Cloud"
    echo "Usage: ./deploy.sh PROJECT_ID [REGION]"
    echo "Exemple: ./deploy.sh mon-projet-12345 europe-west1"
    exit 1
fi

print_info "Déploiement de $SERVICE_NAME sur Cloud Run"
print_info "Projet: $PROJECT_ID"
print_info "Région: $REGION"

# Vérifier si gcloud est installé
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud n'est pas installé. Installez Google Cloud SDK d'abord."
    exit 1
fi

# Vérifier si .env.yaml existe
if [ ! -f ".env.yaml" ]; then
    print_warning ".env.yaml n'existe pas."
    print_info "Création d'un fichier .env.yaml à partir du template..."

    # Générer une SECRET_KEY
    print_info "Génération d'une SECRET_KEY..."
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 2>/dev/null || python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

    cat > .env.yaml <<EOF
SECRET_KEY: "$SECRET_KEY"
DEBUG: "False"
ALLOWED_HOSTS: "*.run.app,127.0.0.1,localhost"
EOF
    print_info "Fichier .env.yaml créé avec une nouvelle SECRET_KEY"
fi

# Configurer le projet
print_info "Configuration du projet Google Cloud..."
gcloud config set project $PROJECT_ID

# Activer les APIs nécessaires
print_info "Activation des APIs nécessaires..."
gcloud services enable run.googleapis.com --quiet
gcloud services enable containerregistry.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet

# Déployer sur Cloud Run
print_info "Déploiement sur Cloud Run (cela peut prendre 5-10 minutes)..."
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --env-vars-file .env.yaml \
    --quiet

# Récupérer l'URL du service
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')

print_info "✅ Déploiement réussi!"
echo ""
echo "🌐 URL de votre API: $SERVICE_URL"
echo "📝 Endpoint principal: $SERVICE_URL/apiBloodlink/"
echo ""
print_warning "N'oubliez pas de mettre à jour ALLOWED_HOSTS dans .env.yaml avec cette URL:"
echo "ALLOWED_HOSTS: \"$(echo $SERVICE_URL | sed 's|https://||'),*.run.app,127.0.0.1,localhost\""
echo ""
print_info "Pour tester votre API:"
echo "curl $SERVICE_URL/apiBloodlink/"
