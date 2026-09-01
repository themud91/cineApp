using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace TicketAPI.Filters
{
    public class ApiKeyAuthFilter(IConfiguration configuration, ILogger<ApiKeyAuthFilter> logger) : IActionFilter
    {
        private const string HeaderName = "X-Api-Key";

        public void OnActionExecuting(ActionExecutingContext context)
        {
            // Render expose la variable sous le nom API_SHARED_KEY, le meme que
            // lit api_client.py cote Django. Le trait de soulignement n'est PAS
            // un separateur de configuration en .NET (seul le double l'est), donc
            // configuration["ApiSharedKey"] ne la voyait jamais : la cle sortait
            // vide et toute requete repondait 500. On accepte les deux noms.
            var expectedKey = configuration["API_SHARED_KEY"] ?? configuration["ApiSharedKey"];

            if (string.IsNullOrEmpty(expectedKey))
            {
                // Sans ce log la panne est muette : aucune exception n'est levee,
                // et MVC transforme le StatusCodeResult en ProblemDetails
                // generique qui ne dit rien de la cause.
                logger.LogCritical(
                    "Cle partagee absente de la configuration. Definir API_SHARED_KEY sur le "
                    + "service pour que {Path} reponde.",
                    context.HttpContext.Request.Path);

                context.Result = new StatusCodeResult(StatusCodes.Status500InternalServerError);
                return;
            }

            if (!context.HttpContext.Request.Headers.TryGetValue(HeaderName, out var providedKey) ||
                !string.Equals(providedKey, expectedKey, StringComparison.Ordinal))
            {
                logger.LogWarning(
                    "Requete rejetee sur {Path} : en-tete {Header} absent ou invalide.",
                    context.HttpContext.Request.Path, HeaderName);

                context.Result = new UnauthorizedResult();
            }
        }

        public void OnActionExecuted(ActionExecutedContext context) { }
    }
}
