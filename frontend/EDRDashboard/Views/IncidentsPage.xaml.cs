using Microsoft.UI.Xaml.Controls;
using EDRDashboard.ViewModels;

namespace EDRDashboard.Views
{
    public sealed partial class IncidentsPage : Page
    {
        public IncidentsPage()
        {
            InitializeComponent();
            DataContext = new IncidentViewModel();
        }
    }
}