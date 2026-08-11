using System.Text.Json.Serialization;

namespace EDRDashboard.Models
{
    public class Report
    {
        [JsonPropertyName("report_name")]
        public string ReportName { get; set; } = "";

        [JsonPropertyName("type")]
        public string Type { get; set; } = "";

        [JsonPropertyName("generated_by")]
        public string GeneratedBy { get; set; } = "";

        [JsonPropertyName("created")]
        public string Created { get; set; } = "";

        [JsonPropertyName("status")]
        public string Status { get; set; } = "";
    }
}