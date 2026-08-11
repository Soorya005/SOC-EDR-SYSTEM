using System.Text.Json.Serialization;

namespace EDRDashboard.Models
{
    public class MitreTechnique
    {
        [JsonPropertyName("technique_id")]
        public string TechniqueId { get; set; } = "";

        [JsonPropertyName("name")]
        public string Name { get; set; } = "";

        [JsonPropertyName("tactic")]
        public string Tactic { get; set; } = "";

        [JsonPropertyName("alert_count")]
        public int AlertCount { get; set; }

        [JsonPropertyName("severity")]
        public string Severity { get; set; } = "";
    }
}