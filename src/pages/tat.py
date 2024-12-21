import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def tat():
    return html.Div(children=[
    
    html.H1("Thin Airfoil Theory"),

    dcc.Markdown(r"""
    The analysis of **inviscid and incompressible aerodynamic wing analysis** is separated into two procedures. Firstly, the wing section or airfoil
    properties are considered, these are then modified to account for the complete, finite wing. This is highly useful as it allows us to decouple these two 
    processes, the first of these is the subject of this section and it is called **thin-airfoil theory**. Before we delve into this theory, we must establish a few key 
    concepts uisng the knowledge from the previous sections.
    
    """, mathjax=True),
    html.Br(),
    dcc.Markdown(r"""
                 
    **1. Vortex-Sheet Airfoil and Kutta Condition.**
                 
    In previous chapters we have been able to combine certain elementary potential flows in such a way that the resulting streamlines resemble basic solid bodies, this means
    that there is **no normal flow component into the body** itself since the flow velocity is parallel to a streamline. This will be a condition we will have to 
    impose. Now, if we want to represent more complex shapes as solid bodies in potential flow, we will have to use a more general method rather than trying to place a few sources or vortices
    with varying strengths until we obtain our required shape. A way in which this could be done is that you represent the body's contour by a **vortex sheet**. 
    
    A **vortex sheet** is nothing more than many subsequent vortex filaments next to each other. While a vortex filament is just a 3D extension of the 2D vortex
    we have discussed before, essentially a rotating cylinder of air extending in the perpendicular direction to our previous 2D plane. Now, we have our body represented as a
    vortex sheet but we must calculate the strength of the individual vortices that form this sheet to make the body a streamline of the flow. To do this, we will consider an infinite
    amount of vortices, then we define $$\gamma = \gamma (s)$$ as the strength of the vortex sheet per unit length along $$s$$, which is simply a coordinate along the body. 
    Since this strength per unit length varies along the body, we can then integrate it to obtain the total vorticity of the entire sheet representation and then the lift per unit depth of the body
    from the Kutta-Joukowski theorem. 
                 
    $$
    \Gamma = \int \gamma \, ds              
    $$
    $$
    L' = \rho_{\infty} V_{\infty} \Gamma
    $$

    You might be thinking about **why we use vortices** and not sources or doublets, for example. Firstly, our goal is to calculate the lift and moment of different airfoils (excluding drag due to the limitations of inviscid theory) and
    the vortex is the only elementary flow which **creates circulation**, and without it there wouldn't be any lift as you can see in the Kutta-Joukowski theorem. Hence, we always need to have vortices in our modelling, other elementary flow
    components can be added as you will see later on but vortices are a necessity. Secondly, it also sort of **models the effect of the boundary layer** along the surface of the body, which also
    inherently creates vorticity due to the no-slip condition. It is then a way to emulate its effects in a theory which neglects it in other aspects. 
    
    Finally, as we saw with the lifting flow around a cylinder case, there were an infinite number of theoretical solutions depending on the value of circulation used. The same issue arises for the airfoil, we can 
    have an infinite choice for the value of circulation for an airfoil at a given angle of attack. However, from experimental measurements it is clear that an airfoil will the same lift force (which is related to vorticity) at the same angle
    of attack every time. The condition for which we obtain the same circulation and flow pattern around an airfoil as in experiments in called the **Kutta condition** and it goes as follows:

    A. The value of $$\Gamma$$ is such that **the airflow around the airfoil**, at a given angle of attack, **leaves the trailing edge smoothly**. 
    
    B. For both finite-angled and cusped trailing edges this means that $$\gamma (TE) = 0$$.

    For further information on these initial matters, consult sections 4.4 and 4.5 of the course book.

    """, mathjax=True),
    html.Br(),
    dcc.Markdown(r"""

    **2. Thin Airfoil Theory Assumptions and Conditions.**     
    
    It is generally not possible to find a solution to the vorticity distribution we created, hence some further simplications
    must be made. We will now consider thin airfoils ($$<6\% t/c$$), if we look at these from far away then they can be seen as if they were only the camber line due to this small thickness. Additionally,
    from even farther away the camber line can be seen if it were on the chord line. Taking this into account, we make the following modelling decisions and conditions:

    A. The **camber line is a streamline of the flow**, instead of the body itself.
                  
    B. The **vortex sheet** is located **along the chord line**. 
                 
    C. There is **no normal component of the flow** induced by the vortex sheet **on the camber line**, since it is a streamline of the flow. 
                 
    D. The **airflow leaves the trailing edge smoothly**, $$\gamma (TE) = 0$$
                 
    E. The airflow is **incompressible**.
                 
    F. The **angle of attack is small** ($$<15º$$) such that small-angle approximations are valid. 

    """, mathjax=True),
    html.Br(),
    dcc.Markdown(r"""

    **3. Symmetric Airfoil Results.** 
                 
    The results obtained for a symmetric airfoil, one with no camber, are as follows:

    $$
    c_{l} = 2 \pi \alpha         
    $$
    $$
    c_{m,c/4} = c_{m,LE} + \frac{c_{l}}{4} = 0             
    $$
    $$
    \gamma (\theta) = 2 \alpha V_{\infty} \frac{1+cos(\theta)}{sin(\theta)}
    $$
    
    Here, $$\theta$$ is a new coordinate along the chord of the airfoil and it is related to the cartesian $$x$$ coordinate according to 
    $$x = \frac{c}{2}\left(1-cos(\theta)\right)$$. From these results we can observe that the **center of pressure** (where the resultant lift vector acts) and the 
    **aerodynamic center** (point where the aerodynamic moment is independent of the angle of attack) are **both at the quarter chord point** (c/4) and that the 
    lift variation of the airfoil is the same when pitching up or down since it follows a symmetric line with respect to the $$c_{l}$$ and $$\alpha$$ axes, implying that it **generates
    zero lift at zero angle of attack**. For details on the derivation of these results consult section 4.7 of the course book. 
                 
    """, mathjax=True),
    html.Br(),
    dcc.Markdown(r""" 

    **4. Cambered Airfoil Results.**    

    The result for a cambered airfoil is essentially the symmetric case plus a Fourier series term (an infinite trigonometric series). The key expressions
    are:

    $$
    \gamma (\theta) = 2 V_{\infty} \left(A_{0} \frac{1+cos(\theta)}{sin(\theta)} + \sum_{n=1}^\infty A_{n}sin(n\theta) \right)
    $$ 
    $$
    \frac{dz}{dx} = (\alpha - A_{0}) + \sum_{n=1}^\infty A_{n}cos(n\theta)
    $$ 
    $$
    A_{0} = \alpha - \frac{1}{\pi} \int_0^\pi \frac{dz}{dx} \, d\theta             
    $$
    $$
    A_{n} = \frac{2}{\pi} \int_0^\pi \frac{dz}{dx} cos(n\theta) \, d\theta
    $$  
    $$
    c_{l} = 2\pi(\alpha - \alpha_{L=0}) = \pi(2A_{0} + A_{1})
    $$
    $$
    c_{m, c/4} = \frac{\pi}{4}(A_{2} - A_{1})
    $$ 
    $$
    \frac{x_{CP}}{c} = \frac{1}{4} - \frac{c_{m, c/4}}{c_{l}} = \frac{1}{4}\left(1-\frac{A_{2} - A_{1}}{2A_{0}+A_{1}}\right)
    $$    
    
    Here, $$\theta$$ is the same coordinate as before and $$z(x)$$ is the equation of the camber line. Key takeaways are that the **lift slope is the same as for symmetric airfoils** but here **lift can be generated at zero angle of attack**. 
    Additionally, the **quarter chord point is still the aerodynamic center** as the coefficients in the equation do not depend on the angle of attack and the **center of pressure does not have a fixed location**, 
    it **varies with lift coefficient** and hence, angle of attack. For details on the derivation of these results consult section 4.8 of the course book.           

    """, mathjax=True),
    html.Br(),
    dcc.Markdown(r""" 

    **5. Airfoil Examples**
                 
    In this section you can modify parameters for certain airfoils and observe the changes in the results, all calculations are based on thin-airfoil theory results.                      

    """, mathjax=True),
    
    html.Label("Flap Angle Slider"),
    dcc.Slider(0, 15,
               value=0,
               id="flapAngle",
               marks={0: {'label': "0"},
                           5: {'label': "5"},
                        10: {'label': "10"}, 
                        15: {'label': "15"}}
              ),
    html.Label("Angle of attack Slider"),
    dcc.Slider(0, 15,
               value=0,
               id="angleOfAttack",
               marks={0: {'label': "0"},
                           5: {'label': "5"},
                        10: {'label': "10"}, 
                        15: {'label': "15"}}
              ),

    html.Label("Flap Ratio Slider"),
    dcc.Slider(0, 1,
               value=0.25,
               id="flapRatio",
               marks={0: {'label': "0"},
                           0.25: {'label': "0.25"},
                        0.5: {'label': "0.5"}, 
                        1: {'label': "1"}}
              ),

    html.Label("Freestream Speed Slider"),
    dcc.Slider(0, 30,
               value=15,
               id="freestreamSpeed",
               marks={0: {'label': "0"},
                           10: {'label': "10"},
                        20: {'label': "20"}, 
                        30: {'label': "30"}}
              ),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="flappedAirfoil", mathjax=True),
        ], width=6)
    ], justify='center'),
    
    
    
    ])