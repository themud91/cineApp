namespace TicketAPI.Models {
    public sealed class SmtpOptions {
        public required string Host { get; init; }
        public required int Port { get; init; }
        public required string User { get; init; }
        public required string Password { get; init; }
        public required string FromName { get; init; }
        public required string FromEmail { get; init; }
        public required bool EnableSsl { get; init; }
    }
}
