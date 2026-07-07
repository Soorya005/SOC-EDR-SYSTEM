using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Navigation;
using Microsoft.UI.Xaml;
using EDRDashboard.Models;
using EDRDashboard.ViewModels;

namespace EDRDashboard.Views
{
    public sealed partial class InvestigationPage : Page
    {
        public InvestigationViewModel ViewModel { get; }

        public InvestigationPage()
        {
            InitializeComponent();

            ViewModel = new InvestigationViewModel();

            DataContext = ViewModel;
        }

        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);

            if (e.Parameter is Alert alert)
            {
                ViewModel.Current.AlertTitle = alert.Title;
                ViewModel.Current.Severity = alert.Severity;
                ViewModel.Current.Status = alert.Status;
                ViewModel.Current.Time = alert.Time;

                switch (alert.Title)
                {
                    case "Encoded PowerShell Execution":

                        ViewModel.Current.Technique = "T1059.001";
                        ViewModel.Current.Tactic = "Execution";
                        ViewModel.Current.SigmaRule = "Suspicious Encoded PowerShell";
                        ViewModel.Current.Process = "powershell.exe";
                        ViewModel.Current.ParentProcess = "WINWORD.EXE";
                        ViewModel.Current.CommandLine =
                            "powershell.exe -EncodedCommand SQBFAFgA...";
                        ViewModel.Current.AiSummary =
                            "PowerShell launched from Microsoft Word using an encoded command. This commonly indicates phishing-based malware execution.";
                        break;

                    case "LSASS Memory Access":

                        ViewModel.Current.Technique = "T1003";
                        ViewModel.Current.Tactic = "Credential Access";
                        ViewModel.Current.SigmaRule = "LSASS Memory Read";
                        ViewModel.Current.Process = "procdump.exe";
                        ViewModel.Current.ParentProcess = "cmd.exe";
                        ViewModel.Current.CommandLine =
                            "procdump.exe -ma lsass.exe";
                        ViewModel.Current.AiSummary =
                            "A process attempted to dump LSASS memory, which may indicate credential dumping.";
                        break;

                    case "Registry Persistence":

                        ViewModel.Current.Technique = "T1547";
                        ViewModel.Current.Tactic = "Persistence";
                        ViewModel.Current.SigmaRule = "Registry Run Key";
                        ViewModel.Current.Process = "reg.exe";
                        ViewModel.Current.ParentProcess = "explorer.exe";
                        ViewModel.Current.CommandLine =
                            "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run";
                        ViewModel.Current.AiSummary =
                            "Registry Run keys were modified, suggesting persistence after reboot.";
                        break;

                    default:

                        ViewModel.Current.Technique = "T1047";
                        ViewModel.Current.Tactic = "Execution";
                        ViewModel.Current.SigmaRule = "Suspicious WMI";
                        ViewModel.Current.Process = "wmic.exe";
                        ViewModel.Current.ParentProcess = "powershell.exe";
                        ViewModel.Current.CommandLine =
                            "wmic process call create";
                        ViewModel.Current.AiSummary =
                            "Windows Management Instrumentation was used to execute a remote command.";
                        break;
                }
            }
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            if (Frame.CanGoBack)
                Frame.GoBack();
        }
    }
}