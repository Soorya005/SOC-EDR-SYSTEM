using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;
using EDRDashboard.Services;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace EDRDashboard.ViewModels
{
    public partial class IncidentViewModel : ObservableObject
    {
        private readonly ApiService _apiService = new();

        public ObservableCollection<Incident> Incidents { get; } = new();

        public IncidentViewModel()
{
    _ = LoadIncidents();
}

        public async Task LoadIncidents()
{
    Incidents.Clear();

    var incidents = await _apiService.GetIncidentsAsync();

    foreach (var incident in incidents)
    {
        Incidents.Add(incident);
    }
}

        public async Task Refresh()
{
    await LoadIncidents();
}
    }
}