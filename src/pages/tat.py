import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def tat():
    return html.Div(children=[
    
    html.H1("Thin Airfoil Theory"),

    dcc.Markdown("""
    This page is work in progress.
    
    """, mathjax=True)])