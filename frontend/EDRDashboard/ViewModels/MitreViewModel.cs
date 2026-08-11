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
    public partial class MitreViewModel : ObservableObject
    {
        private readonly ApiService _apiService = new();

        public ObservableCollection<MitreTechnique> Techniques { get; } = new();

        public ObservableCollection<Alert> RelatedAlerts { get; } = new();

        private MitreTechnique? _selectedTechnique;
        public MitreTechnique? SelectedTechnique
        {
            get => _selectedTechnique;
            set
            {
                if (SetProperty(ref _selectedTechnique, value))
                {
                    OnPropertyChanged(nameof(HasSelection));
                    _ = LoadRelatedAlerts();
                }
            }
        }

        public bool HasSelection => SelectedTechnique != null;

        [ObservableProperty]
        private int techniquesCount;

        [ObservableProperty]
        private int tacticsCount;

        [ObservableProperty]
        private int alertsCount;

        public MitreViewModel()
        {
            _ = LoadTechniques();
        }

        public async Task LoadTechniques()
        {
            Techniques.Clear();

            var techniques = await _apiService.GetMitreTechniquesAsync();

            int alertSum = 0;
            var tactics = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

            foreach (var technique in techniques)
            {
                Techniques.Add(technique);
                alertSum += technique.AlertCount;
                if (!string.IsNullOrEmpty(technique.Tactic))
                {
                    tactics.Add(technique.Tactic);
                }
            }

            TechniquesCount = techniques.Count;
            TacticsCount = tactics.Count;
            AlertsCount = alertSum;

            if (Techniques.Count > 0 && SelectedTechnique == null)
            {
                SelectedTechnique = Techniques[0];
            }
        }

        private async Task LoadRelatedAlerts()
        {
            RelatedAlerts.Clear();
            if (SelectedTechnique == null) return;

            try
            {
                var alerts = await _apiService.GetAlertsAsync();
                foreach (var alert in alerts)
                {
                    if (string.Equals(alert.Technique, SelectedTechnique.TechniqueId, StringComparison.OrdinalIgnoreCase))
                    {
                        RelatedAlerts.Add(alert);
                    }
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error loading related alerts: {ex.Message}");
            }
        }

        public async Task Refresh()
        {
            await LoadTechniques();
        }
    }
}