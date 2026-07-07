using Microsoft.UI.Xaml.Controls;
using EDRDashboard.ViewModels;

namespace EDRDashboard.Views
{
    public sealed partial class ReportsPage : Page
    {
        public ReportsPage()
        {
            InitializeComponent();
            DataContext = new ReportsViewModel();
        }
    }
}