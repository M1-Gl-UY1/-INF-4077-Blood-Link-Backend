@echo off
REM Script de déploiement pour Windows
REM Usage: deploy.bat PROJECT_ID [REGION]

setlocal enabledelayedexpansion

set PROJECT_ID=ilios-2f459
set REGION=us-central1
if "%REGION%"=="" set REGION=europe-west1
set SERVICE_NAME=bloodlink-backend

if "%PROJECT_ID%"=="" (
    echo [ERREUR] Veuillez fournir l'ID du projet Google Cloud
    echo Usage: deploy.bat PROJECT_ID [REGION]
    echo Exemple: deploy.bat mon-projet-12345 europe-west1
    exit /b 1
)

echo [INFO] Deploiement de %SERVICE_NAME% sur Cloud Run
echo [INFO] Projet: %PROJECT_ID%
echo [INFO] Region: %REGION%

REM Vérifier si gcloud est installé
where gcloud >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERREUR] gcloud n'est pas installe. Installez Google Cloud SDK d'abord.
    exit /b 1
)

REM Vérifier si .env.yaml existe
if not exist ".env.yaml" (
    echo [ATTENTION] .env.yaml n'existe pas.
    echo [INFO] Creation d'un fichier .env.yaml...

    REM Générer une SECRET_KEY
    for /f "delims=" %%i in ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') do set SECRET_KEY=%%i

    (
        echo SECRET_KEY: "!SECRET_KEY!"
        echo DEBUG: "False"
        echo ALLOWED_HOSTS: "*.run.app,127.0.0.1,localhost"
    ) > .env.yaml

    echo [INFO] Fichier .env.yaml cree avec une nouvelle SECRET_KEY
)

REM Configurer le projet
echo [INFO] Configuration du projet Google Cloud...
gcloud config set project %PROJECT_ID%

REM Activer les APIs nécessaires
echo [INFO] Activation des APIs necessaires...
gcloud services enable run.googleapis.com --quiet
gcloud services enable containerregistry.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet

REM Déployer sur Cloud Run
echo [INFO] Deploiement sur Cloud Run (cela peut prendre 5-10 minutes)...
gcloud run deploy %SERVICE_NAME% ^
    --source . ^
    --platform managed ^
    --region %REGION% ^
    --allow-unauthenticated ^
    --port 8080 ^
    --env-vars-file .env.yaml ^
    --quiet

REM Récupérer l'URL du service
for /f "delims=" %%i in ('gcloud run services describe %SERVICE_NAME% --region %REGION% --format "value(status.url)"') do set SERVICE_URL=%%i

echo.
echo [INFO] Deploiement reussi!
echo.
echo URL de votre API: %SERVICE_URL%
echo Endpoint principal: %SERVICE_URL%/apiBloodlink/
echo.
echo [ATTENTION] N'oubliez pas de mettre a jour ALLOWED_HOSTS dans .env.yaml
echo.
echo Pour tester votre API:
echo curl %SERVICE_URL%/apiBloodlink/

endlocal
