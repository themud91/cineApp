# Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# copier le .csproj d'abord pour le cache Docker
COPY ["TicketAPI.csproj", "./"]
RUN dotnet restore "TicketAPI.csproj"

COPY . .
RUN dotnet publish "TicketAPI.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Runtime (image sans SDK, plus legere)
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .

# fichier JSON des billets
COPY data.json ./data.json

ENV ASPNETCORE_ENVIRONMENT=Production

# polling au lieu d'inotify (limite sur Render)
ENV DOTNET_USE_POLLING_FILE_WATCHER=true

# Render--> variable PORT.
ENTRYPOINT ["sh", "-c", "dotnet TicketAPI.dll --urls http://+:${PORT:-8080}"]
