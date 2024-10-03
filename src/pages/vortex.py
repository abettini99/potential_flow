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

    dcc.Markdown(r'''
    Our final elementary flow is vortex flow, it is essentially the opposite of source flow. It is defined as having streamlines which are concentric circles around a center, where each streamline
    has a constant velocity but its value between streamlines is inversely proportional to the distance from the center. Its velocity potential and stream function are     

    $$
    \phi = -\frac{\Gamma}{2 \pi} \theta\\.
    $$
    $$
    \Psi = \frac{\Gamma}{2 \pi} ln(r)\\,
    $$
    Here, $$\Gamma$$ is defined as the vortex strength, being the value of the circulation along any streamline of a vortex flow. Its velocity components are
    $$
    V_{r} = 0\\,
    $$
    $$
    V_{\theta} = -\frac{\Gamma}{2\pi r}\\.
    $$

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
    html.H2("Application: Uniform + Doublet + Vortex Flows (Rotating and Lifting Cylinder Flow)"),

    dcc.Markdown(r'''
    Similarly to doublets, we can add a vortex flow to the non-lifting flow around a cylinder and obtain a new type of streamline pattern where the flow is not double symmetric around the
    cylinder's axis. Intuitively, it will still result in zero drag due to it being symmetric along the vertical axis, but a finite value of normal or lifting force is there due to the
    unsymmetrical flow along the horizontal axis. This type of flow around a cylinder is observed in real life when the cylinder is rotating, in general it is called the Magnus effect and
    it explains how baseball or tennis balls curve in the air and it can be even be utilized to power sails for ships. The velocity potential and stream function are 

    $$
    \phi = \left(1 + \frac{R^{2}}{r^{2}} \right) V_{\infty} r cos(\theta) - \frac{\Gamma}{2 \pi} \theta\\,
    $$
    $$
    \Psi = \left(V_{\infty} r sin(\theta) \right) \left(1 - \frac{R^{2}}{r^{2}} \right) + \frac{\Gamma}{2 \pi} ln\left(\frac{r}{R} \right)\\,
    $$
    and its velocity components
    $$
    V_{r} = \left(1 - \frac{R^{2}}{r^{2}} \right) V_{\infty} cos(\theta)\\,
    $$
    $$
    V_{\theta} = -\left(1 + \frac{R^{2}}{r^{2}} \right) V_{\infty} sin(\theta) - \frac{\Gamma}{2 \pi r}\\.
    $$
    It can also be noted that depending on the value of circulation, the location of the stagnation points will change. Three different streamlines pattern can arise, see if you can find
    them yourself. 

    ''',mathjax=True),

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

    dcc.Markdown(r'''
    Finally, we can again look at the flow properties along the cylinder's boundary. Additionally, we can analytically calculate the value of the lift per unit length acting on the cylinder
    due to this unsymmetrical flow pattern, by using the expression from Chapter 1 of _Fundamentals of Aerodynamics_ we have

    $$
    L^{'} = \frac{1}{2} \rho_{\infty} V^{2}_{\infty} S c_{l} = \frac{1}{2} \rho_{\infty} V^{2}_{\infty} S \left[ -\frac{1}{2} \int_{0}^{2 \pi} C_{p} sin(\theta) \, d\theta \right] = \rho_{\infty} V_{\infty} \Gamma
    $$

    This is the expression for the lift acting on the cylinder, it is directly related to the circulation and it connects to a more general theorem about the lift over arbitrary bodies called
    the Kutta-Joukowski theorem. 
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
