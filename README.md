# CineApp

Application web de billetterie de cinéma : catalogue de films, réservation de billets et historique d'achats.

## Démonstration

**En direct : https://cineapp-cmad.onrender.com**

Hébergé sur un plan gratuit (Render) :
- Le premier chargement peut prendre jusqu'à une minute (le service se met en veille après 15 minutes d'inactivité).
- Les données sont éphémères : le catalogue est rechargé à chaque build depuis un fixture, et tout ce qu'un visiteur crée (compte, billets) disparaît au redémarrage suivant. C'est une démonstration, pas une application avec persistance réelle.

Aucun compte de démonstration n'est fourni : l'inscription est libre et immédiate.

## Architecture

Deux services indépendants, déployés séparément sur Render, qui communiquent par API REST :

```
Visiteur
   |
   v
CineApp (Django)  --- HTTP + cle API partagee --->  TicketAPI (ASP.NET Core 8, Docker)
   |                                                        |
   v                                                        v
Catalogue, comptes,                              Creation/consultation des
sessions                                          billets, courriel (Brevo)
```

- **CineApp (Django)** sert le site, gère les comptes et le catalogue, et délègue tout ce qui touche aux billets à l'API .NET.
- **TicketAPI (.NET 8)** est indépendante : aucune dépendance sur Django, routes protégées par une clé API partagée, envoi elle-même du courriel de confirmation via l'API HTTP de Brevo (SMTP est bloqué sur le plan gratuit de Render).
- Les deux services peuvent se mettre en veille indépendamment : un visiteur qui achète après une période d'inactivité réveille d'abord Django, puis l'API, en série.

## Stack technique

- **Backend** — Python / Django 6.0, C# / ASP.NET Core 8
- **Frontend** — Bootstrap, CSS personnalisé
- **Déploiement** — Render (Docker pour l'API, WhiteNoise pour les statiques Django)
- **Courriel transactionnel** — API HTTP de Brevo
- **Base de données** — SQLite en local ; en production, rechargée à chaque build depuis un fixture (voir Démonstration)

## Fonctionnalités

- Vues en Class Based Views (ListView, DetailView, CreateView, UpdateView, DeleteView)
- Authentification et gestion des accès (connexion, déconnexion, inscription, rôles admin/utilisateur)
- Historique des billets achetés par utilisateur
- Blocage du double achat pour une même représentation
- Envoi automatique d'un courriel de confirmation après achat, via l'API .NET
- Communication entre Django et l'API .NET par HTTP, authentifiée par clé partagée

## Décisions de production

- **Authentification entre services.** L'API .NET rejette toute requête sur `/api/tickets` sans l'en-tête `X-Api-Key` correcte.
- **Échec explicite en production.** `SECRET_KEY` et `DEBUG` doivent être définies explicitement sur Render ; en leur absence, le démarrage plante au lieu de se rabattre silencieusement sur une valeur de développement.
- **Contenu du courriel échappé**, pour éviter l'injection HTML depuis les champs saisis par l'utilisateur.
- **Relais de courriel fermé.** Le destinataire de la confirmation vient toujours du compte connecté, jamais d'un champ de formulaire.
- **Courriel découplé de l'achat.** Un échec d'envoi n'annule pas un billet déjà enregistré.

## Variables d'environnement

Les deux services doivent partager la même valeur de `API_SHARED_KEY` : sans elle, l'API rejette tout achat de billet.

| Service | Variable | Rôle |
|---|---|---|
| Django | `API_SHARED_KEY` | Clé envoyée dans l'en-tête `X-Api-Key` à chaque appel |
| Django | `TICKET_API_URL` | URL de l'API .NET (défaut : `http://localhost:5056/api/tickets`) |
| Django | `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` | Obligatoires en production |
| API .NET | `API_SHARED_KEY` | Clé attendue, comparée à celle reçue |
| API .NET | `Brevo__ApiKey`, `Brevo__FromEmail` | Envoi du courriel de confirmation |

En .NET, le double trait de soulignement marque l'imbrication : `Brevo__ApiKey` correspond à la section `Brevo`, clé `ApiKey`.

## Installation locale

### API .NET

    cd "Cinema/TicketAPI 1/TicketAPI"
    set API_SHARED_KEY=une-valeur-au-choix
    dotnet run

### Site Django

Dans un second terminal, avec la même valeur de `API_SHARED_KEY` :

    cd Cinema/CineApp
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    set API_SHARED_KEY=une-valeur-au-choix
    python manage.py migrate
    python manage.py loaddata seed.json
    python manage.py runserver

Sans `Brevo__ApiKey`, l'achat fonctionne et le courriel de confirmation est simplement ignoré, avec un avertissement dans les journaux.

## Auteur

Guillermo Perez
