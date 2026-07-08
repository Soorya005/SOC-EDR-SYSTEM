namespace EDRDashboard.Models
{
    public class Alert
    {
        public int Id { get; set; }

        public string Severity { get; set; } = "";

        public string Title { get; set; } = "";

        public string Status { get; set; } = "";

        public string Time { get; set; } = "";

        public string Technique { get; set; } = "";

        public string Endpoint { get; set; } = "";
    }
}