namespace EDRDashboard.Models
{
    public class Incident
    {
        public string Id { get; set; } = "";

        public string Name { get; set; } = "";

        public string Severity { get; set; } = "";

        public string Status { get; set; } = "";

        public string AffectedHost { get; set; } = "";

        public string Technique { get; set; } = "";

        public string Created { get; set; } = "";
    }
}