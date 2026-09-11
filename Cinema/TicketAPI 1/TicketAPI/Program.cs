using Serilog;
using Serilog.Events;
using TicketAPI.Filters;
using TicketAPI.Middlewares;
using TicketAPI.Models;
using TicketAPI.Repositories;
using TicketAPI.Services;

// logger de demarrage pour voir les erreurs au lancement
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft.AspNetCore", LogEventLevel.Warning)
    .WriteTo.Console()
    .CreateBootstrapLogger();

try {
    var builder = WebApplication.CreateBuilder(args);

    builder.Host.UseSerilog((context, configuration) => configuration.ReadFrom.Configuration(context.Configuration));
    Log.Information("Starting Web Application");

    builder.Services.AddControllers();
    builder.Services.AddEndpointsApiExplorer();
    builder.Services.AddSwaggerGen();

    // base JSON en singleton
    builder.Services.AddSingleton(sp => {
        var env = sp.GetRequiredService<IWebHostEnvironment>();
        return new JsonFileDatabase<Billet>(env, "data.json");
    });

    // service email (config dans appsettings.json)
    builder.Services.Configure<BrevoOptions>(
        builder.Configuration.GetSection("Brevo"));
    builder.Services.AddHttpClient<IEmailService, EmailService>(client => {
        client.BaseAddress = new Uri("https://api.brevo.com/");
    });
    // repository en scoped (une instance par requete)
    builder.Services.AddScoped<ITicketRepository, TicketRepository>();
    builder.Services.AddScoped<ApiKeyAuthFilter>();

    var app = builder.Build();

    // middleware d'exceptions en premier
    app.UseMiddleware<GlobalExceptionMiddleware>();

    if (app.Environment.IsDevelopment()) {
        app.UseSwagger();
        app.UseSwaggerUI();
    }

    // pas de redirection HTTPS en prod, Render le gere
    if (app.Environment.IsDevelopment()) {
        app.UseHttpsRedirection();
    }

    app.UseAuthorization();

    app.MapControllers();


    Log.Information("Everything is fine!");

    app.Run();
} catch (Exception ex) {
    Log.Fatal(ex, "Application terminated unexpectedly");
    // sinon le process sort avec code 0
    Environment.ExitCode = 1;
} finally {
    Log.CloseAndFlush();
}
