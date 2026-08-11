using System;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Data;

namespace EDRDashboard.Converters
{
    public class OnlineStatusToTextConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, string language)
        {
            bool isOnline = value is bool && (bool)value;
            return isOnline ? "NOMINAL" : "OFFLINE";
        }

        public object ConvertBack(object value, Type targetType, object parameter, string language)
        {
            throw new NotImplementedException();
        }
    }
}
