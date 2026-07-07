namespace EDRDashboard.Models
{
    public class Investigation
    {
        public string AlertTitle { get; set; } = "";

        public string Severity { get; set; } = "";

        public string Status { get; set; } = "";

        public string Time { get; set; } = "";

        public string AiSummary { get; set; } = "";

        public string Technique { get; set; } = "";

        public string Tactic { get; set; } = "";

        public string SigmaRule { get; set; } = "";

        public string Process { get; set; } = "";

        public string ParentProcess { get; set; } = "";

        public string CommandLine { get; set; } = "";
    }
}