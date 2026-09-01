namespace TicketAPI.Models {
    public sealed class BrevoOptions {
        public required string ApiKey { get; init; }
        public required string FromName { get; init; }
        public required string FromEmail { get; init; }
    }
}
