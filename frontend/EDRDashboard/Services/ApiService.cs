using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using System.Net.Http.Json;
using EDRDashboard.Models;
namespace EDRDashboard.Services
{
    public class ApiService
    {
        private readonly HttpClient _httpClient;

        public ApiService()
        {
            _httpClient = new HttpClient
            {
                BaseAddress = new Uri("http://127.0.0.1:8000/")
            };
        }

        public async Task<DashboardStats> GetDashboardAsync()
        {
            DashboardSummaryResponse? response = null;
            bool backendOnline = false;
            bool databaseOnline = false;

            try
            {
                using var cts = new System.Threading.CancellationTokenSource(TimeSpan.FromSeconds(2));
                response = await _httpClient.GetFromJsonAsync<DashboardSummaryResponse>("stats/summary", cts.Token);
                backendOnline = true;
            }
            catch
            {
                backendOnline = false;
            }

            if (backendOnline && response != null)
            {
                var health = await GetHealthAsync();
                databaseOnline = health != null && health.Database == "connected";
            }

            bool aiOnline = await CheckOllamaStatusAsync();
            bool sysmonRunning = CheckSysmonRunning();

            if (response == null)
            {
                return new DashboardStats
                {
                    BackendOnline = false,
                    DatabaseOnline = false,
                    AiOnline = aiOnline,
                    SysmonRunning = sysmonRunning,
                    LastUpdated = DateTime.Now.ToString("dd MMM yyyy HH:mm")
                };
            }

            return new DashboardStats
            {
                TotalAlerts = response.TotalAlerts,
                CriticalAlerts = response.CriticalAlerts,
                ActiveIncidents = response.ActiveIncidents,
                MonitoredEndpoints = response.MonitoredEndpoints,

                BackendOnline = backendOnline,
                DatabaseOnline = databaseOnline,
                AiOnline = aiOnline,
                SysmonRunning = sysmonRunning,

                LastUpdated = response.LastUpdated
            };
        }

        public async Task<HealthStatusResponse?> GetHealthAsync()
        {
            try
            {
                using var cts = new System.Threading.CancellationTokenSource(TimeSpan.FromSeconds(2));
                return await _httpClient.GetFromJsonAsync<HealthStatusResponse>("health", cts.Token);
            }
            catch
            {
                return null;
            }
        }

        public async Task<bool> CheckOllamaStatusAsync()
        {
            try
            {
                using var localClient = new HttpClient { Timeout = TimeSpan.FromSeconds(2) };
                var response = await localClient.GetAsync("http://127.0.0.1:11434/");
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        public bool CheckSysmonRunning()
        {
            try
            {
                var sysmon = System.Diagnostics.Process.GetProcessesByName("Sysmon");
                var sysmon64 = System.Diagnostics.Process.GetProcessesByName("Sysmon64");
                return (sysmon != null && sysmon.Length > 0) || (sysmon64 != null && sysmon64.Length > 0);
            }
            catch
            {
                return false;
            }
        }


        public async Task<List<Alert>> GetAlertsAsync()
{
    return await _httpClient.GetFromJsonAsync<List<Alert>>("alerts")
           ?? new List<Alert>();
}

        public async Task<Alert?> GetAlertByIdAsync(string alertId)
        {
            try
            {
                using var cts = new System.Threading.CancellationTokenSource(TimeSpan.FromSeconds(5));
                return await _httpClient.GetFromJsonAsync<Alert>($"alerts/{alertId}", cts.Token);
            }
            catch
            {
                return null;
            }
        }

        public async Task<List<Incident>> GetIncidentsAsync()
{
    return await _httpClient.GetFromJsonAsync<List<Incident>>("incidents")
           ?? new List<Incident>();
}

        public async Task<string> GetMitreAsync()
        {
            return await _httpClient.GetStringAsync("mitre");
        }

        public async Task<List<Report>> GetReportsAsync()
{
    return await _httpClient.GetFromJsonAsync<List<Report>>("reports")
           ?? new List<Report>();
}

        public async Task<DailyReportResponse?> GenerateDailyReportAsync()
        {
            var response = await _httpClient.PostAsync("reports/daily", null);
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<DailyReportResponse>();
            }
            return null;
        }

        public async Task<List<MitreTechnique>> GetMitreTechniquesAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<MitreTechnique>>("mitre")
                   ?? new List<MitreTechnique>();
        }

        public async Task<List<AlertTrendItem>> GetAlertTrendsAsync()
        {
            return await _httpClient.GetFromJsonAsync<List<AlertTrendItem>>("stats/trends")
                   ?? new List<AlertTrendItem>();
        }
    }
}