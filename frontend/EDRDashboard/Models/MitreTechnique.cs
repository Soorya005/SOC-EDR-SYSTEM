namespace EDRDashboard.Models
{
    public class MitreTechnique
    {
        public string TechniqueId { get; set; } = "";

        public string Name { get; set; } = "";

        public string Tactic { get; set; } = "";

        public int AlertCount { get; set; }

        public string Severity { get; set; } = "";
    }
}