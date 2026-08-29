using TicketAPI.Models;

namespace TicketAPI.Repositories {
    public interface ITicketRepository {
        Task<List<Billet>> GetAllAsync();
        Task<Billet?> GetByTicketIdAsync(Guid id);
        Task AddAsync(Billet billet);
        Task<List<Billet>> GetByRepresentationIdAsync(int idRepresentation);
        Task<List<Billet>> GetByUserIdAsync(int idUtilisateur);
    }
}
