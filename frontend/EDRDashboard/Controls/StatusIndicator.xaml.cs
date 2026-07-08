using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI;

namespace EDRDashboard.Controls
{
    public sealed partial class StatusIndicator : UserControl
    {
        public StatusIndicator()
        {
            InitializeComponent();
        }

        // Text

        public static readonly DependencyProperty TextProperty =
            DependencyProperty.Register(
                nameof(Text),
                typeof(string),
                typeof(StatusIndicator),
                new PropertyMetadata("Online", OnTextChanged));

        public string Text
        {
            get => (string)GetValue(TextProperty);
            set => SetValue(TextProperty, value);
        }

        private static void OnTextChanged(
            DependencyObject d,
            DependencyPropertyChangedEventArgs e)
        {
            var control = (StatusIndicator)d;
            control.StatusText.Text = e.NewValue?.ToString() ?? "";
        }

        // IsOnline

        public static readonly DependencyProperty IsOnlineProperty =
            DependencyProperty.Register(
                nameof(IsOnline),
                typeof(bool),
                typeof(StatusIndicator),
                new PropertyMetadata(true, OnStatusChanged));

        public bool IsOnline
        {
            get => (bool)GetValue(IsOnlineProperty);
            set => SetValue(IsOnlineProperty, value);
        }

        private static void OnStatusChanged(
            DependencyObject d,
            DependencyPropertyChangedEventArgs e)
        {
            var control = (StatusIndicator)d;

            bool online = (bool)e.NewValue;

            control.StatusDot.Fill =
                new SolidColorBrush(
                    online ? Colors.LimeGreen : Colors.Red);
        }
    }
}