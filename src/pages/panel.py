import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def panel():
    return html.Div(children=[

    html.H1("Panel Methods"),
    dcc.Markdown("""
    
    This section will detail a **group of numerical methods** which can be used to obtain the **potential flow around arbitrary bodies**. For this, we return
    to the point in the previous section where we made the simplification of placing our vortex sheet on the camber line and then on the chord line for an airfoil. In this
    series of methods we will **cover the body in source, vortex or a combination of these sheets**. To make the computations tangible we will use a **discrete number of panels**
    wherein the condition of **flow tangency** or **zero normal flow** will be applied at certain control points, typically in the middle of each panel. 
    
    """, mathjax=True),

    html.Hr(),
    html.H2("Panel Geometry Definitions"),

    dcc.Markdown(r"""
    
    Before diving into the aerodynamic modelling itself, we must define how we organize our panels and the relevant geometrical features, as this will be used for all 
    upcoming methods. The panels are numbered in a **clock-wise** direction along the body, this ensures that the normal vector points out from the body. Each panel has **two boundary points**
    $$(XB, YB)$$ and **one control point** $$(XC, YC)$$ in the middle of the panel, it is also at this point from where the normal vector is defined. Subsequently, we will consider the case of a cylinder (circle in 2D), which is
    made by 8 panels. Below you can see the geometrical parameters related to one panel, highlighted as well on the body.  

    1. $$\varphi$$ is the angle from the positive x-axis to the inner side of the panel.
    
    2. $$\delta$$ is the angle from the positive x-axis to the normal vector.
                     
    3. $$\beta$$ is the angle between the freestream vector and the normal vector.
                
    4. $$\alpha$$ is the angle of attack of the freestream vector with respect to the x-axis.

    5. $$S$$ is the total length of the panel and $$s$$ will be a local 1D coordinate along the panel length.                   

    """, mathjax=True),


    html.Img(src="assets/panel_geometry.png",
            style={
                "width": "400px",  # Set desired width
                "height": "auto"  }),
    
    dcc.Markdown(r"""
    
    Finally, to calculate these geometrical parameters we can make the following observations:

    $$
    XC = \frac{XB_{i+1} + XB_{i}}{2}
    $$  
    $$
    YC = \frac{YB_{i+1} + YB_{i}}{2}
    $$                
    $$
    S = \sqrt{(XB_{i+1} - XB_{i})^{2} + (YB_{i+1} - YB_{i})^{2}}
    $$
    $$
    \varphi = arctan\left(\frac{YB_{i+1} - YB_{i}}{XB_{i+1} - XB_{i}}\right)
    $$
    $$                    
    \delta = \phi + \frac{\pi}{2}
    $$
    $$
    \beta = \delta - \alpha                     
    $$

    """, mathjax=True),
    
    html.Hr(),
    html.H2("Source Panel Method"),
    
        dcc.Markdown(r"""
  
    Now that the geometrical discussions are settled, we can proceed with the covering our body in source panels as a start. Note, that these **will not generate any lift** due to
    the lack of circulation from sources. We define a source sheet much like we did with the vortex sheet in the previous section, it has a strength per unit length of $$\gamma = \gamma (s)$$ and
    an infinitesimal portion of this sheet has strength $$\gamma ds$$. If we consider a point $$P$$ located at some distance $$r$$ from this $$ds$$, it will have a potential of:

    $$
    d\phi = \frac{\gamma ds}{2 \pi} ln(r)
    $$

    Which is simply the potential equation for a source applied infinitesimally, the total potential at $$P$$ due to the entire sheet is obtained by integrating this expression
    over the length of the panel:
                     
    $$
    \phi (x, y) = \int \frac{\gamma}{2 \pi} ln(r) \, ds               
    $$

    """, mathjax=True),

    ])
