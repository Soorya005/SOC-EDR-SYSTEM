using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media;

namespace EDRDashboard.Controls
{
    public sealed partial class StatisticCard : UserControl
    {
        public StatisticCard()
        {
            InitializeComponent();
        }

        // Title
        public static readonly DependencyProperty TitleProperty =
            DependencyProperty.Register(
                nameof(Title),
                typeof(string),
                typeof(StatisticCard),
                new PropertyMetadata("", OnTitleChanged));

        public string Title
        {
            get => (string)GetValue(TitleProperty);
            set => SetValue(TitleProperty, value);
        }

        private static void OnTitleChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var card = (StatisticCard)d;
            card.TitleText.Text = e.NewValue?.ToString() ?? "";
        }

        // Value
        public static readonly DependencyProperty ValueProperty =
            DependencyProperty.Register(
                nameof(Value),
                typeof(object),
                typeof(StatisticCard),
                new PropertyMetadata(null, OnValueChanged));

        public object Value
        {
            get => GetValue(ValueProperty);
            set => SetValue(ValueProperty, value);
        }

        private static void OnValueChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var card = (StatisticCard)d;
            card.ValueText.Text = e.NewValue?.ToString() ?? "0";
        }

        // Accent
        public static readonly DependencyProperty AccentProperty =
            DependencyProperty.Register(
                nameof(Accent),
                typeof(Brush),
                typeof(StatisticCard),
                new PropertyMetadata(null, OnAccentChanged));

        public Brush Accent
        {
            get => (Brush)GetValue(AccentProperty);
            set => SetValue(AccentProperty, value);
        }

        private static void OnAccentChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var card = (StatisticCard)d;

            if (e.NewValue is Brush brush)
                card.AccentBar.Fill = brush;
        }
    }
}