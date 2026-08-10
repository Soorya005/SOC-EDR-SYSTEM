using System;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Media;

namespace EDRDashboard.Converters
{
    public class SeverityToColorConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, string language)
        {
            if (value is string severity)
            {
                var appResources = Application.Current.Resources;
                switch (severity.Trim().ToLower())
                {
                    case "critical":
                        return appResources.TryGetValue("CriticalBrush", out var crit) ? crit : new SolidColorBrush(Microsoft.UI.Colors.Red);
                    case "high":
                        return appResources.TryGetValue("HighBrush", out var high) ? high : new SolidColorBrush(Microsoft.UI.Colors.Orange);
                    case "medium":
                        return appResources.TryGetValue("MediumBrush", out var med) ? med : new SolidColorBrush(Microsoft.UI.Colors.Yellow);
                    case "low":
                        return appResources.TryGetValue("LowBrush", out var low) ? low : new SolidColorBrush(Microsoft.UI.Colors.Gray);
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
