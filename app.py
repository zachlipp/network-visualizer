import dash

external_stylesheets = [
    "http://berniesandersofficial.com/wp-includes/css/dist/block-library/style.min.css?ver=5.2.3",
    "http://berniesandersofficial.com/wp-content/plugins/cpo-companion/assets/css/fontawesome.css?ver=5.2.3",
    "http://berniesandersofficial.com/wp-content/plugins/kiwi-social-share/assets/vendors/icomoon/style.css?ver=2.0.15",
    "http://berniesandersofficial.com/wp-content/themes/allegiant/core/css/base.css?ver=5.2.3",
    "http://berniesandersofficial.com/wp-content/themes/allegiant/style.css?ver=5.2.3",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
