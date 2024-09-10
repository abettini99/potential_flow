import dash
import numpy as np
from dash import html, dcc
import dash_bootstrap_components as dbc

def NavierStokes():
    return html.Div(children=[
        
    #### ================== ####
    #### FUNDAMENTAL THEORY ####
    #### ================== ####
    html.H1("Navier-Stokes Equations"),

    dcc.Markdown(r'''
                 
    The Navier-Stokes equations are a set of partial differential equations, originally named after Claude-Louis Navier and George Gabriel Stokes.
    They describe the conservation of mass, momentum, and energy for a **Compressible** and **Viscous** fluid.

    In Chapter 2 of _Fundamentals of Aerodynamics_ or the relevant course slides, a preliminary derivation is made. The terms related to viscous forces
    and viscous energy phenomena are not derived, and these remain out of the scope of this course and bachelor curriculum. This set of equations can be seen below.

    **Mass Conservation**              
    $$
    \frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{V}) = 0
    $$
    **Momentum Conservation**
    $$
    \rho \frac{\partial u}{\partial t} + \rho u \frac{\partial u}{\partial x} + \rho v \frac{\partial u}{\partial y} + \rho w \frac{\partial u}{\partial z} = -\frac{\partial p}{\partial x} + \rho f_{x} + F_{x-viscous} 
    $$
    $$
    \rho \frac{\partial v}{\partial t} + \rho u \frac{\partial v}{\partial x} + \rho v \frac{\partial v}{\partial y} + \rho w \frac{\partial v}{\partial z} = -\frac{\partial p}{\partial y} + \rho f_{y} + F_{y-viscous}    
    $$
    $$
    \rho \frac{\partial w}{\partial t} + \rho u \frac{\partial w}{\partial x} + \rho v \frac{\partial w}{\partial y} + \rho w \frac{\partial w}{\partial z} = -\frac{\partial p}{\partial z} + \rho f_{z} + F_{z-viscous}
    $$
    **Energy Conservation**
    $$
    \frac{\partial}{\partial t} \left[\rho \left(e + \frac{V^2}{2} \right) \right] + \nabla \cdot \left[ \rho \left(e + \frac{V^{2}}{2} \right) \mathbf{V} \right] = \rho \dot{q}  - \nabla \cdot \left(p \mathbf{V} \right) + \rho (\mathbf{f} \cdot \mathbf{V} ) + \dot{Q^{'}_{viscous}} + \dot{W^{'}_{viscous}}
    $$
    ''',mathjax=True)])