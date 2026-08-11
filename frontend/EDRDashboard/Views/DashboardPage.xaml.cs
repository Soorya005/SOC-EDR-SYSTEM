using Microsoft.UI.Xaml.Controls;
using EDRDashboard.Models;
using EDRDashboard.ViewModels;

namespace EDRDashboard.Views
{
    public sealed partial class DashboardPage : Page
    {
        public DashboardPage()
        {
            InitializeComponent();

            DataContext = new DashboardViewModel();
        }

        private void RecentAlertsList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (RecentAlertsList.SelectedItem is Alert alert)
            {
                Frame.Navigate(typeof(InvestigationPage), alert);
            }
        }
    }
}