using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;
using EDRDashboard.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;

namespace EDRDashboard.ViewModels
{
    public partial class AlertsViewModel : ObservableObject
    {
        private readonly ApiService _apiService = new();

        public ObservableCollection<Alert> Alerts { get; } = new();

        private List<Alert> _allAlerts = new();

        [ObservableProperty]
        private string selectedSeverity = "All";

        [ObservableProperty]
        private string selectedStatus = "All";

        [ObservableProperty]
        private string searchText = "";

        public AlertsViewModel()
        {
            _ = LoadAlerts();
        }

        public async Task LoadAlerts()
        {
            _allAlerts = await _apiService.GetAlertsAsync();
            ApplyFilters();
        }

        public void Search(string text)
        {
            SearchText = text;
            ApplyFilters();
        }

        public void FilterBySeverity(string severity)
        {
            SelectedSeverity = severity;
            ApplyFilters();
        }

        public void FilterByStatus(string status)
        {
            SelectedStatus = status;
            ApplyFilters();
        }

        public void ApplyFilters()
        {
            Alerts.Clear();
            IEnumerable<Alert> filtered = _allAlerts;

            if (!string.IsNullOrWhiteSpace(SearchText))
            {
                filtered = filtered.Where(a =>
                    a.Title.Contains(SearchText, StringComparison.OrdinalIgnoreCase) ||
                    a.Severity.Contains(SearchText, StringComparison.OrdinalIgnoreCase) ||
                    a.Status.Contains(SearchText, StringComparison.OrdinalIgnoreCase));
            }

            if (SelectedSeverity != "All" && SelectedSeverity != "All Severities")
            {
                filtered = filtered.Where(a =>
                    a.Severity.Equals(SelectedSeverity, StringComparison.OrdinalIgnoreCase));
            }

            if (SelectedStatus != "All" && SelectedStatus != "Status: All" && SelectedStatus != "All Statuses")
            {
                filtered = filtered.Where(a =>
                    a.Status.Equals(SelectedStatus, StringComparison.OrdinalIgnoreCase));
            }

            foreach (var alert in filtered)
                Alerts.Add(alert);
        }

        public async Task Refresh()
        {
            await LoadAlerts();
        }
    }
}