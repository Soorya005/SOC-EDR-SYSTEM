using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;
using EDRDashboard.Services;
using System.Collections.ObjectModel;

namespace EDRDashboard.ViewModels
{
    public partial class ReportsViewModel : ObservableObject
    {
        private readonly MockDataService _dataService = new();

        public ObservableCollection<Report> Reports { get; } = new();

        public ReportsViewModel()
        {
            LoadReports();
        }

        public void LoadReports()
        {
            Reports.Clear();

            foreach (var report in _dataService.GetReports())
            {
                Reports.Add(report);
            }
        }

        public void Refresh()
        {
            LoadReports();
        }
    }
}