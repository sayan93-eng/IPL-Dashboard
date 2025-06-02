import dash_bootstrap_components as dbc

homepage_carousel = dbc.Carousel(
    items=[
        {"key": "1", "src": "/assets/images/bar_plot_1.png", "alt":"First Slide", "header":" Bar Plot", "caption":"Innings Progression: Royal Challengers Bangalore"},
        {"key": "2", "src": "/assets/images/bar_plot_2.png", "alt":"Second Slide", "header":" Bar Plot", "caption":"Innings Progression: Rajasthan Royals"},
        {"key": "3", "src": "/assets/images/line_plot_1.png", "alt":"Third Slide", "header":" Line Plot", "caption":"Royal Challengers Bangalore VS Rajasthan Royals"},
        {"key": "4", "src": "/assets/images/line_plot_2.png", "alt":"Fourth Slide", "header":" Line Plot", "caption":"Chennai Super Kings VS Sunrisers Hyderabad"},
        {"key": "5", "src": "/assets/images/pie_chart_1.png", "alt":"Fifth Slide", "header":" Pie Chart", "caption":"Runs Distribution: Chennai Super Kings"},

    ],
    className="carousel-fade",
    controls=True,
    indicators=True,
    interval=2000
)