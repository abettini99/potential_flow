import dash
import numpy as np
from dash import html, dcc
import dash_bootstrap_components as dbc

def potentialFlowTheory():
    return html.Div(children=[
        
    #### ================== ####
    #### FUNDAMENTAL THEORY ####
    #### ================== ####
    html.H1("Potential Flow Theory"),

    dcc.Markdown(r'''
                 
    Potential Flows describe a type of **Inviscid** fluid which present zero vorticity at each point $$\nabla \times \mathbf{V} = 0$$, thus it presents an irrotational velocity field.
    Using the vector identity $$\nabla \times (\nabla \phi) = 0$$ allows us to define the velocity field in terms of the gradient of a scalar function $$\phi$$ called the **Velocity Potential**.
    This **Velocity Potential** is a function of spatial coordinates, such as (x, y, z), and from the definition of the gradient it can be used to obtain the velocity field components as

    $$
    u = \frac{\partial \phi}{\partial x}\\,
    $$
    $$
    v = \frac{\partial \phi}{\partial y}\\,
    $$
    $$
    w = \frac{\partial \phi}{\partial z}\\.
    $$
    
    This definition is useful, since only one function must be defined to obtain all the flow field's velocity components. Additionally, when the flow is **Incompresible** $$\nabla \cdot \mathbf{V} = 0$$
    the governing equations reduce to a single linear second order partial differential equation called Laplace's equation. This governing equation can be expressed in terms of
    the **Velocity Potential** in the form $$\nabla^{2} \phi = 0$$, its linearity and simplicity allows exact and analytical solutions to be derived and then combined as
    linear combinations to describe more complex flow fields. Finally, this function is akin to, for example, gravitational potential and lines of constant velocity potential are also called
    equipotential lines.

    Additionally, another useful function which can be used similarly is the stream function $$\psi$$, however it is limited to **2D** flows only. Essentially, it is a function which describes
    all the streamlines (lines whose direction is tangent to the local velocity vector) of a flow field and individual streamlines are denoted by a certain constant. This comes from the fact that
    the differential equation of a streamline $$\frac{dy}{dx} = \frac{v}{u}$$ allows to be integrated if $$v$$ and $$u$$ are functions of the spatial coordinates, the function $$f$$ which this
    integration yields is the stream function $$\psi$$. These constants are also defined in such a way that their difference represents the mass flow between the two streamlines. From this fact, we
    can also obtain a relationships between the stream function and the flow field velocity components as

    $$
    \rho u = \frac{\partial \psi}{\partial y}\\,
    $$
    $$
    \rho v = -\frac{\partial \psi}{\partial x}\\.
    $$

    Furthermore, if we can assume that the flow is **incompressible** then we obtain a new stream function $$\Psi = \psi / \rho$$ from which the velocity components can be equally obtained. In this case
    the difference between the constants representing the streamlines are now the volume flow between them. 

    $$
    u = \frac{\partial \Psi}{\partial y}
    $$
    $$
    v = -\frac{\partial \Psi}{\partial x}
    $$

    An interesting relationship between these two functions is that lines of constant potential (equipotential lines) and lines of constant stream function (streamlines) are mutually perpendicular
    to each other. Finally, while potential flow may seem restrictive due to its assumptions, it has proven to be quite valuable in aircraft design. For flows outside of the boundary layer, it
    results in predictions which are close enough to the Navier-Stokes equations and allows for the preliminary analysis of airfoils and wings, or even complete bodies, in flows where compressibility
    is negligible (M < 0.3). 
    
    Some common 2D elementary potential flows are available to be used in this app and some examples of airfoil and wing analysis. For more information about the theory take a look at Chapter 3 of _Fundamentals of Aerodynamics_ or the relevant
    course slides. Finally, you will study **Compressible** potential flows in the Aerodynamics II course. 

   
    ''',mathjax=True)])