using System.Net.Http.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Options;
using TicketAPI.Models;

namespace TicketAPI.Services {

    // Envoie via l'API HTTP de Brevo (port 443). Render bloque le port SMTP
    // sortant (587) sur le plan gratuit, confirme en production : voir
    // CineApp-TODO.md, section "Envoi de correo".
    public sealed class EmailService(HttpClient httpClient, IOptions<BrevoOptions> options) : IEmailService {
        private readonly BrevoOptions _options = options.Value;

        public async Task SendAsync(
            string to,
            string subject,
            string htmlBody,
            CancellationToken cancellationToken = default) {

            // Sans cle configuree on n'essaie meme pas d'appeler Brevo : un
            // courriel qui echoue ne doit pas annuler l'achat (voir TicketsController).
            if (string.IsNullOrWhiteSpace(_options.ApiKey)) {
                return;
            }

            var payload = new BrevoEmailRequest {
                Sender = new BrevoContact { Name = _options.FromName, Email = _options.FromEmail },
                To = [new BrevoContact { Email = to }],
                Subject = subject,
                HtmlContent = htmlBody
            };

            using var request = new HttpRequestMessage(HttpMethod.Post, "v3/smtp/email") {
                Content = JsonContent.Create(payload)
            };
            request.Headers.Add("api-key", _options.ApiKey);

            using var response = await httpClient.SendAsync(request, cancellationToken);
            response.EnsureSuccessStatusCode();
        }
    }

    file sealed class BrevoEmailRequest {
        [JsonPropertyName("sender")] public required BrevoContact Sender { get; init; }
        [JsonPropertyName("to")] public required List<BrevoContact> To { get; init; }
        [JsonPropertyName("subject")] public required string Subject { get; init; }
        [JsonPropertyName("htmlContent")] public required string HtmlContent { get; init; }
    }

    file sealed class BrevoContact {
        [JsonPropertyName("email")] public required string Email { get; init; }
        [JsonPropertyName("name")] public string? Name { get; init; }
    }
}
