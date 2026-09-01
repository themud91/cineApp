using Microsoft.AspNetCore.Mvc;
using TicketAPI.Repositories;
using TicketAPI.Services;

namespace TicketAPI.Controllers {
    //api/PingAPI/
    [Route("api/[controller]")]
    [ApiController]
    public class PingAPIController(ITicketRepository ticketRepository) : ControllerBase {
        [HttpGet]
        public OkObjectResult Get() {
            return Ok("{\"ping\":\"pong\"}");
        } 
    }
}