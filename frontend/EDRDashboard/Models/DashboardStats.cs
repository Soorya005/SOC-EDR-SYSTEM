namespace EDRDashboard.Models
{
    public class DashboardStats
    {
        public int TotalAlerts { get; set; }

        public int CriticalAlerts { get; set; }

        public int ActiveIncidents { get; set; }

        public int MonitoredEndpoints { get; set; }

        public string LastUpdated { get; set; } = "";

        public bool BackendOnline { get; set; }

        public bool DatabaseOnline { get; set; }

        public bool AiOnline { get; set; }

        public bool SysmonRunning { get; set; }
    }
}
