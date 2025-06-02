from dash import html

def create_navbar():
    return html.Ul(
        children=[
            html.Li([html.A("HOME", href="/")], className="nav-item"),
            html.Li([html.A("MATCH", href="/match")], className="nav-item"),
            html.Li([html.A("SEASON", href="/season")], className="nav-item"),
            html.Li([html.A("ALLTIME", href="/alltime")], className="nav-item")
        ],
        className="nav nav-tabs nav-justified"
    )


# CREATE FOOTER FOR TESTING PURPOSES
def create_footer():
    return html.Footer(
        children=[
            html.P("© 2024 IPL Dashboard", className="text-center"),
            html.P("Created by Sayan Basu", className="text-center")
        ],
        className="footer"
    )


# On scrolling down, the scorecard tables are displayed on top of nav bar.