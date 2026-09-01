using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using System.Runtime.InteropServices;
using TicketAPI.Repositories;
using TicketAPI.Services;

namespace TicketAPI.Controllers {
    //api/PingAPI/
    [Route("api/[controller]")]
    [ApiController]
    public class PingAPIController(ITicketRepository ticketRepository) : ControllerBase {
        [HttpGet]
        public OkObjectResult Get() {
            return Ok("{\"ping\":\"pong\",\"diag\":\"v3-global-mw\"}");
        }

        // DIAGNOSTIC TEMPORAIRE : liste les filtres MVC globaux et la version du runtime.
        [HttpGet("diag-info")]
        public ActionResult DiagInfo([FromServices] IOptions<MvcOptions> mvcOptions) {
            var filters = mvcOptions.Value.Filters.Select(f => f.ToString()).ToList();
            return Ok(new {
                framework = RuntimeInformation.FrameworkDescription,
                osDescription = RuntimeInformation.OSDescription,
                filters
            });
        }
    }
}