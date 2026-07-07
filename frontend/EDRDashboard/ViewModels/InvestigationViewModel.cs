using CommunityToolkit.Mvvm.ComponentModel;
using EDRDashboard.Models;

namespace EDRDashboard.ViewModels
{
    public partial class InvestigationViewModel : ObservableObject
    {
        public Investigation Current { get; }

        public InvestigationViewModel()
        {
            Current = new Investigation
            {
                AlertTitle = "Encoded PowerShell Execution",

                Severity = "Critical",

                Status = "New",

                Time = "Today • 16:42",

                Technique = "T1059.001",

                Tactic = "Execution",

                SigmaRule = "Suspicious Encoded PowerShell",

                AiSummary =
                "PowerShell was launched from WINWORD.EXE using an encoded command. This behaviour is commonly associated with phishing attacks attempting to execute hidden scripts.",

                Process = "powershell.exe",

                ParentProcess = "WINWORD.EXE",

                CommandLine =
                "powershell.exe -EncodedCommand SQBFAFgA..."
            };
        }
    }
}