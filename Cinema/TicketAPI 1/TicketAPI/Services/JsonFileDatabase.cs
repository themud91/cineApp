namespace TicketAPI.Services {
    using System.Text.Json;
    using System.Threading;

    //Ne touchez pas à cette classe, elle est utilisée pour stocker les données dans un fichier JSON.
    //Vous pouvez l'utiliser pour stocker les billets vendus.
    public class JsonFileDatabase<T> where T : class {
        private readonly string _filePath;
        private readonly SemaphoreSlim _lock = new(1, 1);
        private List<T> _data = [];

        public JsonFileDatabase(IWebHostEnvironment env, string fileName) {
            _filePath = Path.Combine(env.ContentRootPath, fileName);
            LoadFromFile().GetAwaiter().GetResult();
        }

        private async Task LoadFromFile() {
            if (!File.Exists(_filePath)) {
                await File.WriteAllTextAsync(_filePath, "[]");
            }

            var json = await File.ReadAllTextAsync(_filePath);
            _data = JsonSerializer.Deserialize<List<T>>(json)!;
        }

        public async Task<List<T>> GetAllAsync() {
            await _lock.WaitAsync();
            try {
                return [.. _data];
            } finally {
                _lock.Release();
            }
        }

        public async Task AddAsync(T item) {
            await _lock.WaitAsync();
            try {
                _data.Add(item);
                await SaveToFile();
            } finally {
                _lock.Release();
            }
        }

        private async Task SaveToFile() {
            var json = JsonSerializer.Serialize(_data, new JsonSerializerOptions {
                WriteIndented = true
            });

            await File.WriteAllTextAsync(_filePath, json);
        }
    }
}