using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Threading.Tasks;
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
        private readonly ApiService _apiService = new();

        [ObservableProperty]
        private DashboardStats stats = new();

        public ObservableCollection<Alert> RecentAlerts { get; } = new();

        [ObservableProperty]
        private ISeries[] alertTrendSeries = new ISeries[0];

        [ObservableProperty]
        private Axis[] xAxes = new Axis[0];

        [ObservableProperty]
        private Axis[] yAxes = new Axis[0];

        [ObservableProperty]
        private int criticalCount;
        
        [ObservableProperty]
        private int highCount;
        
        [ObservableProperty]
        private int mediumCount;
        
        [ObservableProperty]
        private int lowCount;
        
        [ObservableProperty]
        private double criticalPercent;
        
        [ObservableProperty]
        private double highPercent;
        
        [ObservableProperty]
        private double mediumPercent;
        
        [ObservableProperty]
        private double lowPercent;

        public DashboardViewModel()
        {
            // Initial mock series in case API takes time to return
            AlertTrendSeries = new ISeries[]
            {
                new LineSeries<int>
                {
                    Name = "Alerts",
                    Values = new[] { 0, 0, 0, 0, 0, 0, 0 },
                    Stroke = new SolidColorPaint(SKColor.Parse("#00D2FF"), 2),
                    Fill = new SolidColorPaint(SKColor.Parse("#00D2FF").WithAlpha(20)),
                    GeometrySize = 0,
                    LineSmoothness = 0.6
                }
            };

            XAxes = new Axis[]
            {
                new Axis
                {
                    Labels = new[] { "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" },
                    LabelsPaint = new SolidColorPaint(SKColor.Parse("#6B7280")),
                    SeparatorsPaint = new SolidColorPaint(SKColor.Parse("#1E222B")) { StrokeThickness = 1 }
                }
            };

            YAxes = new Axis[]
            {
                new Axis
                {
                    LabelsPaint = new SolidColorPaint(SKColor.Parse("#6B7280")),
                    SeparatorsPaint = new SolidColorPaint(SKColor.Parse("#1E222B")) { StrokeThickness = 1 },
                    MinLimit = 0
                }
            };

            _ = LoadDashboardAsync();
        }

        public async Task LoadDashboardAsync()
        {
            Stats = await _apiService.GetDashboardAsync();
            if (Stats.BackendOnline)
            {
                await LoadTrendDataAsync();
                await LoadRecentAlertsAsync();
            }
            else
            {
                ClearDashboardData();
            }
        }

        private async Task LoadRecentAlertsAsync()
        {
            try
            {
                var alerts = await _apiService.GetAlertsAsync();
                RecentAlerts.Clear();
                int count = 0;
                foreach (var alert in alerts)
                {
                    RecentAlerts.Add(alert);
                    count++;
                    if (count >= 4) break;
                }

                int crit = 0, high = 0, med = 0, low = 0;
                foreach (var alert in alerts)
                {
                    if (string.Equals(alert.Severity, "Critical", StringComparison.OrdinalIgnoreCase)) crit++;
                    else if (string.Equals(alert.Severity, "High", StringComparison.OrdinalIgnoreCase)) high++;
                    else if (string.Equals(alert.Severity, "Medium", StringComparison.OrdinalIgnoreCase)) med++;
                    else if (string.Equals(alert.Severity, "Low", StringComparison.OrdinalIgnoreCase)) low++;
                    else low++; // default fallback
                }
                
                CriticalCount = crit;
                HighCount = high;
                MediumCount = med;
                LowCount = low;
                
                int total = crit + high + med + low;
                if (total > 0)
                {
                    CriticalPercent = (double)crit / total * 100;
                    HighPercent = (double)high / total * 100;
                    MediumPercent = (double)med / total * 100;
                    LowPercent = (double)low / total * 100;
                }
                else
                {
                    CriticalPercent = 0;
                    HighPercent = 0;
                    MediumPercent = 0;
                    LowPercent = 0;
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error loading recent alerts: {ex.Message}");
            }
        }

        private async Task LoadTrendDataAsync()
        {
            try
            {
                var trends = await _apiService.GetAlertTrendsAsync();
                
                var dates = new List<string>();
                var counts = new List<int>();
                
                foreach (var item in trends)
                {
                    if (DateTime.TryParse(item.Date, out var dt))
                    {
                        dates.Add(dt.ToString("dd MMM"));
                    }
                    else
                    {
                        dates.Add(item.Date);
                    }
                    counts.Add(item.Count);
                }
                
                if (counts.Count == 0)
                {
                    dates.AddRange(new[] { "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" });
                    counts.AddRange(new[] { 0, 0, 0, 0, 0, 0, 0 });
                }
                
                AlertTrendSeries = new ISeries[]
                {
                    new LineSeries<int>
                    {
                        Name = "Alerts",
                        Values = counts.ToArray(),
                        Stroke = new SolidColorPaint(SKColor.Parse("#00D2FF"), 2),
                        Fill = new SolidColorPaint(SKColor.Parse("#00D2FF").WithAlpha(20)),
                        GeometrySize = 6,
                        GeometryStroke = new SolidColorPaint(SKColor.Parse("#00D2FF"), 2),
                        GeometryFill = new SolidColorPaint(SKColor.Parse("#0B0C10")),
                        LineSmoothness = 0.6
                    }
                };
                
                XAxes = new Axis[]
                {
                    new Axis
                    {
                        Labels = dates.ToArray(),
                        LabelsPaint = new SolidColorPaint(SKColor.Parse("#6B7280")),
                        SeparatorsPaint = new SolidColorPaint(SKColor.Parse("#1E222B")) { StrokeThickness = 1 }
                    }
                };
                
                YAxes = new Axis[]
                {
                    new Axis
                    {
                        LabelsPaint = new SolidColorPaint(SKColor.Parse("#6B7280")),
                        SeparatorsPaint = new SolidColorPaint(SKColor.Parse("#1E222B")) { StrokeThickness = 1 },
                        MinLimit = 0
                    }
                };
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error loading trend data: {ex.Message}");
            }
        }

        public async Task Refresh()
        {
            Stats = await _apiService.GetDashboardAsync();
            if (Stats.BackendOnline)
            {
                await LoadTrendDataAsync();
                await LoadRecentAlertsAsync();
            }
            else
            {
                ClearDashboardData();
            }
        }

        private void ClearDashboardData()
        {
            RecentAlerts.Clear();
            CriticalCount = 0;
            HighCount = 0;
            MediumCount = 0;
            LowCount = 0;
            CriticalPercent = 0;
            HighPercent = 0;
            MediumPercent = 0;
            LowPercent = 0;

            AlertTrendSeries = new ISeries[]
            {
                new LineSeries<int>
                {
                    Name = "Alerts",
                    Values = new[] { 0, 0, 0, 0, 0, 0, 0 },
                    Stroke = new SolidColorPaint(SKColor.Parse("#00D2FF"), 2),
                    Fill = new SolidColorPaint(SKColor.Parse("#00D2FF").WithAlpha(20)),
                    GeometrySize = 0,
                    LineSmoothness = 0.6
                }
            };
            XAxes = new Axis[]
            {
                new Axis
                {
                    Labels = new[] { "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" },
                    LabelsPaint = new SolidColorPaint(SKColor.Parse("#6B7280")),
                    SeparatorsPaint = new SolidColorPaint(SKColor.Parse("#1E222B")) { StrokeThickness = 1 }
                }
            };
            YAxes = new Axis[]
            {
                new Axis
                {
                    LabelsPaint = new SolidColorPaint(SKColor.Parse("#6B7280")),
                    SeparatorsPaint = new SolidColorPaint(SKColor.Parse("#1E222B")) { StrokeThickness = 1 },
                    MinLimit = 0
                }
            };
        }
    }
}