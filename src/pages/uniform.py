import dash
import numpy as np
from dash import html, dcc
import dash_bootstrap_components as dbc

def uniform():
    return html.Div(children=[
        
    #### ============== ####
    #### BUILDING BLOCK ####
    #### ============== ####
    html.H1("Uniform Flow"),

    dcc.Markdown('''
    \\[...\\] \n
                 
    Very simple
                 
    $$
    V_x = V_{\\infty} \\cos{\\theta_{\\infty}}\\,,
    $$
    $$
    V_y = V_{\\infty} \\sin{\\theta_{\\infty}}\\,.
    $$

    Which as a set of cartesian velocities can be found by      
    EXAMPLE TEXT: \n
    bla bla bla
    ''',mathjax=True),

    html.Label('Freestream Speed Slider:'),
    dcc.Slider(0.1, 2,
               value=1,
               id='VelInfMag',
              ),
    html.Label('Freestream Angle Slider:'),
    dcc.Slider(-np.pi, np.pi,
               value=0,
               id='VelInfTheta',
               marks={-np.pi: {'label': '-𝜋'},
                           0: {'label': '0'},
                       np.pi: {'label': '𝜋'}}
              ),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='uniformV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='uniformPS', mathjax=True),
        ], width=4)
    ], justify='center'),

    ])
