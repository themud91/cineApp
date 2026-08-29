namespace TicketAPI.Models {
    public class Billet {
        public Guid Id { get; set; } = Guid.NewGuid();
        public int IdFilm { get; set; } = -1; //Id de votre serveur Python
        public int IdReprensation { get; set; } = -1; //Id de votre serveur Python
        public int IdSalle { get; set; } = -1; //Id de votre serveur Python  
        public int IdUtilisateur { get; set; } = -1; //Id de votre serveur Python  
        public decimal Prix { get; set; } = 0.00M;
        public int NombreBillets { get; set; } = 1; 
    }
}
