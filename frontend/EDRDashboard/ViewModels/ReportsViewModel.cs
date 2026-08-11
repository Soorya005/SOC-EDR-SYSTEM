using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using EDRDashboard.Models;
using EDRDashboard.Services;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Windows;

namespace EDRDashboard.ViewModels
{
    public partial class ReportsViewModel : ObservableObject
    {
        private readonly ApiService _apiService = new();

        public ObservableCollection<Report> Reports { get; } = new();

        private Report? _selectedReport;
        public Report? SelectedReport
        {
            get => _selectedReport;
            set => SetProperty(ref _selectedReport, value);
        }

        public IRelayCommand ExportCommand { get; }
        public IAsyncRelayCommand GenerateDailyReportCommand { get; }

        public ReportsViewModel()
        {
            ExportCommand = new RelayCommand(ExportSelected);
            GenerateDailyReportCommand = new AsyncRelayCommand(GenerateDailyReportAsync);

            _ = LoadReports();
        }

        private async Task GenerateDailyReportAsync()
        {
            try
            {
                var response = await _apiService.GenerateDailyReportAsync();
                if (response != null)
                {
                    await LoadReports();
                }
            }
            catch (System.Exception ex)
            {
                Debug.WriteLine($"Error generating daily report: {ex.Message}");
            }
        }

private void ExportSelected()
{
    if (SelectedReport == null)
    {
        Debug.WriteLine("No report selected");
        return;
    }

    Debug.WriteLine($"Selected Report: {SelectedReport.ReportName}");

    var url = $"http://localhost:8000/reports/download/{SelectedReport.ReportName}";

    Process.Start(new ProcessStartInfo
    {
        FileName = url,
        UseShellExecute = true
    });
}

        public async Task LoadReports()
        {
            Reports.Clear();

            var reports = await _apiService.GetReportsAsync();

            foreach (var report in reports)
            {
                Reports.Add(report);
            }
        }

        public async Task Refresh()
        {
            await LoadReports();
        }
    }
}