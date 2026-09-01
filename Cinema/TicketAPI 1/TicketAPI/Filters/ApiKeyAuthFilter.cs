using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace TicketAPI.Filters
{
    public class ApiKeyAuthFilter(IConfiguration configuration) : IActionFilter
    {
        private const string HeaderName = "X-Api-Key";

        public void OnActionExecuting(ActionExecutingContext context)
        {
            var expectedKey = configuration["ApiSharedKey"];
            if (string.IsNullOrEmpty(expectedKey))
            {
                context.Result = new StatusCodeResult(StatusCodes.Status500InternalServerError);
                return;
            }

            if (!context.HttpContext.Request.Headers.TryGetValue(HeaderName, out var providedKey) ||
                providedKey != expectedKey)
            {
                context.Result = new UnauthorizedResult();
            }
        }

        public void OnActionExecuted(ActionExecutedContext context) { }
    }
}
