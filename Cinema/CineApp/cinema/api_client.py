# Ce fichier contient des fonctions pour interagir avec l'API C# de gestion des billets.
import requests

# URL de base de l'API C#
BASE_URL = "http://localhost:5056/api/tickets"


def get_tickets_by_representation(representation_id: int):
    response = requests.get(
        f"{BASE_URL}/representation/{representation_id}", verify=False
    )  # verify=False est un paramètre de la librairie requests qui désactive la validation du certificat SSL lors d’un appel HTTPS.
    return response.json()


def get_tickets_by_user(user_id: int):
    response = requests.get(f"{BASE_URL}/user/{user_id}", verify=False)
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

    response = requests.post(BASE_URL, json=payload, verify=False)

    if response.status_code == 201:  # Created
        return True

    response.raise_for_status()  # Lève une exception pour tout autre code d'erreur
