import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def source():
    return html.Div(children=[
    
    #### ============== ####
    #### BUILDING BLOCK ####
    #### ============== ####
    html.H1("Source Flows"),

    dcc.Markdown('''
    \\[...\\] \n
                 
    The velocity around a source/sink is then given by
                 
    $$
    V_r = \\frac{\\Lambda}{2\\pi r}\\,,
    $$
    $$
    V_\\theta = 0\\,.
    $$

    Which as a set of cartesian velocities can be found by      
    EXAMPLE TEXT: \n
    bla bla bla
    ''',mathjax=True),

    html.Label('Strength Slider:'),
    dcc.Slider(-2, 2,
               value=1,
               id='sourceStrength1',
              ),

    html.Label('Source Position:'),
    dcc.Slider(-1, 1,
               value=0,
               id='Px',
               marks={-1: {'label': '-1'},
                       0: {'label': '0'},
                       1: {'label': '1'}}
              ),
    dcc.Slider(-1, 1,
               value=0,
               id='Py',
               marks={-1: {'label': '-1'},
                       0: {'label': '0'},
                       1: {'label': '1'}}
              ),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourcePS', mathjax=True),
        ], width=4)
    ], justify='center'),
    


    #### ============= ####
    #### APPLICATION 1 ####
    #### ============= ####
    html.Hr(),
    html.H2("Application: Source + Uniform"),

    dcc.Markdown('''
    bla bla bla bla bla, velocity graph 2
    ''',mathjax=True),
    

    html.Label('Source Strength Slider:'),
    dcc.Slider(0, 2,
               value=1,
               id='sourceStrength2',
              ),
    html.Label('Freestream Velocity Slider:'),
    dcc.Slider(0.1, 2,
               value=1,
               id='VelInfMagSourceUniform',
              ),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceuniformV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceuniformPS', mathjax=True),
        ], width=4)
    ], justify='center'),


    dcc.Markdown('''
    We can also look at quantities over the body contour...
    ''',mathjax=True),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceuniformVelS', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceuniformCpS', mathjax=True),
        ], width=6)
    ], justify='center'),



    #### ============= ####
    #### APPLICATION 2 ####
    #### ============= ####
    html.Hr(),
    html.H2("Application: Uniform + Source + Sink (Rankine Oval)"),

    html.Label('Rankine Strength Slider:'),
    dcc.Slider(0.1, 2,
               value=1,
               id='rankineStrength',
              ),
    html.Label('Freestream Velocity Slider:'),
    dcc.Slider(0.1, 2,
               value=1,
               id='rankineVelInfMag',
              ),
    html.Label('Source Sink Separation Slider:'),
    dcc.Slider(0.01, 1.5,
               value=1.0,
               id='rankineSeparation',
              ),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='rankineV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='rankinePS', mathjax=True),
        ], width=4)
    ], justify='center'),

    dcc.Markdown('''
    We can also look at quantities over the body contour...
    ''',mathjax=True),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='rankineVelS', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='rankineCpS', mathjax=True),
        ], width=6)
    ], justify='center'),

    ])

