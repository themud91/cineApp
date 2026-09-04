# documentation:
# https://docs.djangoproject.com/en/6.0/ref/forms/validation/
# https://docs.djangoproject.com/en/5.0/ref/forms/fields/#modelmultiplechoicefield
# https://docs.djangoproject.com/en/5.0/ref/forms/widgets/#checkboxselectmultiple

from django import forms
from .models import Salle, Technologie, Films, Representation, Billet

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Formulaire des Salles
class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ["noSalle", "capacite", "technologies"]
        widgets = {
            # montrer comme checkbox
            "technologies": forms.CheckboxSelectMultiple
        }

    # methode validation capacite
    def clean_capacite(self):
        # get la capacite..
        capacite = self.cleaned_data.get("capacite")
        # error si la capacite insere n'est pas correcte, double validation (dans views, et forms)
        if capacite < 1 or capacite > 250:
            raise forms.ValidationError("La capacité doit être entre 1 et 250.")
        return capacite


# Formulaire du Tech
class TechnologieForm(forms.ModelForm):
    class Meta:
        model = Technologie
        fields = ["nomTechno"]

    # methode pour valider nom obligatoire
    def clean_nomTechno(self):
        nomTechno = self.cleaned_data.get("nomTechno")
        # s'il n'a pas du nom, on montre le message d'erreur
        if not nomTechno:
            raise forms.ValidationError("Le nom de la technologie est obligatoire.")
        return nomTechno


# Formulaire du Films
class FilmsForm(forms.ModelForm):
    class Meta:
        model = Films
        fields = ["titre", "duree", "description", "categorie", "img", "technologies"]
        widgets = {
            # montrer tech comme Checkbox (un film peut avoir plusieurs technologies)
            "technologies": forms.CheckboxSelectMultiple
        }

    # Methode pour valider duration du film
    def clean_duree(self):
        duree = self.cleaned_data.get("duree")
        # si film = 0 minutes, montrer message erreur
        if duree < 1:
            raise forms.ValidationError("La duree doit etre supérieure à 0.")
        if duree > 300:
            raise forms.ValidationError("La durée doit être inférieure à 300 minutes.")
        return duree


# Formulaire Representations
class RepresentationForm(forms.ModelForm):
    class Meta:
        model = Representation
        fields = ["idSalle", "idFilm", "dateHeure", "technologie"]
        help_texts = {"dateHeure": "Format : YYYY-MM-DD HH:MM"}

    # validations (techno compatible + horaires + 30 min entre representations)
    def clean(self):
        cleaned = super().clean()
        salle = cleaned.get("idSalle")
        film = cleaned.get("idFilm")
        dateHeure = cleaned.get("dateHeure")
        technologie = cleaned.get("technologie")

        if not (salle and film and dateHeure and technologie):
            return cleaned

        if technologie.id not in salle.technologies.values_list("id", flat=True):
            raise forms.ValidationError(
                "Cette technologie n'est pas disponible dans cette salle."
            )

        if technologie.id not in film.technologies.values_list("id", flat=True):
            raise forms.ValidationError(
                "Ce film n'est pas disponible en cette technologie."
            )

        heure = dateHeure.hour
        if film.categorie == "enfants" and not (8 <= heure < 14):
            raise forms.ValidationError(
                "Les films pour enfants doivent etre projetes entre 8h et 14h."
            )
        if film.categorie in ["adultes", "horreur"] and not (18 <= heure < 24):
            raise forms.ValidationError(
                "Les films pour adultes doivent etre projetes apres 18h."
            )

        from datetime import timedelta
        from .models import Representation

        fin = dateHeure + timedelta(minutes=film.duree + 30)
        debut = dateHeure - timedelta(minutes=film.duree + 30)
        conflits = Representation.objects.filter(
            idSalle=salle, dateHeure__lt=fin, dateHeure__gt=debut
        )
        if self.instance and self.instance.pk:
            conflits = conflits.exclude(pk=self.instance.pk)
        if conflits.exists():
            raise forms.ValidationError(
                "Il doit y avoir au moins 30 minutes entre les representations."
            )

        return cleaned


# Formulaire Billet
class BilletForm(forms.ModelForm):
    class Meta:
        model = Billet
        fields = ["quantite"]

    # quantite doit etre toujours superior a 0
    def clean_quantite(self):
        quantite = self.cleaned_data.get("quantite")
        if quantite < 1:
            raise forms.ValidationError("La quantité doit être supérieure à 0.")
        return quantite


# Formulaire d'inscription
class RegisterForm(UserCreationForm):
    # Obligatoire : c'est la seule adresse vers laquelle part la confirmation
    # d'achat. Le modele User la laisse facultative par defaut.
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
