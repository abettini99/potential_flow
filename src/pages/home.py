import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def home():
    return html.Div(children=[
    
    html.H1("Welcome!"),

    dcc.Markdown("""

    This is a support app for the course Aerodynamics I. Here you can visualize the elementary flows of Potential Flow Theory and learn about the final outcomes of this theory, the analysis of arbitrary airfoils and wings. Feel free to explore each section.
    """)
    ])
