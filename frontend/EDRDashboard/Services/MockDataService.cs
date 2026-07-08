using System;
using System.Collections.Generic;
using EDRDashboard.Models;

namespace EDRDashboard.Services
{
    public class MockDataService
    {
        public List<Alert> GetAlerts()
        {
            return new List<Alert>
            {
                new Alert
                {
                    Severity = "Critical",
                    Title = "Encoded PowerShell Execution",
                    Status = "New",
                    Time = "Today • 16:42"
                },

                new Alert
                {
                    Severity = "High",
                    Title = "LSASS Memory Access",
                    Status = "Investigating",
                    Time = "Today • 16:20"
                },

                new Alert
                {
                    Severity = "Medium",
                    Title = "Registry Persistence",
                    Status = "Escalated",
                    Time = "Today • 15:58"
                },

                new Alert
                {
                    Severity = "Low",
                    Title = "WMI Execution",
                    Status = "Closed",
                    Time = "Today • 15:30"
                }
            };
        }

        public DashboardStats GetDashboardStats()
        {
            return new DashboardStats
            {
                TotalAlerts = GetAlerts().Count,
                CriticalAlerts = GetAlerts().FindAll(a => a.Severity == "Critical").Count,
                ActiveIncidents = GetIncidents().Count,
                MonitoredEndpoints = 1,

                BackendOnline = true,
                DatabaseOnline = true,
                AiOnline = true,
                SysmonRunning = true,

                LastUpdated = DateTime.Now.ToString("dd MMM yyyy HH:mm")
            };
        }

        public List<Incident> GetIncidents()
        {
            return new List<Incident>
            {
                new Incident
                {
                    Id="INC-001",
                    Name="PowerShell Malware Execution",
                    Severity="Critical",
                    Status="Open",
                    AffectedHost="DESKTOP-01",
                    Technique="T1059.001",
                    Created="Today 16:42"
                },

                new Incident
                {
                    Id="INC-002",
                    Name="Credential Dump Attempt",
                    Severity="High",
                    Status="Investigating",
                    AffectedHost="SERVER-02",
                    Technique="T1003",
                    Created="Today 16:20"
                },

                new Incident
                {
                    Id="INC-003",
                    Name="Registry Persistence",
                    Severity="Medium",
                    Status="Contained",
                    AffectedHost="PC-07",
                    Technique="T1547",
                    Created="Today 15:58"
                }
            };
        }

        public List<MitreTechnique> GetMitreTechniques()
        {
            return new List<MitreTechnique>
            {
                new MitreTechnique
                {
                    TechniqueId="T1059.001",
                    Name="PowerShell",
                    Tactic="Execution",
                    AlertCount=14,
                    Severity="Critical"
                },

                new MitreTechnique
                {
                    TechniqueId="T1003",
                    Name="Credential Dumping",
                    Tactic="Credential Access",
                    AlertCount=8,
                    Severity="High"
                },

                new MitreTechnique
                {
                    TechniqueId="T1547",
                    Name="Registry Run Keys",
                    Tactic="Persistence",
                    AlertCount=5,
                    Severity="Medium"
                },

                new MitreTechnique
                {
                    TechniqueId="T1105",
                    Name="Ingress Tool Transfer",
                    Tactic="Command and Control",
                    AlertCount=3,
                    Severity="Low"
                }
            };
        }

        public List<Report> GetReports()
        {
            return new List<Report>
            {
                new Report
                {
                    ReportName="Daily Security Report",
                    Type="PDF",
                    GeneratedBy="AI Engine",
                    Created="Today",
                    Status="Completed"
                },

                new Report
                {
                    ReportName="Incident Summary",
                    Type="PDF",
                    GeneratedBy="SOC Analyst",
                    Created="Today",
                    Status="Completed"
                },

                new Report
                {
                    ReportName="MITRE Mapping",
                    Type="PDF",
                    GeneratedBy="AI Engine",
                    Created="Yesterday",
                    Status="Completed"
                }
            };
        }

        public Investigation GetInvestigation(Alert alert)
        {
            return new Investigation
            {
                AlertTitle = alert.Title,
                Severity = alert.Severity,
                Status = alert.Status,
                Time = alert.Time,

                Technique = "T1059.001",
                Tactic = "Execution",
                SigmaRule = "Suspicious Encoded PowerShell",

                Process = "powershell.exe",
                ParentProcess = "WINWORD.EXE",
                CommandLine = "powershell.exe -EncodedCommand SQBFAFgA...",

                AiSummary =
                    "AI analysis indicates suspicious execution behavior consistent with phishing-delivered PowerShell malware."
            };
        }
    }
}