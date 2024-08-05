import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff

def plotCylinder(Lx, Ly, Vinf, cylinderRadius):
    
    ## ============ ##
    ## SANITY CHECK ##
    ## ============ ##
    if Lx[0] > Lx[1]:
        raise ValueError('Domain endpoints incorrectly defined: Lx[0] > Lx[1]')
    
    if Ly[0] > Ly[1]:
        raise ValueError('Domain endpoints incorrectly defined: Ly[0] > Ly[1]')

    if Vinf < 0:
        raise ValueError('Freestream Velocity Magnitude is negative!')
    
    if cylinderRadius < 0:
        raise ValueError('Cylinder radius is negative!')
    
    ## ================= ##
    ## MAIN CALCULATIONS ##
    ## ================= ##
    # Create 2D grid, represented using two 1D arrays
    x = np.linspace(Lx[0], Lx[1], 50)
    y = np.linspace(Ly[0], Ly[1], 50)
    
    # Get distance to point for each gridpoint
    XX, YY   = np.meshgrid(x,y)
    r        = np.sqrt(XX*XX + YY*YY)
    theta    = np.arctan2(YY, XX)

    # Get velocities
    Vr       =  (1 - cylinderRadius*cylinderRadius/(r*r))*Vinf*np.cos(theta)
    Vtheta   = -(1 + cylinderRadius*cylinderRadius/(r*r))*Vinf*np.sin(theta)
    Vmag     = np.sqrt(Vr*Vr + Vtheta*Vtheta)
    Vx       = Vr*np.cos(theta) - Vtheta*np.sin(theta)
    Vy       = Vr*np.sin(theta) + Vtheta*np.cos(theta)
    
    # Get potential + streamfunction
    phi      = Vinf*r*np.cos(theta)*(1+cylinderRadius*cylinderRadius/(r*r))
    psi      = Vinf*r*np.sin(theta)*(1-cylinderRadius*cylinderRadius/(r*r))

    # Get body surface (determined by streamline in which stagnation point occurs)
    # We also inject the stagnation point into array after the procedure
    n        = 250
    thetaS   = np.linspace(0+1e-6, 2*np.pi-1e-6, n)
    rS       = cylinderRadius*np.ones(n) # Fairly simple for a cylinder
    # Inject the two stagnation points (and repeat it at 2pi to make a closed loop)
    thetaS   = np.append(thetaS, 0)
    rS       = np.append(rS, cylinderRadius)
    thetaS   = np.append(thetaS, np.pi)
    rS       = np.append(rS, cylinderRadius)
    thetaS   = np.append(thetaS, 2*np.pi)
    rS       = np.append(rS, cylinderRadius)
    # Sort injected variable to correct spot
    idx      = np.argsort(thetaS)
    thetaS   = thetaS[idx]
    rS       = rS[idx]

    # Get quantities along body contour
    xS       = rS*np.cos(thetaS)
    yS       = rS*np.sin(thetaS)
         
    VrS      =  (1 - cylinderRadius*cylinderRadius/(rS*rS))*Vinf*np.cos(thetaS)
    VthetaS  = -(1 + cylinderRadius*cylinderRadius/(rS*rS))*Vinf*np.sin(thetaS)
    VmagS    = np.sqrt(VrS*VrS + VthetaS*VthetaS)
    VxS      = VrS*np.cos(thetaS) - VthetaS*np.sin(thetaS)
    VyS      = VrS*np.sin(thetaS) + VthetaS*np.cos(thetaS)
    # phiS     = Vinf*rS*np.cos(thetaS) + sourceStrength/(2*np.pi) * np.log(rS)
    # psiS     = Vinf*rS*np.sin(thetaS) + sourceStrength/(2*np.pi) * thetaS
    CpS      = 1 - VmagS*VmagS/(Vinf*Vinf)

    ## ==================== ##
    ## ADD TRACES TO FIGURE ##
    ## ==================== ##
    fig1 = make_subplots(rows=1, cols=3,
                         subplot_titles=('Velocity Magnitude', 'x-Velocity', 'y-Velocity')
                        )
    fig2 = make_subplots(rows=1, cols=2,
                         subplot_titles=('Potential', 'Streamfunction')
                        )
    fig3 = make_subplots(rows=1, cols=2,
                         subplot_titles=('Velocity(theta)', 'Velocity(x)')
                        )
    fig4 = make_subplots(rows=1, cols=2,
                         subplot_titles=('Cp(theta)', 'Cp(x)')
                        )
    
    ## Add Contours
    fig1.add_trace(go.Contour(name="Velocity Magnitude",
                              x=x, y=y, z=Vmag,
                              colorscale="RdBu_r", zmin=-2, zmax=2,
                              contours=dict(start=-2,
                                            end  = 2,
                                            size = 4/10,
                                           ),
                              contours_showlines=False,
                              showscale=False,
                              hovertemplate='x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            '<br>Vmag = %{z:.4e}'+
                                            '<extra></extra>', ## '<extra></extra>' removes the trace name from hover text
                             ),
                   row=1, col=1
                  )
    fig1.add_trace(go.Contour(name="x-Velocity",
                              x=x, y=y, z=Vx,
                              colorscale="RdBu_r", zmin=-2, zmax=2,
                              contours=dict(start=-2,
                                            end  = 2,
                                            size = 4/10,
                                           ),
                              contours_showlines=False,
                              showscale=False,
                              hovertemplate='x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            '<br>Vx = %{z:.4e}'+
                                            '<extra></extra>', ## '<extra></extra>' removes the trace name from hover text
                             ),
                      row=1, col=2
                     )
    fig1.add_trace(go.Contour(name="y-Velocity",
                              x=x, y=y, z=Vy,
                              colorscale="RdBu_r", zmin=-2, zmax=2,
                              contours=dict(start=-2,
                                            end  = 2,
                                            size = 4/10,
                                           ),
                              contours_showlines=False,
                              showscale=False,
                              hovertemplate='x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            '<br>Vy = %{z:.4e}'+
                                            '<extra></extra>', ## '<extra></extra>' removes the trace name from hover text
                             ),
                      row=1, col=3
                     )
    fig2.add_trace(go.Contour(name="Potential",
                              x=x, y=y, z=phi,
                              colorscale="RdBu_r", zmin=-2, zmax=2,
                              contours=dict(start=-4,
                                            end  = 4,
                                            size = 4/10,
                                           ),
                              contours_showlines=False,
                              showscale=False,
                              hovertemplate='x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            '<br>φ = %{z:.4e}'+
                                            '<extra></extra>', ## '<extra></extra>' removes the trace name from hover text
                             ),
                   row=1, col=1
                  )
    fig2.add_trace(go.Contour(name="Streamfunction",
                              x=x, y=y, z=psi,
                              colorscale="RdBu_r", zmin=-2, zmax=2,
                              contours=dict(start=-2,
                                            end  = 2,
                                            size = 4/10,
                                           ),
                              contours_showlines=False,
                              showscale=False,
                              hovertemplate='x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            '<br>𝜓 = %{z:.4e}'+
                                            '<extra></extra>', ## '<extra></extra>' removes the trace name from hover text
                             ),
                   row=1, col=2
                  )
    fig3.add_trace(go.Scatter(name=f"x-Velocity",
                              x=thetaS, y=VxS,
                              mode='lines',
                              line=dict(color='#ff0000', width=1.25),
                              hovertemplate='%{y:.4f}',
                              showlegend=False,
                             ),
                row=[1], col=[1]
                )
    fig3.add_trace(go.Scatter(name=f"y-Velocity",
                              x=thetaS, y=VyS,
                              mode='lines',
                              line=dict(color='#0000ff', width=1.25),
                              hovertemplate='%{y:.4f}',
                              showlegend=False,
                             ),
                row=[1], col=[1]
                )
    fig3.add_trace(go.Scatter(name=f"Velocity Magnitude",
                              x=thetaS, y=VmagS,
                              mode='lines',
                              line=dict(color='#000000'),
                              hovertemplate='%{y:.4f}',
                              showlegend=False,
                             ),
                row=[1], col=[1]
                )
    fig3.add_trace(go.Scatter(name=f"x-Velocity",
                              x=xS[thetaS <= np.pi], y=VxS[thetaS <= np.pi],
                              mode='lines',
                              line=dict(color='#ff0000', width=1.25),
                              hovertemplate='%{y:.4f}',
                              showlegend=False,
                             ),
                row=[1], col=[2]
                )
    fig3.add_trace(go.Scatter(name=f"y-Velocity",
                              x=xS[thetaS <= np.pi], y=VyS[thetaS <= np.pi],
                              mode='lines',
                              line=dict(color='#0000ff', width=1.25),
                              hovertemplate='±%{y:.4f}',
                              showlegend=False,
                             ),
                row=[1], col=[2]
                )
    fig3.add_trace(go.Scatter(name=f"Velocity Magnitude",
                              x=xS[thetaS <= np.pi], y=VmagS[thetaS <= np.pi],
                              mode='lines',
                              line=dict(color='#000000'),
                              hovertemplate='%{y:.4f}',
                              showlegend=False,
                             ),
                row=[1], col=[2]
                )
    
    fig4.add_trace(go.Scatter(name=f"Pressure Coefficient",
                              x=thetaS, y=CpS,
                              customdata=xS,
                              mode='lines',
                              line=dict(color='#000000'),
                              hovertemplate=f'<b>Pressure Coefficient</b>'+
                                             '<br>𝜃 = %{x:.4f}'+
                                             '<br>x = %{customdata:.4f}'+
                                             '<br>Cp = %{y:.4f}'+
                                             '<extra></extra>',
                              showlegend=False,
                             ),
                row=[1], col=[1]
                )
    fig4.add_trace(go.Scatter(name=f"Pressure Coefficient",
                              x=xS[thetaS <= np.pi], y=CpS[thetaS <= np.pi],
                              customdata=np.stack((thetaS[thetaS <= np.pi], thetaS[thetaS >= np.pi]), axis=-1),
                              mode='lines',
                              line=dict(color='#000000'),
                              hovertemplate=f'<b>Pressure Coefficient</b>'+
                                             '<br>x = %{x:.4f}'+
                                             '<br>𝜃 = %{customdata[0]:.4f} OR %{customdata[1]:.4f}'+
                                             '<br>Cp = %{y:.4f}'+
                                             '<extra></extra>',
                              showlegend=False,
                             ),
                row=[1], col=[2]
                )

    # Append streamline
    streamlines = ff.create_streamline(x, y,
                                       Vx, Vy,
                                       density=1.0,
                                       arrow_scale=0.04,
                                       hoverinfo='skip',
                                       name='streamlines',
                                       line=dict(color='rgba(0,0,0,1)', width=0.75)
                                      )
    for t in streamlines.data:
        fig1.append_trace(t, row=1, col=1)

    ## Add body contour
    if cylinderRadius != 0:
        fig1.add_trace(go.Scatter(name=f"Body Contour",
                                  x=xS, y=yS,
                                  mode='lines',
                                  line=dict(color='#000000'),
                                  hovertemplate=f'<b>Body Contour</b>'+
                                                 '<br>x = %{x:.4f}'+
                                                 '<br>y = %{y:.4f}'+
                                                 '<extra></extra>',
                                  showlegend=False,
                                  fill="toself",
                                  fillcolor='#ffffff',
                                  fillpattern=dict(fgcolor='lightgray', shape="x", size=8),
                                 ),
                   row=[1,1,1], col=[1,2,3]
                  )
        fig2.add_trace(go.Scatter(name=f"Body Contour",
                                  x=xS, y=yS,
                                  mode='lines',
                                  line=dict(color='#000000'),
                                  hovertemplate=f'<b>Body Contour</b>'+
                                                 '<br>x = %{x:.4f}'+
                                                 '<br>y = %{y:.4f}'+
                                                 '<extra></extra>',
                                  showlegend=False,
                                  fill="toself",
                                  fillcolor='#ffffff',
                                  fillpattern=dict(fgcolor='lightgray', shape="x", size=8),
                                 ),
                       row=[1,1,1], col=[1,2]
                      )

    ## Add Doublet Point
    if cylinderRadius != 0:
        fig1.add_trace(go.Scatter(name=f"Doublet",
                                  x=[0], y=[0],
                                  mode='markers',
                                  marker=dict(color="green", size=8),
                                  hovertemplate=f'<b>Doublet</b>'+
                                                 '<br>x = %{x:.4f}'+
                                                 '<br>y = %{y:.4f}'+
                                                f'<br>Strength = {(cylinderRadius**2 * 2*np.pi*Vinf):.4e}'+
                                                 '<extra></extra>',
                                  showlegend=False,
                                ),
                       row=[1,1,1], col=[1,2,3]
                      )
        fig2.add_trace(go.Scatter(name=f"Doublet",
                                  x=[0], y=[0],
                                  mode='markers',
                                  marker=dict(color="green", size=8),
                                  hovertemplate=f'<b>Doublet</b>'+
                                                 '<br>x = %{x:.4f}'+
                                                 '<br>y = %{y:.4f}'+
                                                f'<br>Strength = {(cylinderRadius**2 * 2*np.pi*Vinf):.4e}'+
                                                 '<extra></extra>',
                                  showlegend=False,
                                 ),
                       row=[1,1], col=[1,2]
                      )
    
    ## Add Stagnation Point
    if cylinderRadius != 0:
        fig1.add_trace(go.Scatter(name=f"Stagnation Point",
                                  x=[cylinderRadius, -cylinderRadius],
                                  y=[0, 0],
                                  mode='markers',
                                  marker=dict(color="blue", size=8),
                                  hovertemplate=f'<b>Stagnation Point</b>'+
                                                 '<br>x = %{x:.4f}'+
                                                 '<br>y = %{y:.4f}'+
                                                 '<extra></extra>',
                                  showlegend=False,
                                 ),
                       row=[1,1,1], col=[1,2,3]
                      )
        fig2.add_trace(go.Scatter(name=f"Stagnation Point",
                                  x=[cylinderRadius, -cylinderRadius],
                                  y=[0, 0],
                                  mode='markers',
                                  marker=dict(color="blue", size=8),
                                  hovertemplate=f'<b>Stagnation Point</b>'+
                                                 '<br>x = %{x:.4f}'+
                                                 '<br>y = %{y:.4f}'+
                                                 '<extra></extra>',
                                  showlegend=False,
                                 ),
                       row=[1,1], col=[1,2]
                      )
        fig3.add_trace(go.Scatter(name=f"Stagnation Point",
                                  x=[0,np.pi,2*np.pi], y=[0,0,0],
                                  mode='markers',
                                  marker=dict(color="blue", size=8),
                                  hoverinfo='skip',
                                  showlegend=False,
                                 ),
                       row=[1], col=[1]
                      )
        fig3.add_trace(go.Scatter(name=f"Stagnation Point",
                                  x=[cylinderRadius, -cylinderRadius],
                                  y=[0,0],
                                  mode='markers',
                                  marker=dict(color="blue", size=8),
                                  hoverinfo='skip',
                                  showlegend=False,
                                 ),
                       row=[1], col=[2]
                      )
        fig4.add_trace(go.Scatter(name=f"Stagnation Point",
                                  x=[0,np.pi,2*np.pi], y=[1,1,1],
                                  mode='markers',
                                  marker=dict(color="blue", size=8),
                                  hoverinfo='skip',
                                  showlegend=False,
                                 ),
                       row=[1], col=[1]
                      )
        fig4.add_trace(go.Scatter(name=f"Stagnation Point",
                                  x=[cylinderRadius, -cylinderRadius],
                                  y=[1,1],
                                  mode='markers',
                                  marker=dict(color="blue", size=8),
                                  hoverinfo='skip',
                                  showlegend=False,
                                 ),
                       row=[1], col=[2]
                      )
        
    ## Update x-axis properties
    fig1.update_xaxes(#title_text='x',
                      title_font_color='#000000',
                      title_standoff=0,
                      gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB
                      gridwidth=1,
                      zerolinecolor='#000000',
                      zerolinewidth=2,
                      linecolor='#000000',
                      linewidth=1,
                      ticks='outside',
                      ticklen=10,
                      tickwidth=2,
                      tickcolor='#000000',
                      tickfont_color='#000000',
                      minor_showgrid=True,
                      minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                      minor_ticks='outside',
                      minor_ticklen=5,
                      minor_tickwidth=2,
                      minor_griddash='dot',
                      hoverformat='.4f',
                      range=[x.min(),x.max()],
                     )
    fig2.update_xaxes(#title_text='x',
                      title_font_color='#000000',
                      title_standoff=0,
                      gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB
                      gridwidth=1,
                      zerolinecolor='#000000',
                      zerolinewidth=2,
                      linecolor='#000000',
                      linewidth=1,
                      ticks='outside',
                      ticklen=10,
                      tickwidth=2,
                      tickcolor='#000000',
                      tickfont_color='#000000',
                      minor_showgrid=True,
                      minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                      minor_ticks='outside',
                      minor_ticklen=5,
                      minor_tickwidth=2,
                      minor_griddash='dot',
                      hoverformat='.4f',
                      range=[x.min(),x.max()],
                     )
    fig3.update_xaxes(#title_text='x',
                      title_font_color='#000000',
                      title_standoff=0,
                      gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB
                      gridwidth=1,
                      zerolinecolor='#000000',
                      zerolinewidth=2,
                      linecolor='#000000',
                      linewidth=1,
                      ticks='outside',
                      ticklen=10,
                      tickwidth=2,
                      tickcolor='#000000',
                      tickfont_color='#000000',
                      minor_showgrid=True,
                      minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                      minor_ticks='outside',
                      minor_ticklen=5,
                      minor_tickwidth=2,
                      minor_griddash='dot',
                      hoverformat='.4f',
                     )
    fig3.update_layout(xaxis2 = dict(range=[-1,1])) # Update axes of only one graph
    fig4.update_xaxes(#title_text='x',
                      title_font_color='#000000',
                      title_standoff=0,
                      gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB
                      gridwidth=1,
                      zerolinecolor='#000000',
                      zerolinewidth=2,
                      linecolor='#000000',
                      linewidth=1,
                      ticks='outside',
                      ticklen=10,
                      tickwidth=2,
                      tickcolor='#000000',
                      tickfont_color='#000000',
                      minor_showgrid=True,
                      minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                      minor_ticks='outside',
                      minor_ticklen=5,
                      minor_tickwidth=2,
                      minor_griddash='dot',
                      hoverformat='.4f',
                     )
    fig4.update_layout(xaxis2 = dict(range=[-1,1])) # Update axes of only one graph

    ## Update y-axis properties
    fig1.update_yaxes(#title_text='y',
                      title_font_color='#000000',
                      title_standoff=0,
                      gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB, 0.75 opacity
                      gridwidth=1,
                      zerolinecolor='#000000',
                      zerolinewidth=2,
                      linecolor='#000000',
                      linewidth=1,
                      ticks='outside',
                      ticklen=10,
                      tickwidth=2,
                      tickcolor='#000000',
                      tickfont_color='#000000',
                      minor_showgrid=True,
                      minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                      minor_ticks='outside',
                      minor_ticklen=5,
                      minor_tickwidth=2,
                      minor_griddash='dot',
                      range=[y.min(),y.max()],
                     )
    fig2.update_yaxes(#title_text='y',
                      title_font_color='#000000',
                      title_standoff=0,
                      gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB, 0.75 opacity
                      gridwidth=1,
                      zerolinecolor='#000000',
                      zerolinewidth=2,
                      linecolor='#000000',
                      linewidth=1,
                      ticks='outside',
                      ticklen=10,
                      tickwidth=2,
                      tickcolor='#000000',
                      tickfont_color='#000000',
                      minor_showgrid=True,
                      minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                      minor_ticks='outside',
                      minor_ticklen=5,
                      minor_tickwidth=2,
                      minor_griddash='dot',
                      range=[y.min(),y.max()],
                     )
    fig3.update_yaxes(#title_text='y',
                      title_font_color='#000000',
                      title_standoff=0,
                      gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB, 0.75 opacity
                      gridwidth=1,
                      zerolinecolor='#000000',
                      zerolinewidth=2,
                      linecolor='#000000',
                      linewidth=1,
                      ticks='outside',
                      ticklen=10,
                      tickwidth=2,
                      tickcolor='#000000',
                      tickfont_color='#000000',
                      minor_showgrid=True,
                      minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                      minor_ticks='outside',
                      minor_ticklen=5,
                      minor_tickwidth=2,
                      minor_griddash='dot',
                      #range=[y.min(),y.max()],
                     )
    fig4.update_yaxes(#title_text='y',
                      title_font_color='#000000',
                      title_standoff=0,
                      gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB, 0.75 opacity
                      gridwidth=1,
                      zerolinecolor='#000000',
                      zerolinewidth=2,
                      linecolor='#000000',
                      linewidth=1,
                      ticks='outside',
                      ticklen=10,
                      tickwidth=2,
                      tickcolor='#000000',
                      tickfont_color='#000000',
                      minor_showgrid=True,
                      minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                      minor_ticks='outside',
                      minor_ticklen=5,
                      minor_tickwidth=2,
                      minor_griddash='dot',
                      #range=[y.min(),y.max()],
                     )
    
    ## Update figure layout
    fig1.update_layout(font_color='#000000',
                       plot_bgcolor='rgba(255,255,255,1)',
                       paper_bgcolor='rgba(255,255,255,1)',
                       showlegend=False,
                      )
    fig2.update_layout(font_color='#000000',
                       plot_bgcolor='rgba(255,255,255,1)',
                       paper_bgcolor='rgba(255,255,255,1)',
                       showlegend=False,
                      )
    fig3.update_layout(font_color='#000000',
                       plot_bgcolor='rgba(255,255,255,1)',
                       paper_bgcolor='rgba(255,255,255,1)',
                       hovermode='x unified',
                       showlegend=False,
                      )
    fig4.update_layout(font_color='#000000',
                       plot_bgcolor='rgba(255,255,255,1)',
                       paper_bgcolor='rgba(255,255,255,1)',
                       showlegend=False,
                      )
    
    return fig1, fig2, fig3, fig4

