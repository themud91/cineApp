namespace TicketAPI.Requests {
    public class BilletRequest {

        // TP3: objet requete POST /api/tickets
        public int IdFilm { get; set; }
        public int IdRepresentation { get; set; }
        public int IdSalle { get; set; }
        public int IdUtilisateur { get; set; }
        public decimal Prix { get; set; }
        public int NombreBillets { get; set; } = 1;
        public required string Email { get; set; }

        //Tp3 besoins user: "...mpLe courriel doit afficher les informations la représentation ainsi que du nombre de billets acheté..."
        public string TitreFilm { get; set; } = "";
        public string NomSalle { get; set; } = "";
        public string DateHeure { get; set; } = "";
    }
}
