import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def doublet():
    return html.Div(children=[
    
    #### ============== ####
    #### BUILDING BLOCK ####
    #### ============== ####
    html.H1("Doublets"),

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

    html.Label('Doublet Strength Slider:'),
    dcc.Slider(-2, 2,
               value=1,
               id='doubletStrength',
              ),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='doubletV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='doubletPS', mathjax=True),
        ], width=4)
    ], justify='center'),

    #### =========== ####
    #### APPLICATION ####
    #### =========== ####
    html.Hr(),
    html.H2("Application: Uniform + Doublet (Cylinder Flow)"),

    html.Label('Freestream Velocity Slider:'),
    dcc.Slider(0.1, 2,
               value=1,
               id='cylinderVinfmag',
              ),
    html.Label('Cylinder Radius Slider:'),
    dcc.Slider(0, 0.5,
               value=0.5,
               id='cylinderRadius',
              ),
    
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='cylinderV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='cylinderPS', mathjax=True),
        ], width=4)
    ], justify='center'),

    dcc.Markdown('''
    We can also look at quantities over the body contour...
    ''',mathjax=True),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='cylinderVelS', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='cylinderCpS', mathjax=True),
        ], width=6)
    ], justify='center'),

    ])
