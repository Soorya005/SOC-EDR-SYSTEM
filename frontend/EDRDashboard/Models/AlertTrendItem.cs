using System.Text.Json.Serialization;

namespace EDRDashboard.Models
{
    public class AlertTrendItem
    {
        [JsonPropertyName("date")]
        public string Date { get; set; } = "";

        [JsonPropertyName("count")]
        public int Count { get; set; }
    }
}
