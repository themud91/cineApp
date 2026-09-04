using System.Net;
using System.Text.Json;

namespace TicketAPI.Middlewares {

    // Dernier filet du pipeline : journalise toute exception non geree et repond en JSON.
    internal sealed class GlobalExceptionMiddleware(
      RequestDelegate next,
      ILogger<GlobalExceptionMiddleware> logger,
      IHostEnvironment env
  ) {
        public async Task InvokeAsync(HttpContext context) {
            try {
                await next(context);
            } catch (Exception ex) {
                if (ex is OperationCanceledException) {
                    // Le client a coupe la connexion : ce n'est pas une panne.
                    throw;
                }

                logger.LogCritical(ex, "Exception non geree sur {Method} {Path}",
                    context.Request.Method, context.Request.Path);

                // Si la reponse est deja partie sur le fil, y ecrire leverait une
                // seconde exception qui masquerait la premiere.
                if (context.Response.HasStarted) {
                    throw;
                }

                context.Response.Clear();
                context.Response.ContentType = "application/json";
                context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;

                // Le stack trace ne sort qu'en developpement : en production il
                // exposerait la structure interne de l'API.
                AppException response = env.IsDevelopment()
                    ? new(context.Response.StatusCode, ex.Message, ex.ToString())
                    : new(context.Response.StatusCode, "Internal Server Error");

                JsonSerializerOptions options = new() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };

                await context.Response.WriteAsync(JsonSerializer.Serialize(response, options));
            }
        }
    }
}
