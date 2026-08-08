using System.Text.Json.Serialization;

namespace EDRDashboard.Models
{
    public class Incident
    {
        [JsonPropertyName("id")]
        public string Id { get; set; } = "";

        [JsonPropertyName("host")]
        public string AffectedHost { get; set; } = "";

        [JsonPropertyName("severity")]
        public string Severity { get; set; } = "";

        [JsonPropertyName("status")]
        public string Status { get; set; } = "";

        [JsonPropertyName("created_at")]
        public string Created { get; set; } = "";

        // Placeholder until backend provides these
        public string Name { get; set; } = "Security Incident";

        public string Technique { get; set; } = "-";
    }
}