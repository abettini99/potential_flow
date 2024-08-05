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
from src.pages.tat import tat
from src.pages.panel import panel
from src.plots.plotUniform import plotUniform
from src.plots.plotSource import plotSource
from src.plots.plotDoublet import plotDoublet
from src.plots.plotVortex import plotVortex
from src.plots.plotSourceUniform import plotSourceUniform
from src.plots.plotRankine import plotRankine
from src.plots.plotCylinder import plotCylinder
from src.plots.plotRotatingCylinder import plotRotatingCylinder

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
        html.H1(f"AE2130-I", style={'fontSize': '36px', 'fontWeight': 'bold'}),
        html.H2(f"Aerodynamics 1", className="lead", style={'fontSize' : '28px'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home",            href="/",              active="exact"),
                dbc.NavLink("Preliminaries",   href="/preliminaries", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.H3(f"Fundamental Theory", className="lead", style={'fontSize' : '24px'}),
        dbc.Nav(
            [
                dbc.NavLink("Navier-Stokes",   href="/ns",             active="exact"),
                dbc.NavLink("Potential Flow",  href="/potential-flow", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.H3(f"Building Blocks", className="lead", style={'fontSize' : '24px'}),
        dbc.Nav(
            [
                dbc.NavLink("Uniform Flows",  href="/uniform", active="exact"),
                dbc.NavLink("Source Flows",   href="/source",  active="exact"),
                dbc.NavLink("Doublets",       href="/doublet",  active="exact"),
                dbc.NavLink("Vortex Flows",   href="/vortex",  active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.H3(f"Airfoil Analysis", className="lead", style={'fontSize' : '24px'}),
        dbc.Nav(
            [
                dbc.NavLink("Thin Airfoil Theory", href="/tat",   active="exact"),
                dbc.NavLink("Panel Method",        href="/panel", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.H3(f"Wing Analysis", className="lead", style={'fontSize' : '24px'}),
        dbc.Nav(
            [
                dbc.NavLink("TBD", href="/tbd", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

#### ==== ####
#### MAIN ####
#### ==== ####
app        = dash.Dash(__name__,
                       external_stylesheets=[dbc.themes.BOOTSTRAP],
                       suppress_callback_exceptions=True)
content    = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"),
                       sidebar,
                       content])

#### ============= ####
#### app CALLABLES ####
#### ============= ####
## ALL CALLABLES GO IN THIS FILE, AS THEY REQUIRE THE app OBJECT.

## ------------------------- ##
## App callable for main app ##
## ------------------------- ##
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
    elif pathname == f"/tat":
        return tat()
    elif pathname == f"/panel":
        return panel()

## ------------------------------ ##
## App callables for uniform page ##
## ------------------------------ ##
@app.callback(Output('uniformV','figure'),
              Output('uniformPS','figure'),
              Input('VelInfMag','value'),
              Input('VelInfTheta','value')
             )
def updateUniformFigure(VelInfMag, VelInfTheta):
    return plotUniform([-1,1], [-1,1], VelInfMag, VelInfTheta)

## ----------------------------- ##
## App callables for source page ##
## ----------------------------- ##
@app.callback(Output('sourceV','figure'),
              Output('sourcePS','figure'),
              Input('Px','value'),
              Input('Py','value'),
              Input('sourceStrength1','value')
             )
def updateSourceFigure(Px, Py, Lambda):
    return plotSource([-1,1], [-1,1], [Px,Py], Lambda)

@app.callback(Output('sourceuniformV','figure'),
              Output('sourceuniformPS','figure'),
              Output('sourceuniformVelS','figure'),
              Output('sourceuniformCpS','figure'),
              Input('sourceStrength2','value'),
              Input('VelInfMagSourceUniform','value')
             )
def updateSourceUniformFigure(Lambda, VelInfMag):
    return plotSourceUniform([-1,1], [-1,1], Lambda, VelInfMag)

@app.callback(Output('rankineV','figure'),
              Output('rankinePS','figure'),
              Output('rankineVelS','figure'),
              Output('rankineCpS','figure'),
              Input('rankineStrength','value'),
              Input('rankineVelInfMag','value'),
              Input('rankineSeparation','value')
             )
def updateRankineFigure(Vinf, Lambda, b):
    return plotRankine([-1,1], [-1,1], Lambda, Vinf, b)

## ------------------------------ ##
## App callables for doublet page ##
## ------------------------------ ##
@app.callback(Output('doubletV','figure'),
              Output('doubletPS','figure'),
              Input('doubletStrength','value')
             )
def updateDoubletFigure(kappa):
    return plotDoublet([-1,1], [-1,1], kappa)

@app.callback(Output('cylinderV','figure'),
              Output('cylinderPS','figure'),
              Output('cylinderVelS','figure'),
              Output('cylinderCpS','figure'),
              Input('cylinderVinfmag','value'),
              Input('cylinderRadius','value')
             )
def updateCylinderFigure(Vinf, radius):
    return plotCylinder([-1,1], [-1,1], Vinf, radius)

## ----------------------------- ##
## App callables for vortex page ##
## ----------------------------- ##
@app.callback(Output('vortexV','figure'),
              Output('vortexPS','figure'),
              Input('vortexStrength','value')
             )
def updateVortexFigure(Gamma):
    return plotVortex([-1,1], [-1,1], Gamma)

@app.callback(Output('rcylinderV','figure'),
              Output('rcylinderPS','figure'),
              Output('rcylinderVelS','figure'),
              Output('rcylinderCpS','figure'),
              Input('rcylinderVinfmag','value'),
              Input('rcylinderRadius','value'),
              Input('rcylinderVortex','value')
             )
def updateRotatingCylinderFigure(Vinf, radius, Gamma):
    return plotRotatingCylinder([-1,1], [-1,1], Vinf, radius, Gamma)

## ----------------------------------- ##
## App callables for panel method page ##
## ----------------------------------- ##

if __name__ == '__main__':
    app.run_server(debug=True)
