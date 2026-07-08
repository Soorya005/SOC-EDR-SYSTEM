using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;
using EDRDashboard.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace EDRDashboard.ViewModels
{
    public partial class AlertsViewModel : ObservableObject
    {
        private readonly MockDataService _dataService = new();

        public ObservableCollection<Alert> Alerts { get; } = new();

        private List<Alert> _allAlerts = new();

        public AlertsViewModel()
        {
            LoadAlerts();
        }

        public void LoadAlerts()
        {
            _allAlerts = _dataService.GetAlerts();

            Alerts.Clear();

            foreach (var alert in _allAlerts)
                Alerts.Add(alert);
        }

        public void Search(string text)
        {
            Alerts.Clear();

            IEnumerable<Alert> filtered;

            if (string.IsNullOrWhiteSpace(text))
            {
                filtered = _allAlerts;
            }
            else
            {
                filtered = _allAlerts.Where(a =>
                    a.Title.Contains(text, StringComparison.OrdinalIgnoreCase) ||
                    a.Severity.Contains(text, StringComparison.OrdinalIgnoreCase) ||
                    a.Status.Contains(text, StringComparison.OrdinalIgnoreCase));
            }

            foreach (var alert in filtered)
                Alerts.Add(alert);
        }

        public void FilterBySeverity(string severity)
        {
            Alerts.Clear();

            IEnumerable<Alert> filtered;

            if (severity == "All")
            {
                filtered = _allAlerts;
            }
            else
            {
                filtered = _allAlerts.Where(a =>
                    a.Severity.Equals(severity, StringComparison.OrdinalIgnoreCase));
            }

            foreach (var alert in filtered)
                Alerts.Add(alert);
        }

        public void Refresh()
        {
            LoadAlerts();
        }
    }
}