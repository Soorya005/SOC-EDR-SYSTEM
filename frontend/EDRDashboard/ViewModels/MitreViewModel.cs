using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;
using EDRDashboard.Services;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace EDRDashboard.ViewModels
{
    public partial class MitreViewModel : ObservableObject
    {
        private readonly ApiService _apiService = new();

        public ObservableCollection<MitreTechnique> Techniques { get; } = new();

        public MitreViewModel()
        {
            _ = LoadTechniques();
        }

        public async Task LoadTechniques()
        {
            Techniques.Clear();

            var techniques = await _apiService.GetMitreTechniquesAsync();

            foreach (var technique in techniques)
            {
                Techniques.Add(technique);
            }
        }

        public async Task Refresh()
        {
            await LoadTechniques();
        }
    }
}