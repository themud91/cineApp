# documentation:
# https://docs.djangoproject.com/en/5.0/ref/models/fields/
# https://docs.djangoproject.com/en/5.0/ref/validators/

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Technologie
class Technologie(models.Model):
    nomTechno = models.CharField(max_length=50)

    def __str__(self):
        return self.nomTechno


# Modele Salle
class Salle(models.Model):
    noSalle = models.CharField(max_length=50)

    # capacite entre 1 et 250
    capacite = models.PositiveIntegerField(
        default=250, validators=[MinValueValidator(1), MaxValueValidator(250)]
    )
    # une salle peut avoir plusieurs technologies
    technologies = models.ManyToManyField(Technologie)

    def __str__(self):
        return self.noSalle


# Modele Films
class Films(models.Model):
    Categories = [
        ("enfants", "Enfants"),
        ("famille", "Famille"),
        ("sci-fi", "sci-fi"),
        ("action", "Action"),
        ("horreur", "Horreur"),
        ("comedie", "Comédie"),
        ("adultes", "Adultes"),
    ]
    titre = models.CharField(max_length=50)
    duree = models.PositiveIntegerField(default=120, help_text="Durée en minutes")
    description = models.TextField()
    categorie = models.CharField(max_length=50, choices=Categories)
    # img est optionnel, peut etre vide
    img = models.URLField(max_length=200, blank=True)

    technologies = models.ManyToManyField(Technologie)

    def __str__(self):
        return self.titre


# Representation
class Representation(models.Model):
    # si je supprime une salle ou une film, ses representations vont se aussi se supprimer
    idSalle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    idFilm = models.ForeignKey(Films, on_delete=models.CASCADE)
    dateHeure = models.DateTimeField()
    technologie = models.ForeignKey(
        Technologie, on_delete=models.PROTECT, null=True
    )  # S'on delete une tech --> djang throws error... si je mettre null not true Django me throw erreur de migration

    def __str__(self):
        return f"{self.idFilm} - {self.idSalle} ({self.dateHeure})"


# Billet
class Billet(models.Model):
    # si je supprime une representation, ses billets vont se aussi se supprimer
    idRepresentation = models.ForeignKey(Representation, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    dateAchat = models.DateTimeField(auto_now_add=True)

    # FK pour User. Permet repondre aux besoin d'user.
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True  # null=True
    )

    def __str__(self):
        return f"Billet {self.id} - {self.idRepresentation}"
