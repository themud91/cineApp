# CineApp

Réplique du site web d'un cinéma populaire du Québec, réalisée dans le cadre d'une activité académique.

## Architecture

Le projet est composé de deux services indépendants qui communiquent par API REST :

- **CineApp** (Django) — site web : catalogue de films, réservation de billets, authentification, historique d'achats.
- **TicketAPI** (ASP.NET Core 8) — API de billetterie : création et consultation des billets, envoi du courriel de confirmation.

## Stack technique

- Python / Django 6.0
- C# / ASP.NET Core 8
- Bootstrap
- SQLite (base de données locale)
- MailKit (envoi de courriels)

## Fonctionnalités

- Vues en Class Based Views (ListView, DetailView, CreateView, UpdateView, DeleteView)
- Authentification et gestion des accès (connexion, déconnexion, inscription, rôles admin/utilisateur)
- Historique des billets achetés par utilisateur
- Blocage du double achat pour une même représentation
- Envoi automatique d'un courriel de confirmation après achat
- Communication avec l'API .NET pour la gestion des billets

## Démonstration

Lien en direct : *(à venir — déploiement en cours)*

### Comptes de démonstration

| Utilisateur | Mot de passe |
|---|---|
| tp3 | 123456 |
| tp32 | MotDePasse42 |

Comptes utilisateurs standards, sans accès administrateur.

## Installation locale

### Site Django

```
cd Cinema/CineApp
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
```

### API .NET

```
cd "Cinema/TicketAPI 1/TicketAPI"
dotnet run
```

## Auteur

Guillermo Perez
