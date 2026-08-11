using System.Text.Json.Serialization;

namespace EDRDashboard.Models
{
    public class DailyReportResponse
    {
        [JsonPropertyName("filename")]
        public string Filename { get; set; } = "";

        [JsonPropertyName("download_url")]
        public string DownloadUrl { get; set; } = "";
    }
}
