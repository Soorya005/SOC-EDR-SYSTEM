using EDRDashboard.Models;
using EDRDashboard.ViewModels;
using Microsoft.UI.Xaml.Controls;

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

        private void FilterAll_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
        {
            ViewModel.FilterBySeverity("All");
        }

        private void FilterCritical_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
        {
            ViewModel.FilterBySeverity("Critical");
        }

        private void FilterHigh_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
        {
            ViewModel.FilterBySeverity("High");
        }

        private void FilterMedium_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
        {
            ViewModel.FilterBySeverity("Medium");
        }

        private void FilterLow_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
        {
            ViewModel.FilterBySeverity("Low");
        }
    }
}