#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors:       A. Bettini
Last Modified: 2024-08-01

Incompressible flow visualizer.
Utilizes dash for user interface, whereas plotly is used for plotting.

Second version of the code.
"""
## Import libraries
import dash
from dash import html, dcc
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from src.pages.home import home
from src.pages.uniform import uniform
from src.pages.source import source
from src.pages.doublet import doublet
from src.pages.vortex import vortex
from src.pages.cylinder import cylinder
from src.pages.panel import panel

SIDEBAR_STYLE = {
    "position"        : "fixed",
    "top"             : 0,
    "left"            : 0,
    "bottom"          : 0,
    "width"           : "12em",
    "padding"         : "2rem 1rem",
    "backgroundColor" : "#2b2b2b",
    "color"           : "#cfcfcf",
    "fontSize"        : "23px",
    "boxShadow"       : "5px 5px 5px 5px lightgrey"
}

CONTENT_STYLE = {
    "marginLeft"  : "18rem",
    "marginRight" : "2rem",
    "padding"     : "2rem 1rem"
}

sidebar = html.Div([
        html.H1(f"Main Header", style={'fontSize': '36px', 'fontWeight': 'bold'}),
        html.Hr(),
        html.H2(f"Sub Header", className="lead", style={'fontSize' : '28px'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home",     href="/",         active="exact"),
                dbc.NavLink("Uniform",  href="/uniform",  active="exact"),
                dbc.NavLink("Source",   href="/source",   active="exact"),
                dbc.NavLink("Doublet",  href="/doublet",  active="exact"),
                dbc.NavLink("Vortex",   href="/vortex",   active="exact"),
                dbc.NavLink("Cylinder", href="/cylinder", active="exact"),
                dbc.NavLink("Panel M.", href="/panel",    active="exact"),
            ],
            vertical=True,
            pills=True,
        )
    ],
    style=SIDEBAR_STYLE,
)

#### =========== ####
#### Application ####
#### =========== ####
app        = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
content    = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"),
                       sidebar,
                       content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if   pathname == f"/":
        return home() 
    elif pathname == f"/uniform":
        return uniform() 
    elif pathname == f"/source":
        return source() 
    elif pathname == f"/doublet":
        return doublet()
    elif pathname == f"/vortex":
        return vortex()
    elif pathname == f"/cylinder":
        return cylinder()
    elif pathname == f"/panel":
        return panel()

if __name__ == '__main__':
    app.run_server(debug=True)
