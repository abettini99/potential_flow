import dash
import numpy as np
from dash import html, dcc
import dash_bootstrap_components as dbc

def preliminaries():
    return html.Div(children=[
        
    html.H1("Preliminaries"),
    dcc.Markdown(r"""

    Before diving into the different components of this app, make sure you have read Chapter 1, 2 and 3 of _Fundamentals of Aerodynamics_ by John D. Anderson.
    Alternately, you can also check out the course slides. Chapter 3 covers the fundamentals about **Inviscid** and **Incompressible** flows, which is at the heart of the features of this app.
    This essentially means, that friction related phenomena and changes in the density of the fluid are neglected. Some fundamental concepts to be known before going further are some coefficients,
    for 3D bodies and airfoils (capital letters relate to 3D bodies and ' indicates per unit length).  

    **Lift Coefficient**
    $$
    C_{L} = \frac{L}{q_{\infty} S} \quad c_{l} = \frac{L'}{q_{\infty} c}\\, 
    $$

    **Drag Coefficient**
    $$
    C_{D} = \frac{D}{q_{\infty} S} \quad c_{d} = \frac{D'}{q_{\infty} c}\\,
    $$

    **Moment Coefficient**
    $$
    C_{M} = \frac{M}{q_{\infty} S l} \quad c_{l} = \frac{L'}{q_{\infty} c^{2}}\\,
    $$

    where $$S$$ and $$l$$ are a reference area and length while $$q_{\infty}$$ is the dynamic pressure, defined as

    $$
    q_{\infty} = \frac{1}{2} \rho_{\infty} V^{2}_{\infty}\\.
    $$
    
    Finally, another useful coefficient is one which relates the pressure difference between a certain point and the freestream, called the pressure coefficient and given by

    $$
    C_{p} = \frac{p - p_{\infty}}{q_{\infty}}\\.
    $$

    """, mathjax=True)
    ])