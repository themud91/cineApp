using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace TicketAPI.Filters
{
    public class ApiKeyAuthFilter(IConfiguration configuration, ILogger<ApiKeyAuthFilter> logger) : IActionFilter
    {
        private const string HeaderName = "X-Api-Key";

        public void OnActionExecuting(ActionExecutingContext context)
        {
            // API_SHARED_KEY (Render) ou ApiSharedKey (appsettings)
            var expectedKey = configuration["API_SHARED_KEY"] ?? configuration["ApiSharedKey"];

            if (string.IsNullOrEmpty(expectedKey))
            {
                // log sinon on sait pas pourquoi ca echoue
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
