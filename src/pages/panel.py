import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def panel():
    return html.Div(children=[

    html.H1("Panel Methods"),
    dcc.Markdown(r"""
    
    This section will detail a **group of numerical methods** which can be used to obtain the **potential flow around arbitrary bodies**. For this, we return
    to the point in the previous section where we made the simplification of placing our vortex sheet on the camber line and then on the chord line for an airfoil. In this
    series of methods we will **cover the body in source, vortex or a combination of these sheets**. To make the computations tangible we will use a **discrete number of panels**
    wherein the condition of **flow tangency** or **zero normal flow** will be **applied at certain control points**, typically in the **middle of each panel**. 
    
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
    
    Finally, to calculate these geometrical parameters we can make the following observations

    $$
    XC = \frac{XB_{i+1} + XB_{i}}{2},
    $$  
    $$
    YC = \frac{YB_{i+1} + YB_{i}}{2},
    $$                
    $$
    S = \sqrt{(XB_{i+1} - XB_{i})^{2} + (YB_{i+1} - YB_{i})^{2}},
    $$
    $$
    \varphi = arctan\left(\frac{YB_{i+1} - YB_{i}}{XB_{i+1} - XB_{i}}\right),
    $$
    $$                    
    \delta = \phi + \frac{\pi}{2},
    $$
    $$
    \beta = \delta - \alpha.                    
    $$

    """, mathjax=True),
    
    html.Hr(),
    html.H2("Source Panel Method"),
    
        dcc.Markdown(r"""
    
    **1. Velocity Component Equations**

    Now that the geometrical discussions are settled, we can proceed with covering our body in **source panels** as a start. Note, that these **will not generate any lift** due to
    the lack of circulation from sources. We define a source sheet much like we did with the vortex sheet in the previous section, it has a strength per unit length of $$\lambda = \lambda (s)$$ and
    an infinitesimal portion of this sheet has strength $$\lambda ds$$. If we consider a point $$P$$ located at some distance $$r$$ from this $$ds$$, it will have a potential of

    $$
    d\phi = \frac{\lambda ds}{2 \pi} ln(r).
    $$

    Which is simply the **potential equation for a source applied infinitesimally**, the **total potential** at $$P$$ due to the entire sheet is obtained by integrating this expression
    over the length of the panel
                     
    $$
    \phi (x, y) = \int \frac{\lambda}{2 \pi} ln(r) \, ds.              
    $$

    Now we take the **strength of these panels** as **constant along their length but varying across different panels**, then the velocity potential induced at point $$P(x, y)$$ from the jth panel
    is just like before but we can take the strength out of the integral
                     
    $$
    \Delta \phi_{j} = \frac{\lambda_{j}}{2 \pi} \int_j  ln(r_{Pj}) \, ds_{j}.            
    $$

    Finally, the potential due to all panels at point P is simply a sum of all the $$n$$ panels' contributions due to the linearity of potential flow
                     
    $$
    \phi (P) = \sum_{j=1}^n \Delta \phi_{j} = \sum_{j=1}^n \frac{\lambda_{j}}{2 \pi} \int_j  ln(r_{Pj}) \, ds_{j}.            
    $$

    This point P is some point in the flow, but we do not really know anything about the flow's condition there. It would make our job easier if we considered this point at some point in the flow where we know something about
    its characteristics. This is the case, for example, at the control points of the panels where we apply the flow tangency condition. Hence, we will **take point P as the control point** of the ith panel of coordinates
    $$(x_{i}, y_{i})$$, then the total potential induced by all the panels is
                     
    $$
    \phi (x_{i}, y_{i}) = \sum_{j=1}^n \frac{\lambda_{j}}{2 \pi} \int_j  ln(r_{ij}) \, ds_{j},              
    $$
    $$
    r_{ij} = \sqrt{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}}.              
    $$
                     
    Our **aim** is to **calculate the values of these source strengths** $$\lambda_{j}$$, because the potential at a point can be related to the velocity components at that point, we can
    use the fact that we know that the normal velocity component with respect to the panel at the control point should be zero. This will allow us to form a set of **algebraic equation to solve for the source strengths**. The normal component of the freestream
    at a control point is obtained from ordinary vector geometry
                     
    $$
    V_{\infty, n} = \mathbf{V_{\infty}} \cdot \mathbf{n_{i}} = V_{\infty} cos(\beta_{i}).                 
    $$
                     
    Note that previously $$\beta$$ was defined as the angle between the normal vector and the freestream vector. The normal velocity induced by the panels at the control point is then
        
    $$
    V_{n} = \frac{\partial}{\partial n_{i}} [\phi (x_{i}, y_{i})] =  \sum_{j=1}^n \frac{\lambda_{j}}{2 \pi} \int_j \frac{\partial}{\partial n_{i}}[ln(r_{ij})] \, ds_{j}.               
    $$
                     
    This last expression is **not entirely correct**, as the derivative of the natural logarithm is proportional to $$1/r_{ij}$$. This means that we will get a singularity for the panel $$j=i$$, for which $$r_{ii}=0$$. It can be derived that for this case, the panel induces a 
    normal velocity of $$\lambda_{i}/2$$ on itself. You can think of this as the panel **splitting the contribution of its induced velocity equally in both normal directions**. You will see later that there is **no induced
    tangential component**, then its contribution is just in the normal direction, equally distribution in both senses. The **correct expression** is then
                     
    $$
    V_{n} = \frac{\lambda_{i}}{2} + \sum_{j=1, j \neq i}^n \frac{\lambda_{j}}{2 \pi} \int_j \frac{\partial}{\partial n_{i}}[ln(r_{ij})] \, ds_{j}.                
    $$                
                     
    As said before, we chose the control points of the panels as we know something about the flow there. We know from previous discussions that for the body to become a streamline of the flow, we need to have the normal component of velocity zero with respect to the body. The total velocity 
    expression at the control points is the sum of the contribution from all panels and the freestream, hence we obtain the following equality
                     
    $$
    V_{n, i}(x_{i}, y_{i}) = V_{n} + V_{\infty, n} = \frac{\lambda_{i}}{2} + \sum_{j=1, j \neq i}^n \frac{\lambda_{j}}{2 \pi} \int_j \frac{\partial}{\partial n_{i}}[ln(r_{ij})] \, ds_{j} + V_{\infty} cos(\beta_{i}) = 0.               
    $$
                     
    To make the expression a bit simpler, we will call the integral, which **only depends on geometry**,  $$I_{i, j}$$ when we look at the ith control point and we integrate over the jth panel
                     
    $$
    \frac{\lambda_{i}}{2} + \sum_{j=1, j \neq i}^n \frac{\lambda_{j}}{2 \pi} I_{i, j} + V_{\infty} cos(\beta_{i}) = 0.                 
    $$
                     
    This expression is a **linear algebraic equation** containing $$n$$ unknowns, if we apply it at all the control points for all our panels we then have $$n$$ equations for $$n$$ unknowns which can be solved to obtain the source strength distribution to make the desired body a streamline of the flow. 
    After we have computed these strengths, we can calculate the tangential velocity along the panels' control points, which is again a combination of the freestream and the induced velocity.

    $$
    V_{\infty, t} = V_{\infty} sin(\beta_{i}),
    $$
    $$
    V_{t} = \frac{\partial \phi}{\partial t_{i}} =  \sum_{j=1}^n \frac{\lambda_{j}}{2 \pi} \int_j \frac{\partial}{\partial t_{i}}[ln(r_{ij})] \, ds_{j},               
    $$
    $$
    V_{t, i}(x_{i}, y_{i}) = V_{\infty, t} + V_{t} = V_{\infty} sin(\beta_{i}) + \sum_{j=1}^n \frac{\lambda_{j}}{2 \pi} \int_j \frac{\partial}{\partial t_{i}}[ln(r_{ij})] \, ds_{j}.                 
    $$

    In this case, the freestream tangential velocity is just the remaining component if we look at the normal velocity expression. The partial derivative is taken in the direction of the panel tangential vector, which **points in the direction from the first boundary point to the second boundary point of the panel
    in a clock-wise direction around our body**. For the case when $$j=i$$ there is **no contribution from the panel on itself**. This is because the induced velocity by a source comes radially out of its center, but the components along the panel surface **sum to zero** as they are cancelled by the sources nearby, since they induce the velocity in the opposite direction as
    compared to their neighbors. Finally, like for the normal velocity, we will denote the integral in this case as $$J_{i, j}$$. 

    **2. Normal and Tangential Geometric Integrals**                 

    In this section we will tackle the solution to the geometric integrals $$I_{i, j}$$ and $$J_{i, j}$$ obtained previously. We first begin with $$I_{i, j}$$ and evaluate the inner derivative
                     
    $$
    \frac{\partial}{\partial n_{i}}[ln(r_{ij})] = \frac{1}{r_{ij}} \frac{\partial r_{ij}}{\partial n_{i}} = \frac{1}{\sqrt{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}}} \frac{\partial}{\partial n_{i}} [\sqrt{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}}],
    $$
    $$
    \frac{\partial}{\partial n_{i}}[ln(r_{ij})] = \frac{1}{\sqrt{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}}} \frac{1}{2} \left((x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2} \right)^{-1/2} \left( 2(x_{i}-x_{j})\frac{\partial x_{i}}{\partial n_{i}} + 2(y_{i} - y_{j}) \frac{\partial y_{i}}{\partial n_{i}} \right),
    $$               
    $$
    \frac{\partial}{\partial n_{i}}[ln(r_{ij})] = \frac{(x_{i}-x_{j})\frac{\partial x_{i}}{\partial n_{i}} + (y_{i} - y_{j}) \frac{\partial y_{i}}{\partial n_{i}}}{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}}.                
    $$

    If you now consider the panel geometry, a small change $$\partial n_{i}$$ in the normal vector will cause a small change on both the x-axis $$\partial x_{i}$$ and the y-axis $$\partial y_{i}$$, these infinitesimal changes form a right-angled triangle
    where the angle of the normal vector with the x-axis $$\delta_{i}$$, as defined before. From this we can find the expressions for the previous partial derivatives
                     
    $$
    \frac{\partial x_{i}}{\partial n_{i}} = cos(\delta_{i}),                 
    $$
    $$
    \frac{\partial y_{i}}{\partial n_{i}} = sin(\delta_{i}).                 
    $$

    The integral then becomes

    $$
    I_{i, j} = \int_j \frac{(x_{i} - x_{j})cos(\delta_{i}) + (y_{i} - y_{j})sin(\delta_{i})}{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}} \, ds_{j}.               
    $$
                     
    Since we integrate along the panel's local coordinate $$s_{j}$$, we need to **express our integrand in terms of it**. We can express the variables $$x_{j}$$ and $$y_{j}$$ in terms of the constant initial boundary point $$X_{j}$$ and $$Y_{j}$$ of the panel together with
    the angle $$\varphi$$ defined at the start, these substitutions are
                     
    $$
    x_{j} = X_{j} + s_{j}cos(\varphi_{j}),                 
    $$
    $$
    y_{j} = Y_{j} + s_{j}sin(\varphi_{j}),                 
    $$
    $$
    cos(\delta) = -sin(\varphi),                
    $$
    $$
    sin(\delta) = cos(\varphi).
    $$                 
    
    The last two expressions are used to remove the angle $$\delta$$ to be able to group terms which arise from the substitution of $$s_{j}$$. After performing the substitution and a lot of algebra, the final form of the integral
    can be simplified to
                     
    $$
    I_{i, j} = \int_0^{S_{j}} \frac{Cs_{j}+D}{s_{j}^{2} + 2As_{j} + B} \, ds_{j},               
    $$
    $$
    A = -(x_{i}-X_{j})cos(\varphi_{j}) - (y_{i}-Y_{j})sin(\varphi_{j}),                
    $$                 
    $$
    B = (x_{i}-X_{j})^{2} + (y_{i}-Y_{j})^{2},                 
    $$
    $$
    C = sin(\varphi_{i}-\varphi_{j}),                
    $$
    $$
    D = -(x_{i}-X_{j})sin(\varphi_{i}) + (y_{i}-Y_{j})cos(\varphi_{i}).                 
    $$
   
    This integral can be solved as it is a known standard form, if we also use $$E = \sqrt{B-A^{2}}$$, then the solution is
                     
    $$
    I_{i, j} = \frac{C}{2} \left( ln \left( \frac{S_{j}^{2} + 2AS_{j} + B}{B} \right) \right) + \frac{D-AC}{E} \left( arctan \left(\frac{S_{j}+A}{E} \right) - arctan \left(\frac{A}{E} \right)   \right).         
    $$
                     
    The procedure for $$J_{i, j}$$ is very similar, the expression for the partial derivative with respect to the tangential vector is

    $$
    \frac{\partial}{\partial t_{i}}[ln(r_{ij})] = \frac{(x_{i}-x_{j})\frac{\partial x_{i}}{\partial t_{i}} + (y_{i} - y_{j}) \frac{\partial y_{i}}{\partial t_{i}}}{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}}.                
    $$

    Similar to before, we can express these partial derivative terms in term of the sine and cosine of some angle, however, in this case it is directly the angle of inner side of the panel with the x-axis $$\varphi$$ since we are dealing with the tangential vector. The integral will then become            

    $$
    \frac{\partial x_{i}}{\partial t_{i}} = cos(\varphi_{i}),                
    $$
    $$
    \frac{\partial y_{i}}{\partial t_{i}} = sin(\varphi_{i}),                 
    $$
    $$
    J_{i, j} = \int_j \frac{(x_{i} - x_{j})cos(\varphi_{i}) + (y_{i} - y_{j})sin(\varphi_{i})}{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}} \, ds_{j}.                 
    $$

    We can then apply the same expressions to introduce $$s_{j}$$ into the integral but we do not need to make any changes for the trigonometric expressions since they have the same angle as argument. Omitting the algebraic 
    manipulations, the integral can be simplified into an identical form to the previous case, however the expressions for some terms are slightly different 
    
    $$
    J_{i, j} = \int_0^{S_{j}} \frac{Cs_{j}+D}{s_{j}^{2} + 2As_{j} + B} \, ds_{j},               
    $$              
                     
    $$
    A = -(x_{i}-X_{j})cos(\varphi_{j}) - (y_{i}-Y_{j})sin(\varphi_{j}),                
    $$                 
    $$
    B = (x_{i}-X_{j})^{2} + (y_{i}-Y_{j})^{2},                 
    $$
    $$
    C = -cos(\varphi_{i}-\varphi_{j}),                
    $$
    $$
    D = (x_{i}-X_{j})cos(\varphi_{i}) + (y_{i}-Y_{j})sin(\varphi_{i}).                 
    $$               

    Just like before, if we use $$E = \sqrt{B-A^{2}}$$ then the integral's solution is the same expression as before 

    $$
    J_{i, j} = \frac{C}{2} \left( ln \left( \frac{S_{j}^{2} + 2AS_{j} + B}{B} \right) \right) + \frac{D-AC}{E} \left( arctan \left(\frac{S_{j}+A}{E} \right) - arctan \left(\frac{A}{E} \right)   \right).         
    $$                           

    **3. System of Equations**

    The final step is to set up our system of equations to solve for the unkown strengths of our source panels. If we have 3 panels, then using the equality derived for the normal velocity component at the control points
    we have the following set of equations
                     
    $$
    V_{n, 1} = \frac{\lambda_{1}}{2} + \frac{\lambda_{2} I_{12}}{2 \pi} + \frac{\lambda_{3} I_{13}}{2 \pi} + V_{\infty} cos(\beta_{1}) = 0,           
    $$
    $$
    V_{n, 2} = \frac{\lambda_{1} I_{21}}{2 \pi} + \frac{\lambda_{2}}{2} + \frac{\lambda_{3} I_{23}}{2 \pi} + V_{\infty} cos(\beta_{2}) = 0,
    $$
    $$
    V_{n, 3} = \frac{\lambda_{1} I_{31}}{2 \pi} + \frac{\lambda_{2} I_{32}}{2 \pi} + \frac{\lambda_{3}}{2} + V_{\infty} cos(\beta_{3}) = 0.
    $$                 

    This can be converted into a **matrix equation**, we also multiply by $$2 \pi$$ so that our system matrix contains the solely the geometric integrals in the off-diagonal elements
    
    $$
    
        \begin{bmatrix}
        \pi & I_{12} & I_{13} \\
        I_{21} & \pi & I_{23} \\
        I_{31} & I_{32} & \pi
        \end{bmatrix}
        \begin{bmatrix}
        \lambda_{1} \\
        \lambda_{2} \\
        \lambda_{3}
        \end{bmatrix}
        =
        \begin{bmatrix}
        -V_{\infty} 2 \pi cos(\beta_{1}) \\
        -V_{\infty} 2 \pi cos(\beta_{2}) \\
        -V_{\infty} 2 \pi cos(\beta_{3})
        \end{bmatrix}
                     
    $$

    After we solve this equation, we can **calculate the tangential velocity at the control points with the previously derived expressions**. Then, using the **incompressible pressure coefficient** formula we can calculate
    the pressure distribution along the body with

    $$
    C_{p, i} = 1 - \left(\frac{V_{i}}{V_{\infty}} \right)^{2}.
    $$                

    Finally, to **check the accuracy of our computations** we can perform the following calculation. Since the **airfoil is simply a solid body in the flow**, it **does not add or subtract any mass**, the sum of our source/sink
    strengths should be 0, indicating that **mass flow is preserved**. The source/sink strengths we have calculated are per unit length, so the total strength of a panel is $$S_{j} \lambda_{j}$$ and our results should satisfy

    $$
    \sum^{n}_{j=1} \lambda_{j} S_{j} = 0.                
    $$
                     
    Note that the **system matrix is a full matrix**, meaning no terms are zero. This is **inconvenient** as you will see later on during your second year that **sparse matrices** (those with a lot of zero terms in the off-diagonal positions) **can be solved
    much more efficiently and faster than full matrices**. This is one of the **drawbacks of this method**.

    **4. Cylinder Example. **
                     
    In this example you can modify parameters for the case of a **cylinder**. If you are implementing the method yourself, you can verify the different point coordinates in the plots and below the matrix equations
    for the 8 panel cylinder is given as well for this purpose. In the plots, you can see the analytical solution for the non-lifing flow around a cylinder and the computed values of the pressure coefficient at the panels' control points. 
    The remaining plots show the **pressure and velocity field** around the cylinder including the **streamlines**, to be able to calculate these kinds of plots you need to calculate the x and y components of the velocity field at each point. 
    This is done much in the same way as with the normal and tangential velocity components, it is the sum of the freestream and the induced velocity but the partial derivatives are taken with respect to the x and y directions.  

    $$
    
        \begin{bmatrix}
        3.1415 & 0.3528 & 0.4017 & 0.4073 & 0.4084 & 0.4073 & 0.4017 & 0.3528 \\
        0.3528 & 3.1415 & 0.3528 & 0.4017 & 0.4073 & 0.4084 & 0.4073 & 0.4017 \\
        0.4017 & 0.3528 & 3.1415 & 0.3528 & 0.4017 & 0.4073 & 0.4084 & 0.4073 \\
        0.4073 & 0.4017 & 0.3528 & 3.1415 & 0.3528 & 0.4017 & 0.4073 & 0.4084 \\
        0.4084 & 0.4073 & 0.4017 & 0.3528 & 3.1415 & 0.3528 & 0.4017 & 0.4073 \\
        0.4073 & 0.4084 & 0.4073 & 0.4017 & 0.3528 & 3.1415 & 0.3528 & 0.4017 \\
        0.4017 & 0.4073 & 0.4084 & 0.4073 & 0.4017 & 0.3528 & 3.1415 & 0.3528 \\
        0.3528 & 0.4017 & 0.4073 & 0.4084 & 0.4073 & 0.4017 & 0.3528 & 3.1415 
        \end{bmatrix}
        \begin{bmatrix}
        \lambda_{1} \\
        \lambda_{2} \\
        \lambda_{3} \\
        \lambda_{4} \\
        \lambda_{5} \\
        \lambda_{6} \\
        \lambda_{7} \\
        \lambda_{8} 
        \end{bmatrix}
        =
        \begin{bmatrix}
        -6.2831 \\
        -4.4428 \\
        0 \\
        4.4428 \\
        6.2831 \\
        4.4428 \\
        0 \\
        -4.4428
        \end{bmatrix}
                     
    $$

    """, mathjax=True),

    html.Label("Number of Panels Slider"),
    dcc.Slider(6, 16,
               value=8,
               id="numPanel",
               marks={6: {'label': "6"},
                        8: {'label': "8"},
                        10: {'label': "10"}, 
                        12: {'label': "12"},
                        14: {'label': "14"},
                        16: {'label': "16"}}
              ),
    html.Label("Freestream Velocity Slider"),
    dcc.Slider(10, 100,
               value=10,
               id="velocity",
               marks={10: {'label': "10"},
                        20: {'label': "20"},
                        30: {'label': "30"}, 
                        40: {'label': "40"},
                        50: {'label': "50"},
                        60: {'label': "60"}, 
                        70: {'label': "70"},
                        80: {'label': "80"},
                        90: {'label': "90"},
                        100: {"label": "100"}}
              ),

    html.Label("Angle of Attack Slider"),
    dcc.Slider(-90, 90,
               value=0,
               id="angleOfAttack10",
               marks={-90: {'label': "-90"},
                         -45: {"label": "-45"},
                           0: {'label': "0"},
                        45: {'label': "45"}, 
                        90: {'label': "90"}}
              ),          

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="SourceCylinder", mathjax=True),
        ], width=10)
    ], justify='center'),
                     
    dcc.Markdown(r"""

    **5. Airfoil Example**
                 
    Lastly, an example with **various airfoil** types is shown. You may observe the **pressure coefficient distribution is a little bit unsual**, this is because the **source panel method does not create circulation** and as such,
    the **airfoil does not generate any lift**. This is deeply related to the pressure distribution and this is the reason for the unusual shape. A few NACA 4-digit airfoil types are available to try, note that it **may take some time for it to load** depending on your hardware.

                 """, mathjax=True),

    html.Label("Airfoil Type Selector"),
    dcc.RadioItems(
    id='airfoilType1',
    options=[
        {'label': 'NACA-0012', 'value': 1},
        {'label': 'NACA-2412', 'value': 2},
        {'label': 'NACA-2404', 'value': 3},
        {'label': 'NACA-4520', 'value': 4}
    ],
    value=1,  # Default value
    ),
    html.Label("Freestream Velocity Slider"),
    dcc.Slider(10, 100,
               value=10,
               id="velocity2",
               marks={10: {'label': "10"},
                        20: {'label': "20"},
                        30: {'label': "30"}, 
                        40: {'label': "40"},
                        50: {'label': "50"},
                        60: {'label': "60"}, 
                        70: {'label': "70"},
                        80: {'label': "80"},
                        90: {'label': "90"},
                        100: {"label": "100"}}
              ),

    html.Label("Angle of Attack Slider"),
    dcc.Slider(-90, 90,
               value=0,
               id="angleOfAttack11",
               marks={-90: {'label': "-90"},
                         -45: {"label": "-45"},
                           0: {'label': "0"},
                        45: {'label': "45"}, 
                        90: {'label': "90"}}
              ),          

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="SourceAirfoil", mathjax=True),
        ], width=10)
    ], justify='center'),


    html.Hr(),
    html.H2("Vortex Panel Method"),

    dcc.Markdown(r"""
                 
    **1. Velocity Component Equations**
                 
    The **previous panel method is a bit useless**, potential theory cannot model drag and the source panel method can't even calculate lift. Using vortex panel seems like a better option, in this case **lift will be created**, since
    the panels will induce some circulation in the flow. Hence, we proceed with covering our body in vortex panels of varying strength between them but constant along one panel. The velocity potential
    induced at a point $$P(x, y)$$ by the jth vortex panel is given by
                 
    $$
    \delta \phi_{j} = \frac{-1}{2 \pi} \int_{j} \theta_{Pj} \gamma_{j} ds_{j}.             
    $$

    Here, $$\theta_{Pj}$$ is the angle formed between the x-axis and the radial distance $$r_{Pj}$$ between the two points being evaluated, again it is simply the expression of the potential of a single vortex
    but distributed along a panel in terms of an integral. The total contribution by all panels to point P is
                 
    $$
    \phi (P) = \sum^{n}_{j=1} \phi_{j} = - \sum^{n}_{j=1} \frac{\gamma_{j}}{2 \pi} \int_{j} \theta_{Pj} ds_{j}.             
    $$

    Now we do the same thing as we did before, we will **take point P to be at the control point of another panel** with coordinates $$(x_{i}, y_{i})$$. The total induced potential at the ith panel's control point is

    $$
    \phi (x_{i}, y_{i}) = - \sum^{n}_{j=1} \frac{\gamma_{j}}{2 \pi} \int_{j} \theta_{Pj} ds_{j}, 
    $$                    
    $$
    \theta_{ij} = arctan \left(\frac{y_{i} - y_{j}}{x_{i} - x_{j}} \right).             
    $$
                 
    The **same boundary conditions applies for the body**, zero normal flow component. Its expression is again the sum of the freestream contribution $$V_{\infty, n}$$ and the normal component induced by the panels $$V_{n}$$, this then
    must equal zero. For the case of the tangential component, it is also the same as before
                 
    $$
    V_{n, i} (x_{i}, y_{i}) = V_{\infty, n} + V_{n} = V_{\infty} cos(\beta_{i}) - \sum^{n}_{j=1} \frac{\gamma_{j}}{2 \pi} \int_{j} \frac{\partial \theta_{Pj}}{\partial n_{i}} ds_{j} = 0,           
    $$
                 
    $$
    V_{t, i} (x_{i}, y_{i}) = V_{\infty, t} + V_{t} = V_{\infty} sin(\beta_{i}) + \frac{\gamma_{i}}{2} - \sum^{n}_{j=1, j \neq i} \frac{\gamma_{j}}{2 \pi} \int_{j} \frac{\partial \theta_{Pj}}{\partial t_{i}} ds_{j}.                       
    $$

    Since the vortex is sort of the opposite of a source, in the sense that the flow directions are perpendicular to each other, when $$i = j$$ we obtain the **opposite results as for a source panel**. There is **no contribution in the normal direction**
    on the panel surface and the **tangential velocity contribution is equally distributed** with $$\gamma / 2$$. Finally, we have to compute the expressions of these integrals like we did with the source panel method. They are similar in that they again only depend on the geometry of our body and we will denote following the same convention but with 
    $$K_{ij}$$ and $$L_{ij}$$ for the normal and tangential integrals, respectively. 

    **2. Normal and Tangential Geometric Integrals**
                 
    We start with the normal geometric integral, we first use the expression for the derivative of the arctangent function
                 
    $$
    \frac{\partial \theta_{ij}}{\partial n_{i}} = \left(\frac{1}{1 + \left( \frac{y_{i} - y_{j}}{x_{i} - x_{j}} \right)^{2}} \right) \left( \frac{(x_{i} - x_{j}) \left( \frac{\partial y_{i}}{\partial n_{i}} - \frac{\partial y_{j}}{\partial n_{i}} \right) - (y_{i} - y_{j}) \left(\frac{\partial x_{i}}{\partial n_{i}} - \frac{\partial x_{j}}{\partial n_{i}} \right)}{(x_{i} - x_{j})^{2}} \right).            
    $$

    To evaluate the partial derivatives we have to notice that the ones which **combine different subscripts i and j are zero**, since a change in the coordinates of the jth panel doesn't have an effect on the normal vector of the ith panel at which we evaluate the 
    total induced velocity. For the ones with the same subscript i, we use the same expressions as with the source panel method. To summarize, the partial derivatives are equal to
                 
    $$
    \frac{\partial y_{j}}{\partial n_{i}} = \frac{\partial x_{j}}{\partial n_{i}} = 0,             
    $$
    $$
    \frac{\partial y_{i}}{\partial n_{i}} = sin(\delta_{i}),          
    $$
    $$
    \frac{\partial x_{i}}{\partial n_{i}} = cos(\delta_{i}).             
    $$
                 
    After these substitutions, the integral becomes

    $$
    K_{ij} = \int_{j} \frac{(x_{i} - x_{j}) sin(\delta_{i}) - (y_{i} - y_{j}) cos(\delta_{i})}{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}}, ds_{j}.            
    $$

    By performing the substitution of the expressions for $$s_{j}$$ and $$\varphi_{j}$$ like for the source panel method, we end up with the same simplified integral expression but with
    slightly differing expressions for the smaller constants

    $$
    K_{i, j} = \int_0^{S_{j}} \frac{Cs_{j}+D}{s_{j}^{2} + 2As_{j} + B} \, ds_{j},               
    $$ 
    $$
    A = -(x_{i}-X_{j})cos(\varphi_{j}) - (y_{i}-Y_{j})sin(\varphi_{j}),                
    $$                 
    $$
    B = (x_{i}-X_{j})^{2} + (y_{i}-Y_{j})^{2},                 
    $$
    $$
    C = -cos(\varphi_{i}-\varphi_{j}),                
    $$
    $$
    D = (x_{i}-X_{j})cos(\varphi_{i}) + (y_{i}-Y_{j})sin(\varphi_{i}),                 
    $$
    $$
    E = \sqrt{B - A^{2}},
    $$
    $$
    K_{i, j} = \frac{C}{2} \left( ln \left( \frac{S_{j}^{2} + 2AS_{j} + B}{B} \right) \right) + \frac{D-AC}{E} \left( arctan \left(\frac{S_{j}+A}{E} \right) - arctan \left(\frac{A}{E} \right)   \right).         
    $$  

    We now proceed similarly with the tangential integral $$L_{ij}$$. The derivative is calculated in the same way

    $$
    \frac{\partial \theta_{ij}}{\partial t_{i}} = \left(\frac{1}{1 + \left( \frac{y_{i} - y_{j}}{x_{i} - x_{j}} \right)^{2}} \right) \left( \frac{(x_{i} - x_{j}) \left( \frac{\partial y_{i}}{\partial t_{i}} - \frac{\partial y_{j}}{\partial t_{i}} \right) - (y_{i} - y_{j}) \left(\frac{\partial x_{i}}{\partial t_{i}} - \frac{\partial x_{j}}{\partial t_{i}} \right)}{(x_{i} - x_{j})^{2}} \right).            
    $$
                 
    The same considerations apply for the partial derivatives in this case, those with differing subscripts are zero and those with the same are evaluated as in the source panel method.
    This leaves the integral in the form of:
                 
    $$
    L_{ij} = \int_{j} \frac{(x_{i} - x_{j}) sin(\varphi_{i}) - (y_{i} - y_{j}) cos(\varphi_{i})}{(x_{i} - x_{j})^{2} + (y_{i} - y_{j})^{2}}, ds_{j}.            
    $$
                 
    We introduce $$s_{j}$$ and simplify the integral to obtain
                 
    $$
    L_{i, j} = \int_0^{S_{j}} \frac{Cs_{j}+D}{s_{j}^{2} + 2As_{j} + B} \, ds_{j},               
    $$              
                     
    $$
    A = -(x_{i}-X_{j})cos(\varphi_{j}) - (y_{i}-Y_{j})sin(\varphi_{j}),                
    $$                 
    $$
    B = (x_{i}-X_{j})^{2} + (y_{i}-Y_{j})^{2},                 
    $$
    $$
    C = sin(\varphi_{i}-\varphi_{j}),                
    $$
    $$
    D = (x_{i}-X_{j})sin(\varphi_{i}) - (y_{i}-Y_{j})cos(\varphi_{i}).                 
    $$               

    If we use $$E = \sqrt{B-A^{2}}$$, then the integral's solution is the same expression as before 

    $$
    L_{i, j} = \frac{C}{2} \left( ln \left( \frac{S_{j}^{2} + 2AS_{j} + B}{B} \right) \right) + \frac{D-AC}{E} \left( arctan \left(\frac{S_{j}+A}{E} \right) - arctan \left(\frac{A}{E} \right)   \right).         
    $$
    
    **3. System of Equations and Lift Calculation**
                 
    For a body of 3 panels, the system of equations looks as follows
                 
    $$
    V_{n, 1} = \frac{-\gamma_{2}}{2 \pi} K_{12} - \frac{\gamma_{3}}{2 \pi} K_{13} + V_{\infty} cos(\beta_{1}) = 0,         
    $$
    $$
    V_{n, 2} = \frac{-\gamma_{1}}{2 \pi} K_{21} - \frac{\gamma_{3}}{2 \pi} K_{23} + V_{\infty} cos(\beta_{2}) = 0,             
    $$
    $$
    V_{n, 3} = \frac{-\gamma_{1}}{2 \pi} K_{31} - \frac{\gamma_{2}}{2 \pi} K_{32} + V_{\infty} cos(\beta_{3}) = 0.            
    $$
                 
    We convert to a matrix equation after multiplying by $$2 \pi$$ to obtain
                 
    $$
    
        \begin{bmatrix}
        0 & -K_{12} & -K_{13} \\
        -K_{21} & 0 & -K_{23} \\
        -K_{31} & -K_{32} & 0
        \end{bmatrix}
        \begin{bmatrix}
        \gamma_{1} \\
        \gamma_{2} \\
        \gamma_{3}
        \end{bmatrix}
        =
        \begin{bmatrix}
        -V_{\infty} 2 \pi cos(\beta_{1}) \\
        -V_{\infty} 2 \pi cos(\beta_{2}) \\
        -V_{\infty} 2 \pi cos(\beta_{3})
        \end{bmatrix}
                     
    $$

    But, this **matrix equation is not fully correct**. If you remember from the discussion in the thin-airfoil theory section, the **flow around an airfoil must satisfy the Kutta condition** $$\gamma (TE) = 0$$.
    This can be applied in multiple ways, one way is to consider the first and last panels (which are at the TE) as being sufficiently small and thus close, that if we force their vortex strength's to be the same, then they will cancel out and
    satisfy the Kutta condition. Hence, we have an **additional equation** $$\gamma_{1} = \gamma_{3}$$ but we already had 3 equations for 3 variables, so this would result in an **overdetermined system**. To fix this, we **remove one of the equations**
    for our system and **add the one from the Kutta condition**, resulting in the final matrix equation

    $$
    
        \begin{bmatrix}
        0 & -K_{12} & -K_{13} \\
        -K_{21} & 0 & -K_{23} \\
        1 & 0 & 1
        \end{bmatrix}
        \begin{bmatrix}
        \gamma_{1} \\
        \gamma_{2} \\
        \gamma_{3}
        \end{bmatrix}
        =
        \begin{bmatrix}
        -V_{\infty} 2 \pi cos(\beta_{1}) \\
        -V_{\infty} 2 \pi cos(\beta_{2}) \\
        -V_{\infty} 2 \pi cos(\beta_{3})
        \end{bmatrix}
                     
    $$

    Once we have solved this system, we can compute the tangential velocities at each control point and use the same pressure coefficient formula to calculate
    the pressure distribution along the body. To **calculate the lift generated by the body**, recall the **Kutta-Joukowski theorem** which gives the lift as proportional to the
    circulation in the flow. The total circulation induced by a panel is $$\gamma_{j} S_{j}$$ since $$\gamma_{j}$$ was its strength per unit length, the total circulation of the body and its lift are then
    
    $$
    \Gamma = \sum^{n}_{j=1} \gamma_{j} S_{j},             
    $$
    $$
    L' = \rho_{\infty} V_{\infty} \sum^{n}_{j=1} \gamma_{j} S_{j}.           
    $$            

    **4. Airfoil Example**

    Here you can find a similar example using the same airfoils as for the source panel method. In this case, the **airfoil does generate lift** and as such, the **pressure distribution is more like you would expect**. 
    You may find however, that **this method does not work well for all types of airfoils** and it is quite **sensitive to the panel geometry**. Nonetheless, some collected data which
    can be compared to the thin-airfoil theory results can also be seen in the table below.            


    """, mathjax=True),

    html.Img(src="assets/VP-vs-XFOIL.png",
            style={
                "width": "600px",  # Set desired width
                "height": "auto"  }
                ),

        dcc.Markdown(r"""
    
    As can be seen from the table, the **vortex panel method is not such an accurate one**. The prediction of the **moment coefficient is quite off**, the **lift coefficient prediction is sometimes even worse than the thin-airfoil 
    theory** when the airfoil is thin. For the thicker airfoil, the vortex panel does better as it accounts for thickness. But overall, you can see that **this method is not the most ideal**.  
 
    """, mathjax=True),

    html.Label("Airfoil Type Selector"),
    dcc.RadioItems(
    id='airfoilType2',
    options=[
        {'label': 'NACA-0012', 'value': 1},
        {'label': 'NACA-2412', 'value': 2},
        {'label': 'NACA-2404', 'value': 3},
        {'label': 'NACA-4520', 'value': 4}
    ],
    value=1,  # Default value
    ),
    html.Label("Freestream Velocity Slider"),
    dcc.Slider(10, 100,
               value=10,
               id="velocity3",
               marks={10: {'label': "10"},
                        20: {'label': "20"},
                        30: {'label': "30"}, 
                        40: {'label': "40"},
                        50: {'label': "50"},
                        60: {'label': "60"}, 
                        70: {'label': "70"},
                        80: {'label': "80"},
                        90: {'label': "90"},
                        100: {"label": "100"}}
              ),

    html.Label("Angle of Attack Slider"),
    dcc.Slider(-90, 90,
               value=0,
               id="angleOfAttack12",
               marks={-90: {'label': "-90"},
                         -45: {"label": "-45"},
                           0: {'label': "0"},
                        45: {'label': "45"}, 
                        90: {'label': "90"}}
              ),          

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="VortexAirfoil", mathjax=True),
        ], width=10)
    ], justify='center'),



    html.Hr(),
    html.H2("Source-Vortex Panel Method"),

    dcc.Markdown(r"""                    

    **1. Velocity Component Equations**

    The vortex panel method works, but it is not as good as we would like since for some airfoils it does not provide a good solution and it can be highly dependent on the panels' sizes and positions. The final method we will
    consider here is a **combination of the previous two**, we will have **source panels of constant strength but varying between panels** and **vortex panels of constant strength but not varying between panels**, so we will have a single value
    for the vortex panel strength. The total normal and tangential velocity expressions at a panel's control point is simply the sum of all the previously derived expressions

    $$
    V_{n, i} (x_{i}, y_{i}) = V_{\infty} cos(\beta_{i}) + \frac{\lambda_{i}}{2} - \sum^{n}_{j=1} \frac{\gamma}{2 \pi} \int_{j} \frac{\partial \theta_{Pj}}{\partial n_{i}} ds_{j} + \sum_{j=1, j \neq i}^n \frac{\lambda_{j}}{2 \pi} \int_j \frac{\partial}{\partial n_{i}}[ln(r_{ij})] \, ds_{j} = 0,
    $$   
    $$
    V_{t, i} (x_{i}, y_{i}) = V_{\infty} sin(\beta_{i}) + \frac{\gamma}{2} - \sum^{n}_{j=1, j \neq i} \frac{\gamma}{2 \pi} \int_{j} \frac{\partial \theta_{Pj}}{\partial t_{i}} ds_{j} + \sum_{j=1}^n \frac{\lambda_{j}}{2 \pi} \int_j \frac{\partial}{\partial t_{i}}[ln(r_{ij})] \, ds_{j}.            
    $$
      

    **2. System of Equations and Lift Calculation**

    We **do not need to calculate any geometric integrals since they are the same as before**, hence we can directly move to creating the system of equations. Considering as an example a 3 panel body, we have
    
    $$
    V_{n, 1} = V_{\infty} cos(\beta_{1}) + \frac{\lambda_{1}}{2} + \frac{\lambda_{2} I_{12}}{2 \pi} + \frac{\lambda_{3} I_{13}}{2 \pi} - \frac{\gamma (K_{12} + K_{13})}{2 \pi} = 0,           
    $$
    $$
    V_{n, 2} = V_{\infty} cos(\beta_{2}) + \frac{\lambda_{2}}{2} + \frac{\lambda_{1} I_{21}}{2 \pi} + \frac{\lambda_{3} I_{23}}{2 \pi} - \frac{\gamma (K_{21} + K_{23})}{2 \pi} = 0,                       
    $$
    $$
    V_{n, 3} = V_{\infty} cos(\beta_{3}) + \frac{\lambda_{3}}{2} + \frac{\lambda_{1} I_{31}}{2 \pi} + \frac{\lambda_{2} I_{32}}{2 \pi} - \frac{\gamma (K_{31} + K_{32})}{2 \pi} = 0.                        
    $$
                 
    In this case, we have 4 unknowns and 3 equations meaning it is an **underdetermined system**. We can obtain the **final equation from the Kutta condition**, although this time it is a bit more involved since we cannot apply the same condition as we did for the vortex
    panel method because in this case all the vortex strengths are equal. Instead we **set the first and last panels' tangential velocities equal to each other**, but since the positive direction is the panel's tangential vector which goes in the clock-wise sense around the body, this means that the condition is
                 
    $$
    V_{t, N} + V_{t, 1} = 0,             
    $$
    $$
    V_{t, 1} = V_{\infty} sin(\beta_{1}) + \sum^{N}_{j=2} \frac{\lambda_{j} J_{ij}}{2 \pi} + \frac{\gamma_{1}}{2} - \sum^{N}_{j=2} \frac{\gamma L_{ij}}{2 \pi},
    $$
    $$
    V_{t, N} = V_{\infty} sin(\beta_{N}) + \sum^{N-1}_{j=1} \frac{\lambda_{j} J_{ij}}{2 \pi} + \frac{\gamma_{N}}{2} - \sum^{N-1}_{j=1} \frac{\gamma L_{ij}}{2 \pi}.             
    $$
                     
    Now, we will try to **isolate the unknown source and vortex strengths** to be able to add it into the system of equations
                 
    $$
    V_{\infty} sin(\beta_{1}) + \sum^{N}_{j=2} \frac{\lambda_{j} J_{ij}}{2 \pi} + \frac{\gamma_{1}}{2} - \sum^{N}_{j=2} \frac{\gamma L_{ij}}{2 \pi} + V_{\infty} sin(\beta_{N}) + \sum^{N-1}_{j=1} \frac{\lambda_{j} J_{ij}}{2 \pi} + \frac{\gamma_{N}}{2} - \sum^{N-1}_{j=1} \frac{\gamma L_{ij}}{2 \pi} = 0,         
    $$
    $$
    \sum^{N}_{j=2} \lambda_{j} J_{ij} - \sum^{N}_{j=2} \gamma L_{ij} + \sum^{N-1}_{j=1} \lambda_{j} J_{ij} - \sum^{N-1}_{j=1} \gamma L_{ij} + 2 \pi \gamma = -2 \pi V_{\infty} (sin(\beta_{1}) + V_{\infty} sin(\beta_{N})).           
    $$
                 
    For the 3 panel body, this expression is
                 
    $$
    \lambda_{2} J_{12} + \lambda_{3} J_{13} + \lambda_{1} J_{31} + \lambda_{2} J_{32} - \gamma L_{12} - \gamma L_{13} - \gamma L_{31} - \gamma L_{32} 2 \pi \gamma = -2 \pi V_{\infty} (sin(\beta_{1}) + sin(\beta_{N})).            
    $$

    If we now multiply the previous system of equations also by $$2 \pi$$ and add the Kutta condition, then we have our final system of equations in matrix form
    
    $$
    
        \begin{bmatrix}
        \pi & I_{12} & I_{13} & -(K_{12} + K_{13}) \\
        I_{21} & \pi & I_{23} & -(K_{21} + K_{23}) \\
        I_{31} & I_{32} & \pi $ -(K_{31} + K_{32}) \\
        J_{31} & (J_{12} + J_{32}) & J_{13} & -(L_{12} + L_{13} + L_{31} + L_{32}) + 2 \pi
        \end{bmatrix}
        \begin{bmatrix}
        \lambda_{1} \\
        \lambda_{2} \\
        \lambda_{3} \\
        \gamma
        \end{bmatrix}
        =
        \begin{bmatrix}
        -V_{\infty} 2 \pi cos(\beta_{1}) \\
        -V_{\infty} 2 \pi cos(\beta_{2}) \\
        -V_{\infty} 2 \pi cos(\beta_{3}) \\
        -V_{\infty} 2 \pi (sin(\beta_{1}) + sin(\beta_{3}))
        \end{bmatrix}
                     
    $$

    After this, the tangential velocity components can also be calculated, followed by the pressure coefficients and the lift with

    $$
    C_{p, i} = 1 - \left(\frac{V_{i}}{V_{\infty}} \right)^{2},
    $$           
    $$
    L' = \rho_{\infty} V_{\infty} \sum^{n}_{j=1} \gamma S_{j}.            
    $$

    **3. Airfoil Example**           

    The final example for the same airfoil types is shown below, **this method is stable for varying panel geometry and airfoil types**. You can find another table
    of tested values in comparison to the thin-airfoil theory results.


    """, mathjax=True),

     html.Img(src="assets/SVP-vs-XFOIL.png",
            style={
                "width": "600px",  # Set desired width
                "height": "auto"  }),


    dcc.Markdown(r"""
    
    From the table it can be seen that the **lift coefficient is predicted quite well** by this method in comparison to XFOIL. **For the moment coefficient there is some improvement 
    over the vortex one**, although **for the thicker airfoil at higher angles of attack**, it **doesn't capture the larger increase in the moment coefficient**, likely due to the fact that we neglect viscous phenomena. 

    """, mathjax=True),

    html.Label("Airfoil Type Selector"),
    dcc.RadioItems(
    id='airfoilType3',
    options=[
        {'label': 'NACA-0012', 'value': 1},
        {'label': 'NACA-2412', 'value': 2},
        {'label': 'NACA-2404', 'value': 3},
        {'label': 'NACA-4520', 'value': 4}
    ],
    value=1,  # Default value
    ),
    html.Label("Freestream Velocity Slider"),
    dcc.Slider(10, 100,
               value=10,
               id="velocity4",
               marks={10: {'label': "10"},
                        20: {'label': "20"},
                        30: {'label': "30"}, 
                        40: {'label': "40"},
                        50: {'label': "50"},
                        60: {'label': "60"}, 
                        70: {'label': "70"},
                        80: {'label': "80"},
                        90: {'label': "90"},
                        100: {"label": "100"}}
              ),

    html.Label("Angle of Attack Slider"),
    dcc.Slider(-90, 90,
               value=0,
               id="angleOfAttack13",
               marks={-90: {'label': "-90"},
                         -45: {"label": "-45"},
                           0: {'label': "0"},
                        45: {'label': "45"}, 
                        90: {'label': "90"}}
              ),          

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="SourceVortexAirfoil", mathjax=True),
        ], width=10)
    ], justify='center')

    ])
