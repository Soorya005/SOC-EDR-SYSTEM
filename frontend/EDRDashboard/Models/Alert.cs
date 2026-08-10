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

        [JsonPropertyName("host")]
        public string Endpoint { get; set; } = "";

        [JsonPropertyName("process_name")]
        public string Process { get; set; } = "";

        [JsonPropertyName("parent_process")]
        public string ParentProcess { get; set; } = "";

        [JsonPropertyName("command_line")]
        public string CommandLine { get; set; } = "";

        [JsonPropertyName("tactic")]
        public string Tactic { get; set; } = "";

        [JsonPropertyName("ai_explanation")]
        public string AiExplanation { get; set; } = "";

        [JsonPropertyName("ai_recommendations")]
        public string AiRecommendations { get; set; } = "";
    }
}