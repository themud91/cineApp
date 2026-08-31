# Etape 1 : compilation avec le SDK complet.
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Le .csproj est copie seul en premier : tant qu'il ne change pas, Docker
# reutilise le cache de restore au lieu de retelecharger les paquets.
COPY ["TicketAPI.csproj", "./"]
RUN dotnet restore "TicketAPI.csproj"

COPY . .
RUN dotnet publish "TicketAPI.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Etape 2 : execution sur une image sans SDK (~220 Mo au lieu de ~800 Mo).
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .

# Base de donnees plate des billets, lue depuis ContentRootPath.
COPY data.json ./data.json

ENV ASPNETCORE_ENVIRONMENT=Production

# Le conteneur atteint la limite d'instances inotify de l'hote et CreateBuilder
# echoue en montant le surveillant de appsettings.json. Le sondage periodique
# n'en consomme aucune.
ENV DOTNET_USE_POLLING_FILE_WATCHER=true

# Render--> variable PORT.
ENTRYPOINT ["sh", "-c", "dotnet TicketAPI.dll --urls http://+:${PORT:-8080}"]
