using TicketAPI.Models;
using TicketAPI.Services;

namespace TicketAPI.Repositories {

    public class TicketRepository(JsonFileDatabase<Billet> database) : ITicketRepository {

        public async Task<List<Billet>> GetAllAsync() {
            return [.. (await database.GetAllAsync())];
        }

        public async Task<Billet?> GetByTicketIdAsync(Guid id) {
            var billets = await database.GetAllAsync();
            return billets.FirstOrDefault(b => b.Id == id);
        }

        public async Task AddAsync(Billet billet) {
            billet.Id = Guid.NewGuid();
            await database.AddAsync(billet); 
        }

        public async Task<List<Billet>> GetByRepresentationIdAsync(int idRepresentation)
        {
            var billets = await database.GetAllAsync();
            return [.. billets.Where(b => b.IdReprensation == idRepresentation)];
        }

        public async Task<List<Billet>> GetByUserIdAsync(int idUtilisateur)
        {
            var billets = await database.GetAllAsync();
            return [.. billets.Where(b => b.IdUtilisateur == idUtilisateur)];
        }
    }
}
