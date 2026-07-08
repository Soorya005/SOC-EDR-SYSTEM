using Microsoft.UI.Xaml.Controls;
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
    }
}