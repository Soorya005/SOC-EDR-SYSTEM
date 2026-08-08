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
                BaseAddress = new Uri("http://localhost:8000/")
            };
        }

        public async Task<DashboardStats> GetDashboardAsync()
{
    var response = await _httpClient.GetFromJsonAsync<DashboardSummaryResponse>(
        "stats/summary"
    );

    if (response == null)
    {
        return new DashboardStats();
    }

    return new DashboardStats
    {
        TotalAlerts = response.total_alerts,
        CriticalAlerts = response.critical_alerts,
        ActiveIncidents = response.active_incidents,
        MonitoredEndpoints = response.monitored_endpoints,

        BackendOnline = response.backend_online,
        DatabaseOnline = response.database_online,
        AiOnline = response.ai_online,
        SysmonRunning = response.sysmon_running,

        LastUpdated = response.last_updated
    };
}

        public async Task<List<Alert>> GetAlertsAsync()
{
    return await _httpClient.GetFromJsonAsync<List<Alert>>("alerts")
           ?? new List<Alert>();
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
    }
}