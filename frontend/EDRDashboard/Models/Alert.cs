using System.Text.Json.Serialization;

namespace EDRDashboard.Models
{
    public class Alert
    {
        [JsonPropertyName("id")]
        public string Id { get; set; } = "";

        [JsonPropertyName("rule_name")]
        public string Title { get; set; } = "";

        [JsonPropertyName("severity")]
        public string Severity { get; set; } = "";

        [JsonPropertyName("status")]
        public string Status { get; set; } = "";

        [JsonPropertyName("technique_id")]
        public string Technique { get; set; } = "";

        [JsonPropertyName("created_at")]
        public string Time { get; set; } = "";

        // Backend doesn't return endpoint yet
        public string Endpoint { get; set; } = "";
    }
}