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

## 🔐 Authentification & Utilisateurs

### POST /registers/
Crée un nouvel utilisateur avec un rôle spécifique : `doctor`, `provider`, ou `bank`.
Cette route remplace les créations directes via `/doctors/`, `/providers/`, `/bloodBanks/`.

**Paramètres requis:**
```json
{
  "username": "dr_house",
  "email": "dr_house@gmail.com",
  "password": "123456",
  "role": "doctor"  // Valeurs possibles: "doctor", "provider", "bank"
}
```

**Réponse (201 Created):**
```json
{
  "id": "73390e9b-6e5c-439d-a8ba-3ef440d08fdc",
  "username": "dr_house",
  "email": "dr_house@gmail.com",
  "role": "doctor"
}
```

---

### POST /logins/
Connexion d'un utilisateur existant. Génère un token JWT valide pendant **60 minutes**.

**Paramètres requis:**
```json
{
  "email": "dr_house@gmail.com",
  "password": "123456"
}
```

**Réponse (200 OK):**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjczMzkwZTliLTZlNWMtNDM5ZC1hOGJhLTNlZjQ0MGQwOGZkYyIsImV4cCI6MTc2MTkxMjA2NiwiaWF0IjoxNzYxOTA4NDY2fQ.JqmIwyPVMMTlBiKSeYIBn_h9NoI15KPEQgj3GR-2dz4"
}
```

**Note:** Le token est également stocké dans un cookie `httponly` nommé `jwt`.

---

### GET /users/
Récupère les informations de l'utilisateur connecté. **Nécessite un token JWT valide**.

**Paramètres requis (dans le body):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Réponse (200 OK):**
```json
{
  "id": "73390e9b-6e5c-439d-a8ba-3ef440d08fdc",
  "username": "dr_house",
  "email": "dr_house@gmail.com",
  "role": "doctor"
}
```

**Erreurs possibles:**
- `401 Unauthenticated` - Token manquant ou expiré

---

### POST /logout/
Déconnecte l'utilisateur en supprimant le cookie JWT.

**Réponse (200 OK):**
```json
{
  "message": "success"
}
```

---

## 👨‍⚕️ Docteurs

### GET /doctors/
Liste tous les docteurs avec leurs demandes de sang associées.

**Réponse (200 OK):**
```json
[
  {
    "id": "e0a02494-7ff9-4bb6-a899-5cf9d009e8ad",
    "name": "Dr. House",
    "grade": "INT",  // INT, RES, ASS, SPC, CHS, PRF
    "speciality": "GP",  // GP, CD, NE, OR, PD
    "user": {
      "id": "73390e9b-6e5c-439d-a8ba-3ef440d08fdc",
      "username": "dr_house",
      "email": "dr_house@gmail.com",
      "role": "doctor"
    },
    "blood_bank": "9295e3c1-757c-43bf-9817-c10b39637c43",
    "bank_id": "9295e3c1-757c-43bf-9817-c10b39637c43",
    "blood_requests": []
  }
]
```

### POST /doctors/
**(Déprécié - Utiliser `/registers/` à la place)**
Crée un nouveau docteur directement.

### GET /doctors/<uuid:id>/
Récupère les détails d'un docteur spécifique.

**Réponse (200 OK):** Même structure que GET /doctors/ (objet unique)

### PUT /doctors/<uuid:id>/
Met à jour les informations d'un docteur.

**Paramètres (tous optionnels):**
```json
{
  "name": "Dr. House Updated",
  "grade": "SPC",
  "speciality": "CD",
  "blood_bank": "uuid-de-la-banque"
}
```

### DELETE /doctors/<uuid:id>/
Supprime un docteur.

**Réponse (204 No Content)**

---

## 🏥 Banques de sang

### GET /bloodBanks/
Liste toutes les banques de sang avec leurs transactions.

**Réponse (200 OK):**
```json
[
  {
    "id": "9295e3c1-757c-43bf-9817-c10b39637c43",
    "name": "Banque Centrale de Yaoundé",
    "location": "Yaoundé, Cameroun",
    "password": "pbkdf2_sha256$...",  // Mot de passe hashé
    "user": {
      "id": "uuid",
      "username": "banque_yaounde",
      "email": "banque@example.com",
      "role": "bank"
    },
    "transactions": []
  }
]
```

### POST /bloodBanks/
**(Déprécié - Utiliser `/registers/` à la place)**

### GET /bloodBanks/<uuid:id>/
Récupère les détails d'une banque spécifique.

### PUT /bloodBanks/<uuid:id>/
Met à jour les informations d'une banque.

**Paramètres (tous optionnels):**
```json
{
  "name": "Nouveau nom",
  "location": "Nouvelle adresse",
  "password": "nouveau_mot_de_passe"
}
```

### DELETE /bloodBanks/<uuid:id>/
Supprime une banque de sang.

**Réponse (204 No Content)**

---

## 💉 Providers (Fournisseurs/Donneurs)

### GET /providers/
Liste tous les providers.

**Réponse (200 OK):**
```json
[
  {
    "id": "504bfe0c-5ab4-4771-b245-fab8e364a30e",
    "name": "Jean Dupont",
    "sexe": "M",  // M ou F
    "date_birth": "1990-01-15",
    "email": "jean.dupont@example.com",
    "phone_number": "+237123456789",
    "blood_group": "A",  // A, B, AB, O
    "rhesus": "+",  // + ou -
    "last_give": "2024-12-01",
    "historique_medical": null,
    "user": {
      "id": "uuid",
      "username": "jean_dupont",
      "email": "jean.dupont@example.com",
      "role": "provider"
    }
  }
]
```

### POST /providers/
**(Déprécié - Utiliser `/registers/` à la place)**

### GET /providers/<uuid:id>/
Récupère les détails d'un provider spécifique.

### PUT /providers/<uuid:id>/
Met à jour les informations d'un provider.

**Paramètres (tous optionnels):**
```json
{
  "name": "Jean Dupont",
  "sexe": "M",
  "date_birth": "1990-01-15",
  "email": "jean.dupont@example.com",
  "phone_number": "+237123456789",
  "blood_group": "A",
  "rhesus": "+",
  "last_give": "2024-12-01"
}
```

### DELETE /providers/<uuid:id>/
Supprime un provider.

**Réponse (204 No Content)**

---

## 🩸 Blood Requests (Demandes de sang)

### GET /bloodRequests/
Liste toutes les demandes de sang.

**Réponse (200 OK):**
```json
[
  {
    "id": "d1b20e12-4d97-4029-9551-e6592910f475",
    "doctor_name": "Dr. House",
    "bank_name": "Banque Centrale",
    "date_request": "2025-10-31T11:32:35.368751Z",
    "blood_group": "A",  // A, B, AB, O
    "rhesus": "POS",  // POS ou NEG
    "quantity": 1,
    "status": "pending",  // pending, approved, rejected
    "docteur": "e0a02494-7ff9-4bb6-a899-5cf9d009e8ad",
    "bank": "9295e3c1-757c-43bf-9817-c10b39637c43",
    "user": {
      "id": "uuid",
      "username": "dr_house",
      "email": "dr_house@gmail.com",
      "role": "doctor"
    }
  }
]
```

### POST /bloodRequests/
Un docteur crée une demande de sang vers une banque.

**Paramètres requis:**
```json
{
  "blood_group": "A",  // A, B, AB, O
  "rhesus": "POS",  // POS ou NEG
  "quantity": 1,
  "docteur": "e0a02494-7ff9-4bb6-a899-5cf9d009e8ad",  // UUID du docteur
  "bank": "9295e3c1-757c-43bf-9817-c10b39637c43"  // UUID de la banque
}
```

**Paramètres optionnels:**
```json
{
  "status": "pending"  // Par défaut: pending
}
```

**Réponse (201 Created):**
```json
{
  "id": "d1b20e12-4d97-4029-9551-e6592910f475",
  "doctor_name": "Dr. House",
  "bank_name": "Banque Centrale",
  "date_request": "2025-10-31T11:32:35.368751Z",
  "blood_group": "A",
  "rhesus": "POS",
  "quantity": 1,
  "status": "pending",
  "docteur": "e0a02494-7ff9-4bb6-a899-5cf9d009e8ad",
  "bank": "9295e3c1-757c-43bf-9817-c10b39637c43"
}
```

### GET /bloodRequests/<uuid:id>/
Récupère les détails d'une demande spécifique.

**Réponse (200 OK):** Même structure que POST /bloodRequests/

### PUT /bloodRequests/<uuid:id>/
Met à jour une demande de sang.

**Paramètres (tous optionnels):**
```json
{
  "blood_group": "B",
  "rhesus": "NEG",
  "quantity": 2,
  "status": "approved"
}
```

### DELETE /bloodRequests/<uuid:id>/
Supprime une demande de sang.

**Réponse (204 No Content)**

---

## ✅ Validation de demande

### POST /requests/<uuid:request_id>/validate/
La banque de sang valide une demande. **Crée automatiquement une alerte** qu'un provider pourra consulter.

**Aucun paramètre requis (le request_id suffit)**

**Réponse (200 OK):**
```json
{
  "id": "644d367e-d9ab-4663-a51b-0ed05ed109d3",
  "bank_name": "Banque Centrale",
  "status": "PENDING",  // PENDING, SENT, RECEIVED, IN_PROGRESS, RESOLVED, CANCELLED, FAILED
  "created_date": "2025-10-31",
  "Resolved_date": null,
  "blood_groupe": "A",
  "rhesus": "POS",
  "bank": "9295e3c1-757c-43bf-9817-c10b39637c43"
}
```

**Erreur (400 Bad Request):**
```json
{
  "error": "Requête introuvable ou déjà traitée."
}
```

---

## 🚨 Alerts (Alertes de sang)

### GET /alerts/
Liste toutes les alertes émises par les banques.

**Réponse (200 OK):**
```json
[
  {
    "id": "644d367e-d9ab-4663-a51b-0ed05ed109d3",
    "bank_name": "Banque Centrale",
    "status": "PENDING",
    "created_date": "2025-10-31",
    "Resolved_date": null,
    "blood_groupe": "A",
    "rhesus": "POS",
    "bank": "9295e3c1-757c-43bf-9817-c10b39637c43"
  }
]
```

### POST /alerts/
Crée une nouvelle alerte (généralement créée automatiquement via la validation de demande).

**Paramètres requis:**
```json
{
  "blood_groupe": "A",
  "rhesus": "POS",
  "bank": "9295e3c1-757c-43bf-9817-c10b39637c43"
}
```

**Paramètres optionnels:**
```json
{
  "status": "PENDING",
  "Resolved_date": "2025-11-15"
}
```

### GET /alerts/<uuid:id>/
Récupère les détails d'une alerte spécifique.

### PUT /alerts/<uuid:id>/
Met à jour une alerte.

### DELETE /alerts/<uuid:id>/
Supprime une alerte.

**Réponse (204 No Content)**

---

## 💬 Réponse à une alerte

### POST /alerts/<uuid:alert_id>/reply/
Un provider répond à une alerte de banque de sang.

**Paramètres requis:**
```json
{
  "provider_id": "504bfe0c-5ab4-4771-b245-fab8e364a30e"
}
```

**Réponse (201 Created):**
```json
{
  "id": "e8d13a5c-58e0-4668-97b8-f3863941b554",
  "provider_name": "Jean Dupont",
  "alert_status": "PENDING",
  "date": "2025-10-31T11:58:42.704537Z",
  "status": "RESPONDED",  // PENDING, RESPONDED, COMPLETED, CANCELLED
  "provider": "504bfe0c-5ab4-4771-b245-fab8e364a30e",
  "alert": "644d367e-d9ab-4663-a51b-0ed05ed109d3"
}
```

**Erreur (400 Bad Request):**
```json
{
  "error": "Réponse déjà existante ou alerte introuvable"
}
```

ou

```json
{
  "errors": "provider_id manquant"
}
```

---

## 🔔 Alertes reçues par les providers

### GET /receiveAlertes/
Liste toutes les alertes reçues/répondues par les providers.

**Réponse (200 OK):**
```json
[
  {
    "id": "e8d13a5c-58e0-4668-97b8-f3863941b554",
    "provider_name": "Jean Dupont",
    "alert_status": "PENDING",
    "date": "2025-10-31T11:58:42.704537Z",
    "status": "RESPONDED",
    "provider": "504bfe0c-5ab4-4771-b245-fab8e364a30e",
    "alert": "644d367e-d9ab-4663-a51b-0ed05ed109d3"
  }
]
```

### POST /receiveAlertes/
Enregistre une nouvelle réponse à une alerte (généralement créée via `/alerts/<uuid:alert_id>/reply/`).

### GET /receiveAlertes/<uuid:id>/
Récupère les détails d'une alerte reçue spécifique.

### PUT /receiveAlertes/<uuid:id>/
Met à jour le statut d'une alerte reçue.

**Paramètres (optionnels):**
```json
{
  "status": "COMPLETED"
}
```

### DELETE /receiveAlertes/<uuid:id>/
Supprime une alerte reçue.

**Réponse (204 No Content)**

---

## 📦 Blood Bags (Poches de sang)

### GET /blood_bags/
Liste toutes les poches de sang. **Se créent automatiquement lors de l'initiation d'une transaction.**

**Réponse (200 OK):**
```json
[
  {
    "id": "uuid",
    "blood_group": "A",  // A, B, AB, O
    "rhesus": "POS",  // POS ou NEG
    "provider": "504bfe0c-5ab4-4771-b245-fab8e364a30e",
    "providerFor_name": "Jean Dupont"
  }
]
```

### POST /blood_bags/
Crée une nouvelle poche de sang.

**Paramètres requis:**
```json
{
  "blood_group": "A",
  "rhesus": "POS",
  "provider": "504bfe0c-5ab4-4771-b245-fab8e364a30e"
}
```

### GET /blood_bags/<uuid:id>/
Récupère les détails d'une poche spécifique.

### PUT /blood_bags/<uuid:id>/
Met à jour une poche de sang.

### DELETE /blood_bags/<uuid:id>/
Supprime une poche de sang.

**Réponse (204 No Content)**

---

## 🔄 Transactions de sang

### GET /getbloodTransactions/
Liste toutes les transactions de sang entre providers et banques.

**Réponse (200 OK):**
```json
[
  {
    "id": "uuid",
    "provider_name": "Jean Dupont",
    "bank_name": "Banque Centrale",
    "date": "2025-10-31T12:00:00Z",
    "provider": "504bfe0c-5ab4-4771-b245-fab8e364a30e",
    "bank": "9295e3c1-757c-43bf-9817-c10b39637c43",
    "blood_bag": "uuid-de-la-poche"
  }
]
```

### POST /postbloodTransactions/
Initialise une nouvelle transaction de sang (après validation d'une alerte).
**Crée automatiquement une poche de sang** liée au provider.

**Paramètres requis:**
```json
{
  "provider_id": "504bfe0c-5ab4-4771-b245-fab8e364a30e",
  "bank_id": "9295e3c1-757c-43bf-9817-c10b39637c43"
}
```

**Réponse (200 OK):**
```json
{
  "id": "uuid",
  "provider_name": "Jean Dupont",
  "bank_name": "Banque Centrale",
  "date": "2025-10-31T12:00:00Z",
  "provider": "504bfe0c-5ab4-4771-b245-fab8e364a30e",
  "bank": "9295e3c1-757c-43bf-9817-c10b39637c43",
  "blood_bag": "uuid-de-la-poche-creee"
}
```

**Erreur (400 Bad Request):**
```json
{
  "error": "Requête introuvable ou déjà traitée."
}
```

### GET /bloodTransactions/<uuid:id>/
Récupère les détails d'une transaction spécifique.

### PUT /bloodTransactions/<uuid:id>/
Met à jour une transaction.

### DELETE /bloodTransactions/<uuid:id>/
Supprime une transaction.

**Réponse (204 No Content)**

---

## ⚡ Tableau récapitulatif de tous les endpoints

| Endpoint                                | Méthode          | Rôle principal                                    | Statut         |
| --------------------------------------- | ---------------- | ------------------------------------------------- | -------------- |
| `/registers/`                           | POST             | Crée un utilisateur (doctor, provider, bank)      | ✅ Actif       |
| `/logins/`                              | POST             | Connexion (génère token JWT)                      | ✅ Actif       |
| `/users/`                               | GET              | Récupère infos utilisateur connecté               | ✅ Actif       |
| `/logout/`                              | POST             | Déconnexion (supprime token)                      | ✅ Actif       |
| `/doctors/`                             | GET, POST        | Liste/crée des docteurs                           | ⚠️ Déprécié    |
| `/doctors/<uuid:id>/`                   | GET, PUT, DELETE | Gère un docteur spécifique                        | ✅ Actif       |
| `/bloodBanks/`                          | GET, POST        | Liste/crée des banques                            | ⚠️ Déprécié    |
| `/bloodBanks/<uuid:id>/`                | GET, PUT, DELETE | Gère une banque spécifique                        | ✅ Actif       |
| `/providers/`                           | GET, POST        | Liste/crée des providers                          | ⚠️ Déprécié    |
| `/providers/<uuid:id>/`                 | GET, PUT, DELETE | Gère un provider spécifique                       | ✅ Actif       |
| `/bloodRequests/`                       | GET, POST        | Liste/crée des demandes de sang                   | ✅ Actif       |
| `/bloodRequests/<uuid:id>/`             | GET, PUT, DELETE | Gère une demande spécifique                       | ✅ Actif       |
| `/requests/<uuid:request_id>/validate/` | POST             | Validation demande → crée alerte automatiquement  | ✅ Actif       |
| `/alerts/`                              | GET, POST        | Liste/crée des alertes                            | ✅ Actif       |
| `/alerts/<uuid:id>/`                    | GET, PUT, DELETE | Gère une alerte spécifique                        | ✅ Actif       |
| `/alerts/<uuid:alert_id>/reply/`        | POST             | Provider répond à une alerte                      | ✅ Actif       |
| `/receiveAlertes/`                      | GET, POST        | Liste/enregistre alertes reçues                   | ✅ Actif       |
| `/receiveAlertes/<uuid:id>/`            | GET, PUT, DELETE | Gère une alerte reçue spécifique                  | ✅ Actif       |
| `/blood_bags/`                          | GET, POST        | Liste/crée des poches de sang                     | ✅ Actif       |
| `/blood_bags/<uuid:id>/`                | GET, PUT, DELETE | Gère une poche spécifique                         | ✅ Actif       |
| `/getbloodTransactions/`                | GET              | Liste toutes les transactions                     | ✅ Actif       |
| `/postbloodTransactions/`               | POST             | Crée transaction + poche automatiquement          | ✅ Actif       |
| `/bloodTransactions/<uuid:id>/`         | GET, PUT, DELETE | Gère une transaction spécifique                   | ✅ Actif       |

---

## 📊 Flux de travail typique

### 1. Inscription et Connexion
```
POST /registers/ → POST /logins/ → Obtient JWT token
```

### 2. Demande de sang (Docteur → Banque)
```
POST /bloodRequests/ → Docteur crée une demande
```

### 3. Validation et Alerte (Banque)
```
POST /requests/<id>/validate/ → Crée automatiquement une alerte
```

### 4. Réponse du Provider
```
POST /alerts/<id>/reply/ → Provider répond à l'alerte
```

### 5. Transaction finale
```
POST /postbloodTransactions/ → Crée transaction + poche de sang
```

---

## 🔑 Authentification JWT

Après connexion via `/logins/`, vous recevez un token JWT dans la réponse:
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Durée de validité:** 60 minutes

**Utilisation du token:**
- Pour `/users/`, envoyez le token dans le body:
  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

**Déconnexion:**
- Utilisez `POST /logout/` pour supprimer le cookie JWT

---

## 📝 Codes de statut HTTP

| Code | Signification | Utilisation |
|------|---------------|-------------|
| 200 | OK | Requête réussie (GET, PUT) |
| 201 | Created | Ressource créée avec succès (POST) |
| 204 | No Content | Suppression réussie (DELETE) |
| 400 | Bad Request | Paramètres manquants ou invalides |
| 401 | Unauthorized | Token manquant, expiré ou invalide |
| 404 | Not Found | Ressource introuvable |

---

## 🎯 Valeurs des énumérations

### Rôles utilisateur
- `doctor` - Docteur
- `provider` - Fournisseur/Donneur
- `bank` - Banque de sang

### Grades docteur
- `INT` - Interne
- `RES` - Résident
- `ASS` - Assistant médical
- `SPC` - Spécialiste
- `CHS` - Chef de service
- `PRF` - Professeur

### Spécialités docteur
- `GP` - Généraliste
- `CD` - Cardiologue
- `NE` - Neurologue
- `OR` - Orthopédiste
- `PD` - Pédiatre

### Groupes sanguins
- `A`, `B`, `AB`, `O`

### Rhésus
- `POS` (Positif +)
- `NEG` (Négatif -)

### Statuts demande de sang
- `pending` - En attente
- `approved` - Approuvée
- `rejected` - Rejetée

### Statuts alerte
- `PENDING` - En attente
- `SENT` - Envoyée
- `RECEIVED` - Reçue
- `IN_PROGRESS` - En cours de traitement
- `RESOLVED` - Résolue
- `CANCELLED` - Annulée
- `FAILED` - Échouée

### Statuts alerte reçue
- `PENDING` - En attente de réponse
- `RESPONDED` - Répondue
- `COMPLETED` - Terminée avec succès
- `CANCELLED` - Annulée

### Sexe
- `M` - Masculin
- `F` - Féminin


🧑‍💻 Auteur
Idriss TAGNY
Étudiant en Génie Logiciel – Université de Yaoundé I