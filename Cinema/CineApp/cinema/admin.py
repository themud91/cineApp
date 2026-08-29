from django.contrib import admin
from .models import Salle, Technologie, Films, Representation, Billet

admin.site.register(Salle)
admin.site.register(Technologie)
admin.site.register(Films)
admin.site.register(Representation)
admin.site.register(Billet)
