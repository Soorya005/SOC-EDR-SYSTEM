using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using EDRDashboard.Views;

namespace EDRDashboard
{
    public sealed partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            MainNavigation.DataContext = new ViewModels.MainViewModel();

            ContentFrame.Navigate(typeof(DashboardPage));
        }

        private void MainNavigation_SelectionChanged(
            NavigationView sender,
            NavigationViewSelectionChangedEventArgs args)
        {
            if (args.IsSettingsSelected)
            {
                ContentFrame.Navigate(typeof(SettingsPage));
                return;
            }

            if (args.SelectedItemContainer == null)
                return;

            switch (args.SelectedItemContainer.Tag?.ToString())
            {
                case "Dashboard":
                    ContentFrame.Navigate(typeof(DashboardPage));
                    break;

                case "Alerts":
                    ContentFrame.Navigate(typeof(AlertsPage));
                    break;

                case "Incidents":
                    ContentFrame.Navigate(typeof(IncidentsPage));
                    break;

                case "Mitre":
                    ContentFrame.Navigate(typeof(MitrePage));
                    break;

                case "Reports":
                    ContentFrame.Navigate(typeof(ReportsPage));
                    break;

                case "Settings":
                    ContentFrame.Navigate(typeof(SettingsPage));
                    break;

                case "Investigations":
                    ContentFrame.Navigate(typeof(InvestigationPage));
                    break;
            }
        }
    }
}