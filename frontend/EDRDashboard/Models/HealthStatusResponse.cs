using System.Text.Json.Serialization;

namespace EDRDashboard.Models
{
    public class HealthStatusResponse
    {
        [JsonPropertyName("status")]
        public string Status { get; set; } = "";

        [JsonPropertyName("database")]
        public string Database { get; set; } = "";
    }
}
