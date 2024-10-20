#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors:       A. Bettini
Last Modified: 2024-08-12

Incompressible flow visualizer.
Utilizes dash for user interface, whereas plotly is used for plotting.

Second version of the code.
"""
## Import libraries
import dash
from dash import html, dcc
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from src.pages.home import home
from src.pages.preliminaries import preliminaries
from src.pages.NavierStokes import NavierStokes
from src.pages.potentialFlow import potentialFlowTheory
from src.pages.uniform import uniform
from src.pages.source import source
from src.pages.doublet import doublet
from src.pages.vortex import vortex
from src.pages.tat import tat
from src.pages.panel import panel
from src.pages.liftline import liftline
from src.pages.numliftline import numliftline
from src.pages.vortfil import vortfil
from src.pages.vortfil import VortexFilament
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
    "boxShadow"       : "5px 5px 5px 5px lightgrey",
    "overflow"        : "scroll"
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
                dbc.NavLink("Navier-Stokes",   href="/ns",       active="exact"),
                dbc.NavLink("Potential Flow",  href="/pot-flow", active="exact"),
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
                dbc.NavLink("Doublets",       href="/doublet", active="exact"),
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
                dbc.NavLink("Vortex filaments", href="/vortfil", active="exact"),
                dbc.NavLink("Lifting line theory", href="/liftline", active="exact"),
                dbc.NavLink("Numerical lifting line", href="/numliftline", active="exact"),
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
server     = app.server # Added so that the app can be served using waitress.

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
    elif pathname == f"/preliminaries":
        return preliminaries()
    elif pathname == f"/ns":
        return NavierStokes()
    elif pathname == f"/pot-flow":
        return potentialFlowTheory()
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
    elif pathname == f"/vortfil":
        return vortfil()
    elif pathname == f"/liftline":
        return liftline()
    elif pathname == f"/numliftline":
        return numliftline()

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
@app.callback(
    Output('vort', 'figure'),
    Output('filam-store', 'data'),  # Store the Filam object
    Output('transform-store', 'data'),  # Store the transformation matrix
    Input('draw-button', 'n_clicks'),  # Trigger based on the draw button click
    Input('split-button', 'n_clicks'),  # Trigger based on the split button click
    State('x_point_intercept', 'value'),  # Capture the current values but do not trigger on change
    State('y_point_intercept', 'value'),
    State('VortexStrength', 'value'),
    State('VortexAngle', 'value'),
    State('selected-point-output', 'children'),
    State('angle_1', 'value'),
    State('angle_2', 'value'),
    State('filam-store', 'data')  # Get the current stored Filam object
)
def handle_vortex_operations(draw_clicks, split_clicks, x, y, Gamma, theta, selected_point, angle_1, angle_2, data):
    # Determine if we are drawing a new vortex or splitting the existing one
    roll_angle = -np.deg2rad(60)
    pitch_angle = -np.deg2rad(20)
    roll_angle2 = np.deg2rad(5)

    roll_transform = np.array([[1,0,0],
                               [0,np.cos(roll_angle),-np.sin(roll_angle)],
                               [0,np.sin(roll_angle),np.cos(roll_angle)]])
    pitch_transform = np.array([[np.cos(pitch_angle),0,np.sin(pitch_angle)],
                                [0,1,0],
                                [-np.sin(pitch_angle),0,np.cos(pitch_angle)]])

    transform = np.dot(pitch_transform, roll_transform)

    roll_transform2 = np.array([[1,0,0],[0,np.cos(roll_angle2),-np.sin(roll_angle2)],[0,np.sin(roll_angle2),np.cos(roll_angle2)]])
    transform = np.dot(roll_transform2,transform)

    transform_store = transform.tolist()
    

    ctx = dash.callback_context
    if not ctx.triggered:
        # If nothing has triggered the callback yet, return empty figure and no change in data
        return go.Figure(), data, transform_store

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'draw-button' and draw_clicks:
        # Drawing the vortex filament
        vec = np.array([np.sin(np.deg2rad(theta)), np.cos(np.deg2rad(theta)), 0])
        Filam = VortexFilament(Gamma, [x, y, 0], vec)
        Filam_dict = Filam.to_dict()
        return Filam.draw_vortex_family([-2.1, 2.1], [-2, 2], transform=transform), Filam_dict, transform_store

    elif button_id == 'split-button' and split_clicks:
        # Splitting the vortex filament
        if data is None:
            # No existing vortex filament data
            return go.Figure(), data

        # Extract the selected point's x and y coordinates from the text
        selected_x = float(selected_point.split(',')[0].split('=')[1])
        selected_y = float(selected_point.split(',')[1].split('=')[1])

        # Recreate the Filam object from the stored data
        Filam = VortexFilament.from_dict(data)

        # Split the vortex filament at the selected point
        Filam.split([0.9, 0.1], [selected_x, selected_y, 0], [angle_1, angle_2])

        Filam_dict = Filam.to_dict()
        return Filam.draw_vortex_family([-2.1, 2.1], [-2, 2], transform=transform), Filam_dict, transform_store

    # If no valid action, return the same data and figure
    return go.Figure(), data, transform_store

@app.callback(
    Output('selected-point-output', 'children'),  # Display the clicked point
    Input('vort', 'clickData'),  # Capture click events on the graph
    Input('transform-store', 'data')
)
def display_selected_data(clickData, transform):
    if clickData is None:
        return "Click on a point on the graph to select it."

    transform = np.array(transform)[:2,:2]
    transform = np.linalg.inv(transform)

    # Extract the selected point's x and y coordinates from clickData
    selected_x = clickData['points'][0]['x']
    selected_y = clickData['points'][0]['y']


    selected_point = np.array([selected_x, selected_y])

    selected_point = np.dot(transform, selected_point)
    selected_x = selected_point[0]
    selected_y = selected_point[1]
    
    # You can now use selected_x and selected_y for further processing
    return f"Selected Point: x = {selected_x:.2f}, y = {selected_y:.2f}"


    

## ----------------------------------- ##
## App callables for panel method page ##
## ----------------------------------- ##

## =================== ##
## Main code execution ##
## =================== ##
if __name__ == '__main__':
    ## For DEBUG
    # app.run_server(debug=True)

    ## For PROD
    app.run_server(debug=False)
