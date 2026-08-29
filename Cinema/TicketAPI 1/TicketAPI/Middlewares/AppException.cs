namespace TicketAPI.Middlewares {
    public sealed record AppException {
        public AppException(int statusCode, string message, string details) {
            StatusCode = statusCode;
            Message = message;
            Details = details;
        }

        public AppException(int statusCode, string message) {
            StatusCode = statusCode;
            Message = message;
        }

        public int StatusCode { get; private init; }
        public string Message { get; private init; }
        public string Details { get; private init; } = string.Empty;
    }
}
