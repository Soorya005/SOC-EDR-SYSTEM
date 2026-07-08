using System;
using System.Net.Http;
using System.Threading.Tasks;
namespace EDRDashboard.Services
{
    public class ApiService
    {
        private readonly HttpClient _httpClient;

        public ApiService()
        {
            _httpClient = new HttpClient
            {
                BaseAddress = new Uri("http://localhost:8000/")
            };
        }

        public async Task<string> GetDashboardAsync()
        {
            return await _httpClient.GetStringAsync("dashboard");
        }

        public async Task<string> GetAlertsAsync()
        {
            return await _httpClient.GetStringAsync("alerts");
        }

        public async Task<string> GetIncidentsAsync()
        {
            return await _httpClient.GetStringAsync("incidents");
        }

        public async Task<string> GetMitreAsync()
        {
            return await _httpClient.GetStringAsync("mitre");
        }

        public async Task<string> GetReportsAsync()
        {
            return await _httpClient.GetStringAsync("reports");
        }
    }
}