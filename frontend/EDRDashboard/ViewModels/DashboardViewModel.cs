using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;
using EDRDashboard.Services;
using LiveChartsCore;
using LiveChartsCore.SkiaSharpView;
using LiveChartsCore.SkiaSharpView.Painting;
using SkiaSharp;

namespace EDRDashboard.ViewModels
{
    public partial class DashboardViewModel : ObservableObject
    {
        private readonly MockDataService _dataService = new();

        [ObservableProperty]
        private DashboardStats stats = new();

        public ISeries[] AlertTrendSeries { get; }

        public Axis[] XAxes { get; }

        public Axis[] YAxes { get; }

        public DashboardViewModel()
        {
            Stats = _dataService.GetDashboardStats();

            AlertTrendSeries = new ISeries[]
            {
                new ColumnSeries<int>
                {
                    Name = "Alerts",
                    Values = new[] { 5, 9, 7, 11, 6, 8, 4 },
                    Fill = new SolidColorPaint(SKColors.DodgerBlue)
                }
            };

            XAxes = new Axis[]
            {
                new Axis
                {
                    Labels = new[]
                    {
                        "Mon",
                        "Tue",
                        "Wed",
                        "Thu",
                        "Fri",
                        "Sat",
                        "Sun"
                    }
                }
            };

            YAxes = new Axis[]
            {
                new Axis
                {
                    MinLimit = 0
                }
            };
        }

        public void Refresh()
        {
            Stats = _dataService.GetDashboardStats();
        }
    }
}