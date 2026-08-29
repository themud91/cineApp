# https://docs.djangoproject.com/en/6.0/topics/class-based-views/

from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    # Accueil
    path("", views.accueilView, name="accueil"),
    path("apropos/", views.apropos_View, name="apropos"),
    # Salles
    path("salles/", views.SalleListView.as_view(), name="salle_list"),
    path("salles/add/", views.SalleCreateView.as_view(), name="salle_create"),
    path("salles/<int:pk>/", views.SalleDetailView.as_view(), name="salle_detail"),
    path("salles/<int:pk>/edit/", views.SalleUpdateView.as_view(), name="salle_edit"),
    path(
        "salles/<int:pk>/delete/", views.SalleDeleteView.as_view(), name="salle_delete"
    ),
    # Technologies
    path("technologies/", views.TechnologieListView.as_view(), name="technologie_list"),
    path(
        "technologies/add/",
        views.TechnologieCreateView.as_view(),
        name="technologie_create",
    ),
    path(
        "technologies/<int:pk>/edit/",
        views.TechnologieUpdateView.as_view(),
        name="technologie_edit",
    ),
    path(
        "technologies/<int:pk>/delete/",
        views.TechnologieDeleteView.as_view(),
        name="technologie_delete",
    ),
    # Films (CBV)
    path("films/", views.FilmListView.as_view(), name="film_list"),
    path("films/add/", views.FilmCreateView.as_view(), name="film_create"),
    path("films/<int:pk>/", views.FilmDetailView.as_view(), name="film_detail"),
    path("films/<int:pk>/edit/", views.FilmUpdateView.as_view(), name="film_edit"),
    path("films/<int:pk>/delete/", views.FilmDeleteView.as_view(), name="film_delete"),
    # Representations (CBV)
    path(
        "representations/",
        views.RepresentationListView.as_view(),
        name="representation_list",
    ),
    path(
        "representations/add/",
        views.RepresentationCreateView.as_view(),
        name="representation_create",
    ),
    path(
        "representations/<int:pk>/",
        views.RepresentationDetailView.as_view(),
        name="representation_detail",
    ),
    path(
        "representations/<int:pk>/edit/",
        views.RepresentationUpdateView.as_view(),
        name="representation_edit",
    ),
    path(
        "representations/<int:pk>/delete/",
        views.RepresentationDeleteView.as_view(),
        name="representation_delete",
    ),
    # Billets (CBV)
    path("billets/", views.BilletsView.as_view(), name="billets"),
    path(
        "billets/film/<int:pk>/",
        views.FilmRepresentationsView.as_view(),
        name="film_representations",
    ),
    # 'id' (pas 'pk') car BilletCreateView.dispatch() lit self.kwargs['id'] manuellement, sans passer par pk_url_kwarg. pas besoin.
    path(
        "billets/<int:id>/add/", views.BilletCreateView.as_view(), name="billet_create"
    ),
    path("gestion/billets/", views.BilletListView.as_view(), name="billet_list"),
    path("historique/", views.HistoriqueView.as_view(), name="historique"),
    # Authentification
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="auth/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
]
