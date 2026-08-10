using System;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Media;

namespace EDRDashboard.Converters
{
    public class ReportStatusToColorConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, string language)
        {
            if (value is string status)
            {
                var appResources = Application.Current.Resources;
                switch (status.Trim().ToLower())
                {
                    case "completed":
                        return appResources.TryGetValue("HealthyBrush", out var healthy) ? healthy : new SolidColorBrush(Microsoft.UI.Colors.Green);
                    case "generating":
                        return appResources.TryGetValue("AccentCyanBrush", out var generating) ? generating : new SolidColorBrush(Microsoft.UI.Colors.DeepSkyBlue);
                    case "failed":
                        return appResources.TryGetValue("CriticalBrush", out var failed) ? failed : new SolidColorBrush(Microsoft.UI.Colors.Red);
                }
            }
            return new SolidColorBrush(Microsoft.UI.Colors.Gray);
        }

        public object ConvertBack(object value, Type targetType, object parameter, string language)
        {
            throw new NotImplementedException();
        }
    }
}
