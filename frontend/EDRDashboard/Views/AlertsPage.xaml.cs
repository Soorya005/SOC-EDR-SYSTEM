using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using EDRDashboard.Models;
using EDRDashboard.ViewModels;

namespace EDRDashboard.Views
{
    public sealed partial class AlertsPage : Page
    {
        private AlertsViewModel ViewModel => (AlertsViewModel)DataContext;

        public AlertsPage()
        {
            InitializeComponent();

            DataContext = new AlertsViewModel();
        }

        private void AlertsList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (AlertsList.SelectedItem is Alert alert)
            {
                Frame.Navigate(typeof(InvestigationPage), alert);
            }
        }

        private void SearchBox_TextChanged(
            AutoSuggestBox sender,
            AutoSuggestBoxTextChangedEventArgs args)
        {
            ViewModel.Search(sender.Text);
        }

        private void SeverityCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (SeverityCombo == null || ViewModel == null) return;
            if (SeverityCombo.SelectedItem is ComboBoxItem item)
            {
                var severity = item.Content.ToString();
                if (severity == "All Severities") severity = "All";
                ViewModel.FilterBySeverity(severity);
            }
        }

        private void StatusCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (StatusCombo == null || ViewModel == null) return;
            if (StatusCombo.SelectedItem is ComboBoxItem item)
            {
                var status = item.Content.ToString();
                if (status == "All Statuses") status = "All";
                ViewModel.FilterByStatus(status);
            }
        }

        private async void RefreshButton_Click(object sender, RoutedEventArgs e)
        {
            await ViewModel.Refresh();
        }

        private void InvestigateButton_Click(object sender, RoutedEventArgs e)
        {
            if (sender is Button btn && btn.Tag is Alert alert)
            {
                Frame.Navigate(typeof(InvestigationPage), alert);
            }
        }
    }
}