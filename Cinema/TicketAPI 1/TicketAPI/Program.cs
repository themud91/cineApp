using Microsoft.AspNetCore.HttpLogging;
using Serilog;
using Serilog.Events;
using TicketAPI.Filters;
using TicketAPI.Models;
using TicketAPI.Repositories;
using TicketAPI.Services;

// Logger provisoire actif des la premiere ligne. Sans lui, une exception levee
// dans CreateBuilder serait avalee en silence : le catch appellerait Log.Fatal
// sur un logger pas encore configure et le conteneur mourrait sans rien afficher.
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft.AspNetCore", LogEventLevel.Warning)
    .WriteTo.Console()
    .CreateBootstrapLogger();

try {
    var builder = WebApplication.CreateBuilder(args);

    builder.Services.AddHttpLogging(logging => {
        logging.LoggingFields = HttpLoggingFields.All;
        logging.RequestHeaders.Add("sec-ch-ua");
        logging.ResponseHeaders.Add("LoggingHeader");
        logging.RequestBodyLogLimit = 4096;
        logging.ResponseBodyLogLimit = 4096;
        logging.CombineLogs = true;
    });

    builder.Host.UseSerilog((context, configuration) => configuration.ReadFrom.Configuration(context.Configuration));
    Log.Information("Starting Web Application");
     

    builder.Services.AddControllers(); 
    builder.Services.AddEndpointsApiExplorer();
    builder.Services.AddSwaggerGen();

    //Enregistrement de la base de données JSON en tant que service singleton pour pouvoir l'injecter dans les repositories.
    builder.Services.AddSingleton(sp => {
        var env = sp.GetRequiredService<IWebHostEnvironment>();
        return new JsonFileDatabase<Billet>(env, "data.json");
    });

    //Enregistrement du service de courriel avec la configuration de appSettings.json.
    builder.Services.Configure<BrevoOptions>(
        builder.Configuration.GetSection("Brevo"));
    builder.Services.AddHttpClient<IEmailService, EmailService>(client => {
        client.BaseAddress = new Uri("https://api.brevo.com/");
    });
    // Service de repository pour gérer les billets, enregistré en tant que service scoped pour avoir une instance par requête HTTP.
    builder.Services.AddScoped<ITicketRepository, TicketRepository>();
    builder.Services.AddScoped<ApiKeyAuthFilter>();

    var app = builder.Build();
     
    if (app.Environment.IsDevelopment()) {
        app.UseSwagger();
        app.UseSwaggerUI();
    }

    // En production (Render) le TLS se termine au proxy et le conteneur recoit
    // du HTTP simple : la redirection n'a pas de port HTTPS a viser.
    if (app.Environment.IsDevelopment()) {
        app.UseHttpsRedirection();
    }

    app.UseAuthorization();

    app.MapControllers();


    Log.Information("Everything is fine!");

    app.Run();
} catch (Exception ex) {
    Log.Fatal(ex, "Application terminated unexpectedly");
    // Sans ceci le processus sort avec le code 0 et l'echec passe inapercu.
    Environment.ExitCode = 1;
} finally {
    Log.CloseAndFlush();
}
