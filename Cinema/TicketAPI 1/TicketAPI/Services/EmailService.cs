using MailKit.Net.Smtp;
using MailKit.Security;
using Microsoft.Extensions.Options;
using MimeKit;
using TicketAPI.Models;

namespace TicketAPI.Services {

    //Voir appSetting.json pour la configuration de ce service
    public sealed class EmailService(IOptions<SmtpOptions> options) : IEmailService {
        private readonly SmtpOptions _options = options.Value;
        //Le corps du message doit être fait en html
        //ex: "<h1>Merci pour votre achat !</h1><p>Voici votre billet...</p>"
        public async Task SendAsync(
            string to,
            string subject,
            string htmlBody,
            CancellationToken cancellationToken = default) {

            var message = new MimeMessage();
            message.From.Add(new MailboxAddress(_options.FromName, _options.FromEmail));
            message.To.Add(MailboxAddress.Parse(to));
            message.Subject = subject;

            message.Body = new TextPart("html") {
                Text = htmlBody
            };

            // Sans mot de passe configure on n'essaie meme pas de se connecter :
            // une connexion vers un port bloque n'echoue pas, elle reste suspendue
            // et fait expirer la requete HTTP du cote de Django.
            if (string.IsNullOrWhiteSpace(_options.Password)) {
                return;
            }

            // Sans delai maximal, ConnectAsync peut attendre indefiniment.
            using var client = new SmtpClient { Timeout = 10000 };

            var secure = _options.EnableSsl
                ? SecureSocketOptions.StartTls
                : SecureSocketOptions.None;

            await client.ConnectAsync(
                _options.Host,
                _options.Port,
                secure,
                cancellationToken);

            await client.AuthenticateAsync(
                _options.User,
                _options.Password,
                cancellationToken);

            await client.SendAsync(message, cancellationToken);
            await client.DisconnectAsync(true, cancellationToken);
        }
    }
}