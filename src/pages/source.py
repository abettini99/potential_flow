import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def source():
    return html.Div(children=[
    
    #### ============== ####
    #### BUILDING BLOCK ####
    #### ============== ####
    html.H1("Source Flows"),

    dcc.Markdown(r'''
                 
    Source flow is defined as such that all its streamlines emanate from a central point and the velocity along them is inversely proportional to the distance from said center. This flow type
    is more conveniently defined in radial coordinates with $$V_{r}$$ being the radial velocity and $$V_{\theta}$$ the tangential velocity. The velocity potential and stream function are given by
                 
    $$
    \phi = \frac{\Lambda}{2 \pi} ln(r)\\, 
    $$

    $$
    \Psi = \frac{\Lambda \theta}{2 \pi}\\,
    $$
    and its velocity components are then
    $$
    V_{r} = \frac{\Lambda}{2 \pi r}\\,
    $$
    $$
    V_{\theta} = 0\\.
    $$

    The $$\Lambda$$ is called the source strength, and physically it represents the rate of volume flow from the source per unit depth perpendicular to the 2D plane, positive strength is called a source
    and a negative one is a sink. 
    
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
    html.H2("Application: Source + Uniform Flows"),

    dcc.Markdown(r'''
    We can combine our two current elementary flows and due to the linearity of Laplace's equation, it is still a valid solution. The resulting streamline shape resembles that of a semi-infinite body.
    Applying linearity, the velocity potential and stream function of this semi-infinite body in polar coordinates is
    $$
    \phi = \frac{\Lambda}{2 \pi} ln(r) + V_{\infty} r cos(\theta)\\,
    $$

    $$
    \Psi = \frac{\Lambda \theta}{2 \pi} + V_{\infty} r sin(\theta)\\,
    $$
    its velocity components are then
    $$
    V_{r} = \frac{\Lambda}{2 \pi r} + V_{\infty} cos(\theta)\\,
    $$
    $$
    V_{\theta} = -V_{\infty} sin(\theta)\\.
    $$
    
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


    dcc.Markdown(r'''
    Furthermore, by equating the velocity components to 0 we can find the stagnation points in the flow, as can be seen from the velocity field plots there is only one upstream of the source.
    The streamline which passes through this stagnation point is defined as a dividing streamline, since it separates the flow coming from the freestream to that from the source. If the flow inside of
    the semi-infinite body, contained by the dividing streamline, were to dissappear then the outer flow would remain the same, this allows us to model the shape defined by the dividing streamline
    as a physical body in the flow. This modelling approach is only possible with **Inviscid** flows, since they do not present the no-slip condition or 0 velocity magnitude at the body-flow boundary.
    For these flows, the only condition is that the flow is tangent at the body-flow boundary. We can then look at the flow properties along this semi-infinite body with the pressure coefficient
    and velocity components.

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
    html.H2("Application: Uniform + Source + Sink Flows (Rankine Oval)"),

    dcc.Markdown(r'''
    Finally, you might have thought of a way to make the previous semi-infinite body closed. Well, if we add a sink this time, at an equal distance d and strength $$\Lambda$$ from the origin as a source we
    obtain a closed body called the Rankine Oval, named after William J. M. Rankine who first solved this flow problem. The velocity potential and stream function of this flow field are

    $$
    \phi = \frac{\Lambda}{2 \pi} ln\left(\sqrt{d^{2} + r^{2} + 2rdcos(\theta)}\right) + \frac{-\Lambda}{2 \pi} ln\left(\sqrt{d^{2} + r^{2} - 2rdcos(\theta)}\right) + V_{\infty} r cos(\theta)\\,
    $$
    $$
    \Psi = V_{\infty} r sin(\theta) + \frac{\Lambda}{2 \pi} \left[ arctan\left( \frac{r sin(\theta)}{r cos(\theta) - d} \right) - arctan\left(\frac{r sin(\theta)}{r cos(\theta) + d} \right) \right],
    $$
    and its velocity components are
    $$
    V_{r} = V_{\infty}cos(\theta) + \frac{\Lambda}{2 \pi} \left(\frac{r + dcos(\theta)}{d^{2} + r^{2} + 2rdcos(\theta)} \right) - \frac{\Lambda}{2 \pi} \left(\frac{r - dcos(\theta)}{d^{2} + r^{2} - 2rdcos(\theta)} \right)\\,
    $$
    $$
    V_{\theta} = -V_{\infty}sin(\theta) - \frac{\Lambda}{2 \pi} \left(\frac{dsin(\theta)}{d^{2} + r^{2} + 2rdcos(\theta)} \right) + \frac{\Lambda}{2 \pi} \left(\frac{dsin(\theta)}{d^{2} + r^{2} - 2rdcos(\theta)} \right)\\.
    $$
    
    
    ''',mathjax=True),



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

    dcc.Markdown(r'''
    We can again use the same modelling aspect as before, the dividing streamline now goes from one stagnation point to the other and defines the Oval as the body. The flow properties over
    this body can also be investigated. 
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

