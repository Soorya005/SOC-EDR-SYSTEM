namespace EDRDashboard.Models
{
    public class DashboardSummaryResponse
    {
        public int total_alerts { get; set; }

        public int critical_alerts { get; set; }

        public int active_incidents { get; set; }

        public int monitored_endpoints { get; set; }

        public bool backend_online { get; set; }

        public bool database_online { get; set; }

        public bool ai_online { get; set; }

        public bool sysmon_running { get; set; }

        public string last_updated { get; set; } = "";
    }
}