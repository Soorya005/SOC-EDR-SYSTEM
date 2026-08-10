using System.Text.Json.Serialization;

namespace EDRDashboard.Models
{
    public class DashboardSummaryResponse
    {
        [JsonPropertyName("total_alerts")]
        public int TotalAlerts { get; set; }

        [JsonPropertyName("critical_alerts")]
        public int CriticalAlerts { get; set; }

        [JsonPropertyName("active_incidents")]
        public int ActiveIncidents { get; set; }

        [JsonPropertyName("monitored_endpoints")]
        public int MonitoredEndpoints { get; set; }

        [JsonPropertyName("backend_online")]
        public bool BackendOnline { get; set; }

        [JsonPropertyName("database_online")]
        public bool DatabaseOnline { get; set; }

        [JsonPropertyName("ai_online")]
        public bool AiOnline { get; set; }

        [JsonPropertyName("sysmon_running")]
        public bool SysmonRunning { get; set; }

        [JsonPropertyName("last_updated")]
        public string LastUpdated { get; set; } = "";
    }
}