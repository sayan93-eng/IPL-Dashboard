"""
Homepage will be a dash app with the same nav as the other apps.
"""
import os
import dash

from dash import html
from dash.dependencies import Input, Output
from src.components.navbar import create_navbar, create_footer
from src.components.styles import PAGE_CONTAINER_STYLE
from src.components.carousel import homepage_carousel

app = dash.Dash(
    __name__,
    url_base_pathname='/',
    assets_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'),
    external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css'],
)

app.layout = html.Div(children=[

    html.Div([
        create_navbar()
    ], className='navbar'),

    html.Div([
        html.Div([

            html.H1("IPL Statistics Dashboard")   
            ], className='row text-center my-4 mx-auto'),

            html.Div([
                html.P([
                    "The IPL Statistics Dashboard serves as a comprehensive analytics portal for Indian Premier League cricket data spanning from 2008 to 2024. The modern interface features a responsive navigation system and a dynamic carousel showcasing key IPL moments. Our upcoming features include advanced match statistics with in-depth innings summaries and partnership analysis, detailed player analysis with head-to-head statistics and form predictions, and comprehensive venue analysis with historical performance metrics and score prediction models."
                ], style={
                    'margin':'0',
                    'line-height':'1.5'
                })
            ], className='row my-4 mx-auto', style={
                'backgroundColor' :'black',
                'color':'white',
                'padding': '20px'
            }),

            html.Div([
                homepage_carousel
            ], className='row my-5 mx-auto', style={
                'padding':'20px',
                'borderRadius':'10px',
                'boxShadow': '0 -0 10px #24d5ec, 0 0 10px #24d5ec',
                'backgroundColor' : 'black'
            }), 

    ], className='container-fluid' , style=PAGE_CONTAINER_STYLE),

    html.Div([
        create_footer()
    ], className='footer')

], className='wrapper')


if __name__ == '__main__':
    app.run(debug=True)