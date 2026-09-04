# https://docs.djangoproject.com/fr/4.1/ref/class-based-views/
# https://docs.djangoproject.com/fr/4.1/ref/class-based-views/generic-display/#listview
# https://docs.djangoproject.com/fr/4.1/ref/class-based-views/generic-display/#detailview
# https://docs.djangoproject.com/fr/4.1/ref/class-based-views/generic-editing/#createview
# https://docs.djangoproject.com/fr/4.1/ref/class-based-views/generic-editing/#updateview
# https://docs.djangoproject.com/fr/4.1/ref/class-based-views/generic-editing/#deleteview
# dispatch(): https://docs.djangoproject.com/fr/4.1/ref/class-based-views/base/#django.views.generic.base.View.dispatch
# get_context_data: https://docs.djangoproject.com/fr/4.1/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin.get_context_data
# form_valid: https://docs.djangoproject.com/fr/4.1/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid
# SuccessMessageMixin: https://docs.djangoproject.com/fr/4.1/ref/contrib/messages/#django.contrib.messages.views.SuccessMessageMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
import datetime
import platform

import django

from .models import Salle, Technologie, Films, Representation, Billet
from .forms import (
    SalleForm,
    TechnologieForm,
    FilmsForm,
    RepresentationForm,
    BilletForm,
    RegisterForm,
)

# Auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Message de confirmation apres chaque operation
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Client de l'API C#
from .api_client import *

# Prix unitaire d'un billet, en dollars
PRIX_BILLET = 12.0


# Accueil
def accueilView(request):
    representations = Representation.objects.filter(
        dateHeure__date=datetime.date.today()
    ).order_by("dateHeure")
    context = {"today": datetime.date.today(), "representations": representations}
    return render(request, "accueil.html", context)


# Mixin, Creation du class StaffRequiredMixin: seul un admin (is_staff) peut acceder
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("login")
        return redirect("accueil")


# Salles seule pour Admin (StaffRequiredMixin)
class SalleListView(StaffRequiredMixin, ListView):
    model = Salle
    template_name = "salles/salle_list.html"
    context_object_name = "salles"


class SalleDetailView(StaffRequiredMixin, DetailView):
    model = Salle
    template_name = "salles/salle_detail.html"
    context_object_name = "salle"


class SalleCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Salle
    form_class = SalleForm
    template_name = "salles/salle_form.html"
    success_url = "/salles/"
    success_message = "Salle créée avec succès!"


class SalleUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Salle
    form_class = SalleForm
    template_name = "salles/salle_form.html"
    success_url = "/salles/"
    success_message = "Salle modifiée avec succès!"


class SalleDeleteView(StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Salle
    template_name = "salles/salle_delete.html"
    success_url = "/salles/"
    success_message = "Salle supprimée avec succès!"


# Technologies seule pour Admin (StaffRequiredMixin)
class TechnologieListView(StaffRequiredMixin, ListView):
    model = Technologie
    template_name = "technologies/technologie_list.html"
    context_object_name = "technologies"


class TechnologieCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Technologie
    form_class = TechnologieForm
    template_name = "technologies/technologie_form.html"
    success_url = "/technologies/"
    success_message = "Technologie créée avec succès!"


class TechnologieUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Technologie
    form_class = TechnologieForm
    template_name = "technologies/technologie_form.html"
    success_url = "/technologies/"
    success_message = "Technologie modifiée avec succès!"


class TechnologieDeleteView(StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Technologie
    template_name = "technologies/technologie_delete.html"
    success_url = "/technologies/"
    success_message = "Technologie supprimée avec succès!"


# Films  seule pour Admin (StaffRequiredMixin)
class FilmListView(StaffRequiredMixin, ListView):
    model = Films
    template_name = "films/film_list.html"
    context_object_name = "films"


class FilmDetailView(StaffRequiredMixin, DetailView):
    model = Films
    template_name = "films/film_detail.html"
    context_object_name = "film"


class FilmCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Films
    form_class = FilmsForm
    template_name = "films/film_form.html"
    success_url = "/films/"
    success_message = "Film créé avec succès!"


class FilmUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Films
    form_class = FilmsForm
    template_name = "films/film_form.html"
    success_url = "/films/"
    success_message = "Film modifié avec succès!"


class FilmDeleteView(StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Films
    template_name = "films/film_delete.html"
    success_url = "/films/"
    success_message = "Film supprimé avec succès!"


# Representations : reserve aux admins, avec message de confirmation
class RepresentationListView(StaffRequiredMixin, ListView):
    model = Representation
    template_name = "representations/representation_list.html"
    context_object_name = "representations"


class RepresentationDetailView(StaffRequiredMixin, DetailView):
    model = Representation
    template_name = "representations/representation_detail.html"
    context_object_name = "representation"


class RepresentationCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Representation
    form_class = RepresentationForm
    template_name = "representations/representation_form.html"
    success_url = "/representations/"
    success_message = "Représentation créée avec succès!"


class RepresentationUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Representation
    form_class = RepresentationForm
    template_name = "representations/representation_form.html"
    success_url = "/representations/"
    success_message = "Représentation modifiée avec succès!"


class RepresentationDeleteView(StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Representation
    template_name = "representations/representation_delete.html"
    success_url = "/representations/"
    success_message = "Représentation supprimée avec succès!"


# Representations d'un film pour l'utilisateur
def film_representations(request, id):
    film = get_object_or_404(Films, id=id)
    representations = Representation.objects.filter(idFilm=film).order_by("dateHeure")
    return render(
        request,
        "films/film_representations.html",
        {"film": film, "representations": representations},
    )


# Login Required pour voir (LoginRequiredMixin)
# Vue page de choix d'un film pour acheter un billet avec login
class BilletsView(LoginRequiredMixin, ListView):
    model = Films
    template_name = "billets/billets.html"
    context_object_name = "films"


# Vue representations d'un film pour l'utilisateur avec login
class FilmRepresentationsView(LoginRequiredMixin, DetailView):
    model = Films
    template_name = "films/film_representations.html"
    context_object_name = "film"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["representations"] = Representation.objects.filter(
            idFilm=self.object
        ).order_by("dateHeure")
        return context


# Achat d'un billet pour une representation specifique avec(LoginRequiredMixin)
class BilletCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Billet
    form_class = BilletForm
    template_name = "billets/billet_form.html"
    success_url = "/"
    success_message = "Billet acheté avec succès!"

    # dispatch: pour calculer le nombre de places restantes, et rediriger vers l'accueil.
    def dispatch(self, request, *args, **kwargs):
        from django.db.models import Sum

        # Recuperer la representation depuis l'URL
        self.representation = get_object_or_404(Representation, id=self.kwargs["id"])
        # Calculer les places restantes
        billets_vendus = (
            Billet.objects.filter(idRepresentation=self.representation).aggregate(
                total=Sum("quantite")
            )["total"]
            or 0
        )
        self.places_restantes = self.representation.idSalle.capacite - billets_vendus
        # S'il n'y a plus de places, rediriger
        if self.places_restantes <= 0:
            messages.error(
                request, "Désolé, il ne reste plus de places pour cette représentation."
            )
            return redirect("accueil")
        return super().dispatch(request, *args, **kwargs)

    # on passe par context la representation et les places restantes pour que le HTML les affiche
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["representation"] = self.representation
        context["places_restantes"] = self.places_restantes
        return context

    # form_valid verifie la capacite restante et lie le billet a la representation avant le save
    def form_valid(self, form):
        from django.db import transaction
        from django.db.models import Sum

        quantite = form.cleaned_data["quantite"]

        # Un utilisateur ne peut pas acheter deux fois la meme representation
        if Billet.objects.filter(
            user=self.request.user, idRepresentation=self.representation
        ).exists():
            messages.error(
                self.request,
                "Vous avez déjà acheté un billet pour cette représentation.",
            )
            return self.form_invalid(form)

        # La confirmation part vers l'adresse du compte, jamais vers une adresse du POST.
        email = (self.request.user.email or "").strip()
        if not email:
            messages.error(
                self.request,
                "Votre compte n'a pas d'adresse courriel. Ajoutez-en une à votre "
                "compte pour recevoir la confirmation d'achat.",
            )
            return self.form_invalid(form)

        # select_for_update() verrouille la representation : deux achats concurrents ne passent pas le controle en meme temps.
        with transaction.atomic():
            rep = Representation.objects.select_for_update().get(
                id=self.representation.id
            )
            billets_vendus = (
                Billet.objects.filter(idRepresentation=rep).aggregate(
                    total=Sum("quantite")
                )["total"]
                or 0
            )
            places_restantes = rep.idSalle.capacite - billets_vendus
            if quantite > places_restantes:
                messages.error(
                    self.request, f"Seulement {places_restantes} place(s) disponibles."
                )
                return self.form_invalid(form)

            # Appel de l'API C# pour creer le billet
            try:
                create_ticket(
                    id_film=rep.idFilm.id,
                    id_representation=rep.id,
                    id_salle=rep.idSalle.id,
                    id_utilisateur=self.request.user.id,
                    prix=PRIX_BILLET * quantite,
                    nombre_billets=quantite,
                    email=email,
                    titre_film=rep.idFilm.titre,
                    nom_salle=rep.idSalle.noSalle,
                    date_heure=str(rep.dateHeure),
                )

            except Exception:
                messages.error(
                    self.request,
                    "Impossible de contacter le service de billetterie. Veuillez réessayer.",
                )
                return self.form_invalid(form)

            # enregistrer chez Django. Le message de succes vient apres le save :
            # annoncer l'achat avant de l'enregistrer laisserait l'utilisateur avec
            # une confirmation pour un billet qui n'existe pas.
            billet = form.save(commit=False)
            billet.idRepresentation = self.representation
            billet.user = self.request.user
            billet.save()

        messages.success(
            self.request,
            "Billet acheté avec succès ! Un courriel de confirmation vous a été envoyé.",
        )
        return redirect(self.success_url)


# liste des billets vendus  seule pour Admin (StaffRequiredMixin)
class BilletListView(StaffRequiredMixin, ListView):
    model = Representation
    template_name = "billets/billet_list.html"
    context_object_name = "data"

    def get_queryset(self):
        from django.db.models import Sum

        representations = Representation.objects.all()
        data = []
        for rep in representations:
            total = (
                Billet.objects.filter(idRepresentation=rep).aggregate(
                    total=Sum("quantite")
                )["total"]
                or 0
            )
            data.append(
                {
                    "representation": rep,
                    "billets_vendus": total,
                    "places_restantes": rep.idSalle.capacite - total,
                }
            )
        return data


# Inscription d'un nouvel utilisateur
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Bonjour {username}, vous êtes enregistré !")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form": form})


# Vu historique billets
class HistoriqueView(LoginRequiredMixin, ListView):
    model = Billet
    template_name = "billets/historique.html"
    context_object_name = "billets"

    def get_queryset(self):
        return Billet.objects.filter(user=self.request.user).order_by("-dateAchat")


# Page « A Propos »
def apropos_View(request):
    context = {
        "today": datetime.date.today(),
        # Lues a l'execution: elles restent exactes en local comme en production.
        "python_version": platform.python_version(),
        "django_version": django.get_version(),
        "concepteurs": [
            {"nom": "Guillermo Perez"},
        ],
        "description_projet": [
            {
                "titre": "Vues créées avec les Class Based Views (CBV)",
                "description": "Les vues sont maintenant des CBV (ListView, DetailView, CreateView, UpdateView, DeleteView).",
            },
            {
                "titre": "Authentification et gestion des accès",
                "description": "Connexion, déconnexion et inscription, avec accès restreint selon le rôle (admin/utilisateur).",
            },
            {
                "titre": "Historique des achats",
                "description": "Affiche la liste des billets déjà achetés par l'utilisateur connecté.",
            },
            {
                "titre": "Blocage du double achat",
                "description": "Un utilisateur ne peut effectuer qu'un seul achat par représentation. Cet achat peut porter sur plusieurs billets, dans la limite des places restantes.",
            },
            {
                "titre": "API ASP.NET Core – Billetterie",
                "description": "API C# qui gère la création et la consultation des billets.",
            },
            {
                "titre": "Envoi de courriel de confirmation",
                "description": "Envoie un courriel de confirmation après chaque achat de billet.",
            },
        ],
    }
    return render(request, "apropos.html", context)
