import dash
import numpy as np
from dash import html, dcc
import dash_bootstrap_components as dbc

def vortex():
    return html.Div(children=[
    
    #### ============== ####
    #### BUILDING BLOCK ####
    #### ============== ####
    html.H1("Vortex Flows"),

    dcc.Markdown('''
    \\[...\\] \n
                 
    Very simple
                 
    $$
    V_x = \\cdots\\,,
    $$
    $$
    V_y = \\cdots\\,.
    $$

    Which as a set of cartesian velocities can be found by      
    EXAMPLE TEXT: \n
    bla bla bla
    ''',mathjax=True),

    html.Label('Vortex Strength Slider:'),
    dcc.Slider(-2, 2,
               value=1,
               id='vortexStrength',
              ),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='vortexV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='vortexPS', mathjax=True),
        ], width=4)
    ], justify='center'),

    #### =========== ####
    #### APPLICATION ####
    #### =========== ####
    html.Hr(),
    html.H2("Application: Uniform + Doublet + Vortex (Rotating Cylinder Flow)"),


    html.Label('Freestream Velocity Slider:'),
    dcc.Slider(0.1, 1,
               value=1,
               id='rcylinderVinfmag',
              ),
    html.Label('Cylinder Radius Slider:'),
    dcc.Slider(0.01, 0.5,
               value=0.5,
               id='rcylinderRadius',
              ),
    html.Label('Vortex Slider:'),
    dcc.Slider(0.01, 4*np.pi,
               value=2*np.pi,
               id='rcylinderVortex',
               marks={-0.01   : {'label': '0.01'},
                         np.pi: {'label':  '𝜋'},
                       2*np.pi: {'label': '2𝜋'},
                       3*np.pi: {'label': '3𝜋'},
                       4*np.pi: {'label': '4𝜋'}},
              ),
    
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='rcylinderV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='rcylinderPS', mathjax=True),
        ], width=4)
    ], justify='center'),

    dcc.Markdown('''
    We can also look at quantities over the body contour...
    ''',mathjax=True),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='rcylinderVelS', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='rcylinderCpS', mathjax=True),
        ], width=6)
    ], justify='center'),

    ])
