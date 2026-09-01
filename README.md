# CineApp

Application web de billetterie de cinéma : catalogue de films, réservation de billets et historique d'achats.

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

Lien en direct : https://cineapp-cmad.onrender.com

Le service est hébergé sur un plan gratuit : il se met en veille après 15 minutes
d'inactivité, donc le premier chargement peut prendre une minute.

### Accès

Aucun compte de démonstration n'est fourni. Créez le vôtre depuis la page
d'inscription du site : l'accès est immédiat et donne droit à toutes les
fonctionnalités utilisateur.

## Installation locale

### Site Django

```
cd Cinema/CineApp
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata seed.json
python manage.py runserver
```

### API .NET

```
cd "Cinema/TicketAPI 1/TicketAPI"
dotnet run
```

## Auteur

Guillermo Perez
