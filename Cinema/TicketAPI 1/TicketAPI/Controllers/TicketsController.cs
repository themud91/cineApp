using Microsoft.AspNetCore.Mvc;
using Serilog;
using TicketAPI.Models;
using TicketAPI.Repositories;
using TicketAPI.Requests;
using TicketAPI.Services;

namespace TicketAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TicketsController(ITicketRepository ticketRepository, IEmailService emailService) : ControllerBase
    {

        // GET /api/tickets/representation/{idRepresentation}
        [HttpGet("representation/{idRepresentation}")]
        public async Task<ActionResult<List<Billet>>> GetByRepresentation(int idRepresentation)
        {
            var billets = await ticketRepository.GetByRepresentationIdAsync(idRepresentation);
            return Ok(billets);
        }

        // GET /api/tickets/user/{idUtilisateur}
        [HttpGet("user/{idUtilisateur}")]
        public async Task<ActionResult<List<Billet>>> GetByUser(int idUtilisateur)
        {
            var billets = await ticketRepository.GetByUserIdAsync(idUtilisateur);
            return Ok(billets);
        }

        // POST /api/tickets
        [HttpPost]
        public async Task<ActionResult<Billet>> Create([FromBody] BilletRequest request)
        {
            var billet = new Billet
            {
                IdFilm = request.IdFilm,
                IdReprensation = request.IdRepresentation,
                IdSalle = request.IdSalle,
                IdUtilisateur = request.IdUtilisateur,
                Prix = request.Prix,
                NombreBillets = request.NombreBillets
            };

            await ticketRepository.AddAsync(billet);

            //Le courriel doit afficher les informations de la représentation (titre du film, salle, dateHeure) ainsi que le nombre de billets acheté.

            string htmlBody = $@"
      <h1>Merci pour votre achat !</h1>
      <p>Voici les informations de votre billet :</p>
      <ul>
          <li><strong>Numéro de billet :</strong> {billet.Id}</li>
          <li><strong>Film :</strong> {request.TitreFilm}</li>
          <li><strong>Salle :</strong> {request.NomSalle}</li>
          <li><strong>Date et heure :</strong> {request.DateHeure}</li>
          <li><strong>Nombre de billets :</strong> {billet.NombreBillets}</li>
          <li><strong>Prix total :</strong> {billet.Prix:C}</li>
      </ul>
  ";

            // Le billet est deja enregistre : un courriel qui ne part pas ne doit
            // pas annuler l'achat.
            try {
                await emailService.SendAsync(
                    to: request.Email,
                    subject: "Confirmation de votre achat – Cinéma La Pocatière",
                    htmlBody: htmlBody
                );
            } catch (Exception ex) {
                Log.Error(ex, "Envoi du courriel de confirmation echoue pour le billet {Id}", billet.Id);
            }

            return Created($"/api/tickets/{billet.Id}", billet);
        }
    }
}