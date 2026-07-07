using Microsoft.UI.Xaml.Controls;
using EDRDashboard.ViewModels;

namespace EDRDashboard.Views
{
    public sealed partial class MitrePage : Page
    {
        public MitrePage()
        {
            InitializeComponent();
            DataContext = new MitreViewModel();
        }
    }
}