# Fonctions pour appeler l'API C# des billets
import os

import requests

# URL de l'API (localhost par defaut, TICKET_API_URL en prod)
BASE_URL = os.environ.get("TICKET_API_URL", "http://localhost:5056/api/tickets")

# cle partagee avec l'API (header X-Api-Key)
API_KEY = os.environ.get("API_SHARED_KEY", "")
HEADERS = {"X-Api-Key": API_KEY}

# timeout pour ne pas bloquer gunicorn si l'API repond pas
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
