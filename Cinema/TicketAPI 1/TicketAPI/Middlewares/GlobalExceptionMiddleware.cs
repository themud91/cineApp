using System.Net;
using System.Text.Json;

namespace TicketAPI.Middlewares {
    internal sealed class GlobalExceptionMiddleware(
      RequestDelegate next,
      ILogger<GlobalExceptionMiddleware> logger,
      IHostEnvironment env
  ) {
        public async Task InvokeAsync(HttpContext context) {
            try {
                logger.Log(LogLevel.Information, "=====================================================Begin Transaction=====================================================");
                await next(context);
                logger.Log(LogLevel.Information, "=====================================================End Transaction=====================================================");
            } catch (Exception ex) {
                if (ex is not OperationCanceledException) {
                    logger.Log(LogLevel.Critical, "=====================================================ERROR/EXCEPTION HAPPENED=====================================================");
                    logger.LogError(ex, message: ex.Message);
                }

                context.Response.ContentType = "application/json";
                context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;

                AppException response = env.IsDevelopment()
                    ? new(context.Response.StatusCode, ex.Message, ex.ToString())
                    : new(context.Response.StatusCode, "Internal Server Error");

                JsonSerializerOptions options = new() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };

                var json = JsonSerializer.Serialize(response, options);

                await context.Response.WriteAsync(json);
            }
        }
    }
}
