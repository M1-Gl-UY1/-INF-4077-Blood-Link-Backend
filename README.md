# 🩸 API BloodLink - Backend Django

## 📘 Introduction

**API BloodLink** est un backend développé avec **Django REST Framework** pour la gestion des opérations entre :
- Les **docteurs** 👨‍⚕️,
- Les **banques de sang** 🏥,
- Les **providers** (fournisseurs de sang) 🩸,  
- Et les **transactions de sang** 🔁.

Cette API centralise le processus complet de gestion du sang :
- Un **docteur** peut faire une **demande de sang** vers une **banque de sang** (`bloodRequests/`).
- Lorsqu’une **demande est validée**, une **alerte automatique** est générée pour que les **providers** puissent y répondre.
- Les **transactions de sang** sont ensuite créées et suivies dans le système.

> L’endpoint racine du backend est :  
> **`http://127.0.0.1:8000/apiBloodlink/`**

---

## ⚙️ Prérequis

Avant d’installer et d’exécuter ce projet, assure-toi d’avoir :

- 🐍 **Python 3.10+**
- 🌐 **Django 5+**
- 🧱 **Django REST Framework**
- 🗃️ **SQLite** (ou autre SGBD compatible)
- 🔐 **Virtualenv** (optionnel mais recommandé)
- 🧰 **Git**

---

## 🚀 Installation & Configuration

### 1️⃣ Clonage du projet

```bash
git clone git@github.com:M1-Gl-UY1/-INF-4077-Blood-Link-Backend.git
cd apiBloodlink

2️⃣ Création de l’environnement virtuel
python3 -m venv env
source env/bin/activate   # (Linux/Mac)
env\Scripts\activate      # (Windows)

3️⃣ Installation des dépendances
pip install -r requirements.txt

4️⃣ Configuration de la base de données

Le projet utilise SQLite par défaut.
Tu peux modifier les paramètres dans backend/settings.py.

5️⃣ Exécution du serveur
python manage.py migrate
python manage.py runserver


Le serveur démarre sur :
👉 http://127.0.0.1:8000/apiBloodlink/

Le backend est aussi Deployé sur :
[lien ou est hebergé le backend](https://inf-4077-blood-link-backend.onrender.com)


#   📍 Endpoints détaillés
🔐 Authentification & Utilisateurs
POST /registers/

Crée un nouvel utilisateur avec un rôle spécifique :

doctor, provider, ou bloodbank.

Cette route remplace les créations directes via /doctors/, /providers/, /bloodBanks/.

POST /registers/
{
  "username": "dr_house",
  "email":"dr_house@gmail.com"
  "password": "123456",
  "role": "doctor"
}
Reponse:
{
    "id": "73390e9b-6e5c-439d-a8ba-3ef440d08fdc",
    "username": "dr_house",
    "email": "dr_house@gmail.com",
    "role": "doctor"
}


POST /logins/

Connexion d’un utilisateur existant.

Body JSON :
{
  "email":"dr_house@gmail.com"
  "password": "123456"
}
ca cree directement un token de connexion qui va expirer apres 60 min.

{
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjczMzkwZTliLTZlNWMtNDM5ZC1hOGJhLTNlZjQ0MGQwOGZkYyIsImV4cCI6MTc2MTkxMjA2NiwiaWF0IjoxNzYxOTA4NDY2fQ.JqmIwyPVMMTlBiKSeYIBn_h9NoI15KPEQgj3GR-2dz4"
}

GET /users/

Liste tous les utilisateurs.

POST /logout/

Déconnecte l’utilisateur connecté.
{
    "email:"dr_house@gmail.com",
    "password":"1234"
}
ca suprime le token generé

---

👨‍⚕️ Docteurs
| Route                 | Méthode          | Description                                                       |
| --------------------- | ---------------- | ----------------------------------------------------------------- |
| `/doctors/`           | GET, POST        | Liste ou crée un docteur *(déprécié, remplacé par `/registers/`)* |
| `/doctors/<uuid:id>/` | GET, PUT, DELETE | Affiche, modifie ou supprime un docteur                           |

---

🏥 Banques de sang

| Route                    | Méthode          | Description                                                               |
| ------------------------ | ---------------- | ------------------------------------------------------------------------- |
| `/bloodBanks/`           | GET, POST        | Liste ou crée une banque de sang *(déprécié, remplacé par `/registers/`)* |
| `/bloodBanks/<uuid:id>/` | GET, PUT, DELETE | Affiche, modifie ou supprime une banque de sang                           |

---
💉 Providers
| Route                   | Méthode          | Description                                                        |
| ----------------------- | ---------------- | ------------------------------------------------------------------ |
| `/providers/`           | GET, POST        | Liste ou crée un provider *(déprécié, remplacé par `/registers/`)* |
| `/providers/<uuid:id>/` | GET, PUT, DELETE | Affiche, modifie ou supprime un provider                           |

# 🩸 Blood Requests (Demandes de sang)
GET /bloodRequests/

Liste toutes les demandes de sang.

POST /bloodRequests/

Un docteur envoie une demande à une banque de sang.
{
  "blood_group": "A",
  "rhesus": "+",
  "quantity": 1,
  "status": "En attente",
  "doctor": "Dr. (INT - GP)",
  "bank": "banque au prealable creer..."
}
REPONSE:

{
    "id": "d1b20e12-4d97-4029-9551-e6592910f475",
    "doctor_name": "",
    "bank_name": "",
    "date_request": "2025-10-31T11:32:35.368751Z",
    "blood_group": "A",
    "rhesus": "POS",
    "quantity": 1,
    "status": "pending",
    "docteur": "e0a02494-7ff9-4bb6-a899-5cf9d009e8ad",
    "bank": "9295e3c1-757c-43bf-9817-c10b39637c43"
}


✅ Validation d’une demande
POST /requests/<uuid:request_id>/validate/

La banque de sang valide une demande.
Cela crée automatiquement une alerte qu’un provider pourra consulter.

REPONSE:
{
    "id": "644d367e-d9ab-4663-a51b-0ed05ed109d3",
    "bank_name": "",
    "status": "PENDING",
    "created_date": "2025-10-31",
    "Resolved_date": null,
    "blood_groupe": "A",
    "rhesus": "POS",
    "bank": "9295e3c1-757c-43bf-9817-c10b39637c43"
}

🚨 Alerts (Alertes de sang)
| Route                            | Méthode          | Description                     |
| -------------------------------- | ---------------- | ------------------------------- |
| `/alerts/`                       | GET, POST        | Liste ou crée une alerte        |
| `/alerts/<uuid:id>/`             | GET, PUT, DELETE | Opérations sur une alerte       |
| `/alerts/<uuid:alert_id>/reply/` | POST             | Un provider répond à une alerte |




{
    "id": "e8d13a5c-58e0-4668-97b8-f3863941b554",
    "provider_name": "",
    "alert_status": "PENDING",
    "date": "2025-10-31T11:58:42.704537Z",
    "status": "RESPONDED",
    "provider": "504bfe0c-5ab4-4771-b245-fab8e364a30e",
    "alert": "644d367e-d9ab-4663-a51b-0ed05ed109d3"
}


📦 Blood Bags (Poches de sang): elle se creer automatiquement lors de la l'initiation d'une transaction sanguine elle est lié a un provider.
| Route                    | Méthode          | Description                        |
| ------------------------ | ---------------- | ---------------------------------- |
| `/blood_bags/`           | GET, POST        | Liste ou ajoute des poches de sang |
| `/blood_bags/<uuid:id>/` | GET, PUT, DELETE | Détails ou suppression d’une poche |


🔔 Alerts reçues par les providers: ce sont les alertes d'une banque qui ont été repondu par un provider:
| Route                        | Méthode          | Description                            |
| ---------------------------- | ---------------- | -------------------------------------- |
| `/receiveAlertes/`           | GET, POST        | Liste ou enregistre les alertes reçues |
| `/receiveAlertes/<uuid:id>/` | GET, PUT, DELETE | Gestion d’une alerte spécifique        |


🔄 Transactions de sang

| Route                           | Méthode          | Description                                                |
| ------------------------------- | ---------------- | ---------------------------------------------------------- |
| `/getbloodTransactions/`        | GET              | Liste toutes les transactions                              |
| `/postbloodTransactions/`       | POST             | Initialise une transaction (après validation d’une alerte) |
| `/bloodTransactions/<uuid:id>/` | GET, PUT, DELETE | Gère une transaction spécifique                            |





⚡ Version Documentation API (Résumé)
| Endpoint                                | Méthode          | Rôle principal                                    |
| --------------------------------------- | ---------------- | ------------------------------------------------- |
| `/registers/`                           | POST             | Crée un utilisateur (doctor, provider, bloodbank) |
| `/logins/`                              | POST             | Connexion                                         |
| `/users/`                               | GET              | Liste des utilisateurs                            |
| `/logout/`                              | POST             | Déconnexion                                       |
| `/doctors/`                             | GET, POST        | Gestion des docteurs *(déprécié)*                 |
| `/bloodBanks/`                          | GET, POST        | Gestion des banques de sang *(déprécié)*          |
| `/providers/`                           | GET, POST        | Gestion des providers *(déprécié)*                |
| `/bloodRequests/`                       | GET, POST        | Docteur crée une demande de sang                  |
| `/requests/<uuid:request_id>/validate/` | POST             | Validation d’une demande (création d’alerte)      |
| `/alerts/`                              | GET, POST        | Gestion des alertes                               |
| `/alerts/<uuid:alert_id>/reply/`        | POST             | Provider répond à une alerte                      |
| `/receiveAlertes/`                      | GET, POST        | Liste ou enregistre les alertes reçues            |
| `/blood_bags/`                          | GET, POST        | Gestion des poches de sang                        |
| `/getbloodTransactions/`                | GET              | Liste des transactions                            |
| `/postbloodTransactions/`               | POST             | Crée une transaction                              |
| `/bloodTransactions/<uuid:id>/`         | GET, PUT, DELETE | Gestion d’une transaction                         |


🧑‍💻 Auteur
Idriss TAGNY
Étudiant en Génie Logiciel – Université de Yaoundé I