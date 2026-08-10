using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;
using EDRDashboard.Services;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace EDRDashboard.ViewModels
{
    public partial class IncidentViewModel : ObservableObject
    {
        private readonly ApiService _apiService = new();

        public ObservableCollection<Incident> Incidents { get; } = new();

        [ObservableProperty]
        private int openIncidentsCount;

        [ObservableProperty]
        private int criticalIncidentsCount;

        [ObservableProperty]
        private int investigatingCount;

        [ObservableProperty]
        private int containedCount;

        public IncidentViewModel()
        {
            _ = LoadIncidents();
        }

        public async Task LoadIncidents()
        {
            Incidents.Clear();

            var incidents = await _apiService.GetIncidentsAsync();

            int openCnt = 0;
            int critCnt = 0;
            int invCnt = 0;
            int contCnt = 0;

            foreach (var incident in incidents)
            {
                Incidents.Add(incident);

                if (string.Equals(incident.Status, "Open", StringComparison.OrdinalIgnoreCase)) openCnt++;
                else if (string.Equals(incident.Status, "Investigating", StringComparison.OrdinalIgnoreCase)) invCnt++;
                else if (string.Equals(incident.Status, "Contained", StringComparison.OrdinalIgnoreCase) || 
                         string.Equals(incident.Status, "Closed", StringComparison.OrdinalIgnoreCase)) contCnt++;

                if (string.Equals(incident.Severity, "Critical", StringComparison.OrdinalIgnoreCase)) critCnt++;
            }

            // Fallback default counts if database has no incidents yet
            if (incidents.Count == 0)
            {
                OpenIncidentsCount = 0;
                CriticalIncidentsCount = 0;
                InvestigatingCount = 0;
                ContainedCount = 0;
            }
            else
            {
                OpenIncidentsCount = openCnt;
                CriticalIncidentsCount = critCnt;
                InvestigatingCount = invCnt;
                ContainedCount = contCnt;
            }
        }

        public async Task Refresh()
        {
            await LoadIncidents();
        }
    }
}