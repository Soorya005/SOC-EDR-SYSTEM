using System;
using System.Diagnostics;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI;
using EDRDashboard.Services;

namespace EDRDashboard.ViewModels
{
    public partial class SettingsViewModel : ObservableObject
    {
        private readonly ApiService _apiService = new ApiService();

        [ObservableProperty]
        private string apiUrl = "http://127.0.0.1:8000";

        [ObservableProperty]
        private string connectionStatusText = "Idle";

        [ObservableProperty]
        private SolidColorBrush connectionStatusBrush = new SolidColorBrush(Microsoft.UI.Colors.Gray);

        [ObservableProperty]
        private string databaseStatusText = "CHECKING...";

        [ObservableProperty]
        private SolidColorBrush databaseStatusBrush = new SolidColorBrush(Microsoft.UI.Colors.Gray);

        [ObservableProperty]
        private string aiStatusText = "CHECKING...";

        [ObservableProperty]
        private SolidColorBrush aiStatusBrush = new SolidColorBrush(Microsoft.UI.Colors.Gray);

        [ObservableProperty]
        private string sysmonStatusText = "CHECKING...";

        [ObservableProperty]
        private SolidColorBrush sysmonStatusBrush = new SolidColorBrush(Microsoft.UI.Colors.Gray);

        public SettingsViewModel()
        {
            _ = LoadStatusAsync();
        }

        public async Task LoadStatusAsync()
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

            // Set Database Status
            if (backendOnline && databaseOnline)
            {
                DatabaseStatusText = "CONNECTED";
                DatabaseStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#10B981")); // Green
            }
            else
            {
                DatabaseStatusText = "ERROR / DISCONNECTED";
                DatabaseStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#EF4444")); // Red
            }

            // Set AI Status
            if (aiOnline)
            {
                AiStatusText = "CONNECTED";
                AiStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#10B981"));
            }
            else
            {
                AiStatusText = "NOT AVAILABLE / OFFLINE";
                AiStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#EF4444"));
            }

            // Set Sysmon Status
            if (sysmonRunning)
            {
                SysmonStatusText = "RUNNING";
                SysmonStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#10B981"));
            }
            else
            {
                SysmonStatusText = "NOT RUNNING";
                SysmonStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#EF4444"));
            }
        }

        [RelayCommand]
        private async Task TestConnectionAsync()
        {
            ConnectionStatusText = "Testing connection...";
            ConnectionStatusBrush = new SolidColorBrush(Microsoft.UI.Colors.Gray);

            try
            {
                var health = await _apiService.GetHealthAsync();
                if (health != null && health.Status == "healthy")
                {
                    ConnectionStatusText = "Connected successfully to backend";
                    ConnectionStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#10B981"));
                }
                else
                {
                    ConnectionStatusText = "Failed to communicate with backend";
                    ConnectionStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#EF4444"));
                }
            }
            catch
            {
                ConnectionStatusText = "Backend host is unreachable";
                ConnectionStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#EF4444"));
            }

            // Refresh health stats as well
            await LoadStatusAsync();
        }

        [RelayCommand]
        private void SaveSettings()
        {
            ConnectionStatusText = "Settings saved (read-only configuration)";
            ConnectionStatusBrush = new SolidColorBrush(ColorHelper.ToColor("#00D2FF"));
        }
    }
}
