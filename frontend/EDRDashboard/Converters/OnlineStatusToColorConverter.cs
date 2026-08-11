using System;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Media;

namespace EDRDashboard.Converters
{
    public class OnlineStatusToColorConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, string language)
        {
            var appResources = Application.Current.Resources;
            bool isOnline = value is bool && (bool)value;
            
            if (isOnline)
            {
                return appResources.TryGetValue("HealthyBrush", out var healthy) ? healthy : new SolidColorBrush(Microsoft.UI.Colors.LimeGreen);
            }
            else
            {
                return appResources.TryGetValue("CriticalBrush", out var critical) ? critical : new SolidColorBrush(Microsoft.UI.Colors.Red);
            }
        }

        public object ConvertBack(object value, Type targetType, object parameter, string language)
        {
            throw new NotImplementedException();
        }
    }
}
