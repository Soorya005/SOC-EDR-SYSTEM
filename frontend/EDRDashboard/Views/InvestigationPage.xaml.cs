using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Navigation;
using Microsoft.UI.Xaml;
using EDRDashboard.Models;
using EDRDashboard.ViewModels;
using EDRDashboard.Services;

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

        protected override async void OnNavigatedTo(NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);

            if (e.Parameter is Alert alert)
            {
                // First populate with whatever we have locally
                PopulateAlertDetails(alert);

                // Now fetch complete dynamic details from backend API
                var apiService = new ApiService();
                var detailedAlert = await apiService.GetAlertByIdAsync(alert.Id);
                if (detailedAlert != null)
                {
                    PopulateAlertDetails(detailedAlert);
                }
            }
        }

        private void PopulateAlertDetails(Alert alert)
        {
            ViewModel.Current.AlertTitle = alert.Title;
            ViewModel.Current.AlertId = alert.Id;
            ViewModel.Current.Host = string.IsNullOrEmpty(alert.Endpoint) ? "WIN-DC-01" : alert.Endpoint;
            ViewModel.Current.Severity = alert.Severity;
            ViewModel.Current.Status = alert.Status;
            ViewModel.Current.Time = alert.Time;

            if (!string.IsNullOrEmpty(alert.Process))
            {
                ViewModel.Current.Technique = string.IsNullOrEmpty(alert.Technique) ? "T1047" : alert.Technique;
                ViewModel.Current.Tactic = string.IsNullOrEmpty(alert.Tactic) ? "Execution" : alert.Tactic;
                ViewModel.Current.SigmaRule = alert.Title;
                ViewModel.Current.Process = alert.Process;
                ViewModel.Current.ParentProcess = alert.ParentProcess;
                ViewModel.Current.CommandLine = alert.CommandLine;

                string explanation = string.IsNullOrEmpty(alert.AiExplanation) ? "" : alert.AiExplanation;
                string recs = string.IsNullOrEmpty(alert.AiRecommendations) ? "" : alert.AiRecommendations;
                if (!string.IsNullOrEmpty(explanation))
                {
                    ViewModel.Current.AiSummary = explanation + (string.IsNullOrEmpty(recs) ? "" : "\n\nRECOMMENDATIONS:\n" + recs);
                }
                else
                {
                    ViewModel.Current.AiSummary = "AI explanation is not available yet.";
                }
            }
            else
            {
                // Fallback to mock data if process info is not loaded/available yet
                switch (alert.Title)
                {
                    case "Encoded PowerShell Execution":
                        ViewModel.Current.Technique = "T1059.001";
                        ViewModel.Current.Tactic = "Execution";
                        ViewModel.Current.SigmaRule = "Suspicious Encoded PowerShell";
                        ViewModel.Current.Process = "powershell.exe";
                        ViewModel.Current.ParentProcess = "WINWORD.EXE";
                        ViewModel.Current.CommandLine = "powershell.exe -EncodedCommand SQBFAFgA...";
                        ViewModel.Current.AiSummary = "PowerShell launched from Microsoft Word using an encoded command. This commonly indicates phishing-based malware execution.";
                        break;
                    case "LSASS Memory Access":
                        ViewModel.Current.Technique = "T1003";
                        ViewModel.Current.Tactic = "Credential Access";
                        ViewModel.Current.SigmaRule = "LSASS Memory Read";
                        ViewModel.Current.Process = "procdump.exe";
                        ViewModel.Current.ParentProcess = "cmd.exe";
                        ViewModel.Current.CommandLine = "procdump.exe -ma lsass.exe";
                        ViewModel.Current.AiSummary = "A process attempted to dump LSASS memory, which may indicate credential dumping.";
                        break;
                    case "Registry Persistence":
                        ViewModel.Current.Technique = "T1547";
                        ViewModel.Current.Tactic = "Persistence";
                        ViewModel.Current.SigmaRule = "Registry Run Key";
                        ViewModel.Current.Process = "reg.exe";
                        ViewModel.Current.ParentProcess = "explorer.exe";
                        ViewModel.Current.CommandLine = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run";
                        ViewModel.Current.AiSummary = "Registry Run keys were modified, suggesting persistence after reboot.";
                        break;
                    default:
                        ViewModel.Current.Technique = "T1047";
                        ViewModel.Current.Tactic = "Execution";
                        ViewModel.Current.SigmaRule = "Suspicious WMI";
                        ViewModel.Current.Process = "wmic.exe";
                        ViewModel.Current.ParentProcess = "powershell.exe";
                        ViewModel.Current.CommandLine = "wmic process call create";
                        ViewModel.Current.AiSummary = "Windows Management Instrumentation was used to execute a remote command.";
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