# SecureStack

SecureStack est une API REST orientée exploitation et sécurité, conçue pour gérer des serveurs, des tâches de sauvegarde et des incidents dans un contexte proche de la production.

Le projet vise à démontrer une montée en compétence vers les métiers du développement back-end, du cloud et de la cybersécurité, à travers des choix techniques cohérents et une architecture maîtrisée.

---

## Présentation

SecureStack est développé avec Django et Django REST Framework.  
Il reproduit des problématiques concrètes rencontrées dans des environnements systèmes et cloud :

- gestion d’actifs (serveurs)
- contrôle d’accès et permissions
- traçabilité des actions
- sécurisation d’API
- préparation au déploiement conteneurisé

Le projet est volontairement centré sur le back-end et l’architecture applicative.

---

## Objectifs techniques

- Concevoir une API REST structurée, maintenable et extensible
- Implémenter une authentification sécurisée par JWT
- Mettre en place une gestion fine des permissions et des rôles
- Journaliser les actions critiques à des fins d’audit
- Conteneuriser l’application pour un déploiement reproductible
- Préparer une architecture compatible cloud

---

## Fonctionnalités

### Authentification et utilisateurs
- Inscription et connexion
- Authentification JWT avec expiration
- Protection des endpoints sensibles
- Rôles utilisateur (utilisateur, administrateur)

### Gestion des serveurs
- CRUD complet des serveurs
- Association serveur – utilisateur
- Suivi du statut (actif, maintenance, hors ligne)

### Gestion des sauvegardes
- Création de tâches de sauvegarde
- Suivi de l’état des backups
- Historique des sauvegardes par serveur

### Gestion des incidents
- Déclaration d’incidents
- Suivi du cycle de vie (ouvert, résolu)
- Association aux serveurs concernés

### Journalisation
- Traçabilité des actions critiques
- Logs exploitables pour audit et supervision

---

## Architecture

L’architecture de SecureStack suit une approche **API-first**, avec une séparation claire des responsabilités et une projection vers un environnement de production.

```text
┌────────────────────────────┐
│           Client           │
│  Postman / futur frontend  │
└───────────────┬────────────┘
                │ HTTPS / JSON
                ▼
┌────────────────────────────┐
│        API REST            │
│  Django REST Framework     │
│                            │
│  - Authentification JWT    │
│  - Permissions / rôles     │
│  - Logique métier          │
│  - Journalisation (audit)  │
└───────────────┬────────────┘
                │ ORM Django
                ▼
┌────────────────────────────┐
│       Base de données      │
│                            │
│  SQLite (développement)    │
│  PostgreSQL (production)   │
└────────────────────────────┘
```

Cette architecture permet :

- une évolution vers un déploiement cloud
- l’ajout d’un reverse proxy (Nginx)
- l’intégration future de mécanismes de supervision

---

## Technologies

### Backend
- Python
- Django
- Django REST Framework
- JWT (authentification)

### Base de données
- SQLite (environnement de développement)
- PostgreSQL (prévu en production)

### Sécurité
- Authentification JWT
- Permissions via Django REST Framework
- Journalisation des actions
- Bonnes pratiques de configuration Django

### Infrastructure
- Docker
- Docker Compose
- Déploiement cloud prévu (GCP / Render)

---

## Structure du projet

```bash
securestack/
├── api/
│   ├── models.py          # Server, BackupTask, Incident
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   └── tests/
├── users/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── config/
│   ├── settings.py
│   └── urls.py
├── docker/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Installation

### Prérequis
- Python 3.x
- Docker et Docker Compose (optionnel)

### Lancement en local

```bash
git clone https://github.com/username/securestack.git
cd securestack
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Lancement avec Docker

```bash
docker-compose up --build
```
---

### Exemples d’endpoints

```bash
POST    /api/auth/login        # Authentification
GET     /api/servers           # Liste des serveurs
POST    /api/servers           # Création d’un serveur
GET     /api/backups           # Liste des sauvegardes
POST    /api/incidents         # Déclaration d’un incident
```

## Exemple d’utilisation de l’API

### Authentification

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
        "username": "user@example.com",
        "password": "password123"
      }'
```

Réponse (extrait) :

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Accès à une ressource protégée : 


```bash
curl -X GET http://localhost:8000/api/servers \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Cet exemple illustre l’utilisation d’un token JWT pour accéder à un endpoint protégé de l’API.

## Axes d’amélioration

- Migration complète vers PostgreSQL
- Mise en place du rate limiting
- Centralisation et exploitation des logs
- Ajout de tests automatisés étendus
- Déploiement cloud complet
- Interface front-end légère (dashboard)

## Auteur

Oumaima El Khadraoui
