using Microsoft.AspNetCore.Mvc;

namespace TicketAPI.Controllers {
    //api/PingAPI/
    [Route("api/[controller]")]
    [ApiController]
    public class PingAPIController : ControllerBase {

        // Marqueur de version : permet de verifier d'un seul curl que Render sert
        // bien le dernier commit, et non une couche Docker restee en cache.
        private const string Version = "auth-fix-1";

        [HttpGet]
        public IActionResult Get() => Ok(new { ping = "pong", version = Version });
    }
}
