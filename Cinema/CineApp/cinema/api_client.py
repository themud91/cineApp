# Ce fichier contient des fonctions pour interagir avec l'API C# de gestion des billets.
import os

import requests

# URL de base de l'API C#. En local, utilise localhost par défaut.
# En production, définir la variable d'environnement TICKET_API_URL.
BASE_URL = os.environ.get("TICKET_API_URL", "http://localhost:5056/api/tickets")

# Clé partagée avec l'API : elle rejette toute requête qui ne la présente pas
# dans l'en-tête X-Api-Key. Voir API_SHARED_KEY côté TicketAPI.
API_KEY = os.environ.get("API_SHARED_KEY", "")
HEADERS = {"X-Api-Key": API_KEY}

# Délai maximal des appels à l'API. Sans lui, une API qui ne répond pas bloque
# le worker gunicorn jusqu'à ce qu'il soit tué, et Django renvoie une erreur 500.
TIMEOUT = 60


def get_tickets_by_representation(representation_id: int):
    response = requests.get(
        f"{BASE_URL}/representation/{representation_id}", headers=HEADERS, timeout=TIMEOUT
    )
    return response.json()


def get_tickets_by_user(user_id: int):
    response = requests.get(f"{BASE_URL}/user/{user_id}", headers=HEADERS, timeout=TIMEOUT)
    return response.json()


def create_ticket(
    id_film: int,
    id_representation: int,
    id_salle: int,
    id_utilisateur: int,
    prix: float,
    nombre_billets: int,
    email: str,
    titre_film: str = "",
    nom_salle: str = "",
    date_heure: str = "",
) -> bool:

    # afficher l'info de la representation dans l'email
    payload = {
        "idFilm": id_film,
        "idRepresentation": id_representation,
        "idSalle": id_salle,
        "idUtilisateur": id_utilisateur,
        "prix": prix,
        "nombreBillets": nombre_billets,
        "email": email,
        "titreFilm": titre_film,
        "nomSalle": nom_salle,
        "dateHeure": date_heure,
    }

    response = requests.post(BASE_URL, json=payload, headers=HEADERS, timeout=TIMEOUT)

    if response.status_code == 201:  # Created
        return True

    response.raise_for_status()  # Lève une exception pour tout autre code d'erreur
