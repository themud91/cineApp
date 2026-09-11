using Microsoft.AspNetCore.Mvc;

namespace TicketAPI.Controllers {
    //api/PingAPI/
    [Route("api/[controller]")]
    [ApiController]
    public class PingAPIController : ControllerBase {

        // version pour verifier le deploy sur Render
        private const string Version = "auth-fix-1";

        [HttpGet]
        public IActionResult Get() => Ok(new { ping = "pong", version = Version });
    }
}
