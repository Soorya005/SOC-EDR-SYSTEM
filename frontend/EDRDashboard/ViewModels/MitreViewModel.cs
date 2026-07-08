using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;
using EDRDashboard.Services;
using System.Collections.ObjectModel;

namespace EDRDashboard.ViewModels
{
    public partial class MitreViewModel : ObservableObject
    {
        private readonly MockDataService _dataService = new();

        public ObservableCollection<MitreTechnique> Techniques { get; } = new();

        public MitreViewModel()
        {
            LoadTechniques();
        }

        public void LoadTechniques()
        {
            Techniques.Clear();

            foreach (var technique in _dataService.GetMitreTechniques())
            {
                Techniques.Add(technique);
            }
        }

        public void Refresh()
        {
            LoadTechniques();
        }
    }
}