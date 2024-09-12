import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def doublet():
    return html.Div(children=[
    
    #### ============== ####
    #### BUILDING BLOCK ####
    #### ============== ####
    html.H1("Doublets"),

    dcc.Markdown(r'''
    A special case occurs when we have a source and sink pair of strengths $$\Lambda$$ and separated by a distance $$l$$, if we let $$l \rightarrow 0$$ while $$l \Lambda = const$$ we then
    obtain a streamline pattern called a Doublet of strength $$\kappa = l \Lambda$$. The resulting streamline pattern are a family of circles on either side of the line which originally joined
    the source-sink pair and the relative position of these two elements also determines the direction of the doublet's flow, this is indicated by an arrow from the sink to the source. The
    velocity potential and stream function of a doublet are

    $$
    \phi = \frac{\kappa}{2 \pi} \frac{cos(\theta)}{r}\\,
    $$

    $$
    \Psi = -\frac{\kappa}{2 \pi} \frac{sin(\theta)}{r}\\,
    $$
    from which we can obtain the velocity components
    $$
    V_{r} = -\frac{\kappa}{2 \pi} \frac{cos(\theta)}{r^{2}}\\,
    $$
    $$
    V_{theta} = -\frac{\kappa}{2 \pi} \frac{sin(\theta)}{r^{2}}\\.
    $$
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
    html.H2("Application: Uniform + Doublet Flows (Non-lifting Cylinder Flow)"),

    dcc.Markdown(r'''
    In the previous section, you may have noticed that by reducing the source-sink pair separation and manipulating some settings you could turn the Rankine oval into a shape closely resembling
    a circle. Well, since the doublet is the limiting case of a source-sink pair superimposed, combining it with a uniform flow yields a streamline pattern which is essentially a circle or a cylinder
    section. The dividing streamline again traverses from one stagnation point to the other and the velocity potential and stream function expressions are

    $$
    \phi = \frac{\kappa}{2 \pi} \frac{cos(\theta)}{r} + V_{\infty} r cos(\theta)\\,
    $$
    $$
    \Psi = -\frac{\kappa}{2 \pi} \frac{sin(\theta)}{r} + V_{\infty} r sin(\theta)\\,
    $$
    from which we can obtain the velocity components in which the radius of the cylinder can be found to be $$R = \sqrt{\frac{\kappa}{2 \pi V_{\infty}}}$$
    $$
    V_{r} = V_{\infty}cos(\theta) \left(1 - \frac{\kappa}{2 \pi V_{\infty} r^{2}} \right) = V_{\infty}cos(\theta) \left(1 - \frac{R^{2}}{r^{2}} \right)\\,
    $$
    $$
    V_{\theta} = -V_{\infty}sin(\theta) \left(1 + \frac{\kappa}{2 \pi V_{\infty} r^{2}} \right) = -V_{\infty}sin(\theta) \left(1 + \frac{R^{2}}{r^{2}} \right)\\.
    $$

    ''',mathjax=True),


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

    dcc.Markdown(r'''
    We can again look at the flow properties along the cylinder's boundary. Do note that due to the double symmetry that this flow presents with respect to the axis with origin at the center of the cylinder
    there is neither a lift nor a drag force which acts upon it. 
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
