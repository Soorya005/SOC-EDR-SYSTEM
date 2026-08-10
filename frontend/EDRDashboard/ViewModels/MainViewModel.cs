using System;
using System.Diagnostics;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using Microsoft.UI.Xaml.Media;
using EDRDashboard.Services;
using Microsoft.UI;
using Microsoft.UI.Xaml;

namespace EDRDashboard.ViewModels
{
    public partial class MainViewModel : ObservableObject
    {
        private readonly ApiService _apiService = new ApiService();
        private readonly DispatcherTimer _timer;

        [ObservableProperty]
        private string systemStatusText = "Checking systems...";

        [ObservableProperty]
        private SolidColorBrush systemStatusColor = new SolidColorBrush(Microsoft.UI.Colors.Gray);

        [ObservableProperty]
        private SolidColorBrush systemStatusDotColor = new SolidColorBrush(Microsoft.UI.Colors.Gray);

        public MainViewModel()
        {
            _timer = new DispatcherTimer();
            _timer.Interval = TimeSpan.FromSeconds(5);
            _timer.Tick += async (s, e) => await RunHealthCheckAsync();
            _timer.Start();

            // Run first check immediately
            _ = RunHealthCheckAsync();
        }

        public async Task RunHealthCheckAsync()
        {
            bool backendOnline = false;
            bool databaseOnline = false;

            try
            {
                var health = await _apiService.GetHealthAsync();
                backendOnline = health != null && health.Status == "healthy";
                databaseOnline = health != null && health.Database == "connected";
            }
            catch
            {
                backendOnline = false;
                databaseOnline = false;
            }

            bool aiOnline = await _apiService.CheckOllamaStatusAsync();
            bool sysmonRunning = _apiService.CheckSysmonRunning();

            if (backendOnline && databaseOnline && aiOnline && sysmonRunning)
            {
                SystemStatusText = "All systems operational";
                SystemStatusColor = new SolidColorBrush(ColorHelper.ToColor("#10B981"));
                SystemStatusDotColor = new SolidColorBrush(ColorHelper.ToColor("#10B981"));
            }
            else if (!backendOnline && !databaseOnline && !aiOnline && !sysmonRunning)
            {
                SystemStatusText = "All systems offline";
                SystemStatusColor = new SolidColorBrush(ColorHelper.ToColor("#EF4444"));
                SystemStatusDotColor = new SolidColorBrush(ColorHelper.ToColor("#EF4444"));
            }
            else
            {
                SystemStatusText = "System attention required";
                SystemStatusColor = new SolidColorBrush(ColorHelper.ToColor("#F97316"));
                SystemStatusDotColor = new SolidColorBrush(ColorHelper.ToColor("#F97316"));
            }
        }
    }

    public static class ColorHelper
    {
        public static Windows.UI.Color ToColor(string hex)
        {
            hex = hex.Replace("#", "");
            byte r = byte.Parse(hex.Substring(0, 2), System.Globalization.NumberStyles.HexNumber);
            byte g = byte.Parse(hex.Substring(2, 2), System.Globalization.NumberStyles.HexNumber);
            byte b = byte.Parse(hex.Substring(4, 2), System.Globalization.NumberStyles.HexNumber);
            return Windows.UI.Color.FromArgb(255, r, g, b);
        }
    }
}
