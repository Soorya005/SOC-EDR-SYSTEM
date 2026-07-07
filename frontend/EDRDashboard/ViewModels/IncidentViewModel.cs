using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;
using EDRDashboard.Services;
using System.Collections.ObjectModel;

namespace EDRDashboard.ViewModels
{
    public partial class IncidentViewModel : ObservableObject
    {
        private readonly MockDataService _dataService = new();

        public ObservableCollection<Incident> Incidents { get; } = new();

        public IncidentViewModel()
        {
            LoadIncidents();
        }

        public void LoadIncidents()
        {
            Incidents.Clear();

            foreach (var incident in _dataService.GetIncidents())
            {
                Incidents.Add(incident);
            }
        }

        public void Refresh()
        {
            LoadIncidents();
        }
    }
}