using System.Net;
using System.Text.Json;

namespace TicketAPI.Middlewares {

    // attrape les exceptions non gerees et repond en JSON
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
                    // client deconnecte, pas une erreur
                    throw;
                }

                logger.LogCritical(ex, "Exception non geree sur {Method} {Path}",
                    context.Request.Method, context.Request.Path);

                // reponse deja commencee, on peut plus ecrire
                if (context.Response.HasStarted) {
                    throw;
                }

                context.Response.Clear();
                context.Response.ContentType = "application/json";
                context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;

                // stack trace seulement en dev
                AppException response = env.IsDevelopment()
                    ? new(context.Response.StatusCode, ex.Message, ex.ToString())
                    : new(context.Response.StatusCode, "Internal Server Error");

                JsonSerializerOptions options = new() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };

                await context.Response.WriteAsync(JsonSerializer.Serialize(response, options));
            }
        }
    }
}
