import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff

def plotSource(Lx, Ly, P, strength):
    
    ## ============ ##
    ## SANITY CHECK ##
    ## ============ ##
    if Lx[0] > Lx[1]:
        raise ValueError('Domain endpoints incorrectly defined: Lx[0] > Lx[1]')
    
    if Ly[0] > Ly[1]:
        raise ValueError('Domain endpoints incorrectly defined: Ly[0] > Ly[1]')

    ## ================= ##
    ## MAIN CALCULATIONS ##
    ## ================= ##
    # Create 2D grid, represented using two 1D arrays
    x        = np.linspace(Lx[0], Lx[1], 50)
    y        = np.linspace(Ly[0], Ly[1], 50)
    
    # Get coordinates relative to origin of source
    xP       = x - P[0]
    yP       = y - P[1]

    # Get distance to point for each gridpoint
    XXP, YYP = np.meshgrid(xP,yP)
    r        = np.sqrt(XXP*XXP + YYP*YYP)
    theta    = np.arctan2(YYP, XXP)
    
    # Get velocities
    Vr       = strength/(2*np.pi*r) 
    Vtheta   = 0
    Vmag     = np.sqrt(Vr*Vr + Vtheta*Vtheta)
    Vx       = Vr*np.cos(theta) - Vtheta*np.sin(theta)
    Vy       = Vr*np.sin(theta) + Vtheta*np.cos(theta)
    
    # Get potential + streamfunction
    phi      = strength/(2*np.pi)*np.log(r)
    psi      = strength/(2*np.pi)*theta

    ## ==================== ##
    ## ADD TRACES TO FIGURE ##
    ## ==================== ##
    fig1 = make_subplots(rows=1, cols=3,
                         subplot_titles=('Velocity Magnitude', 'x-Velocity', 'y-Velocity')
                        )
    fig2 = make_subplots(rows=1, cols=2,
                         subplot_titles=('Potential', 'Streamfunction')
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
                              colorscale="RdBu_r", #zmin=-2, zmax=2,
                              #contours=dict(start=-2,
                              #              end  = 2,
                              #              size = 4/10,
                              #             ),
                              contours_showlines=False,
                              showscale=False,
                              hovertemplate='x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            '<br>𝜓 = %{z:.4e}'+
                                            '<extra></extra>', ## '<extra></extra>' removes the trace name from hover text
                             ),
                   row=1, col=2
                  )

    ## Append streamline
    if strength != 0:
        streamlines = ff.create_streamline(x, y,   # for some reason, we need the x-axis reflection, so we need negative y
                                           Vx, Vy, # for some reason, we need the x-axis reflection, so we need negative y
                                           density=1.0,
                                           arrow_scale=0.04,
                                           hoverinfo='skip',
                                           name='streamlines',
                                           line=dict(color='rgba(0,0,0,1)', width=0.75)
                                          )
        for t in streamlines.data:
            fig1.append_trace(t, row=1, col=1)

    ## Add Source Point
    if strength != 0:
        fig1.add_trace(go.Scatter(name=f"Source",
                                  x=[P[0]], y=[P[1]],
                                  mode='markers',
                                  marker=dict(color="green", size=8),
                                  hovertemplate=f'<b>Source</b>'+
                                                 '<br>x = %{x:.4f}'+
                                                 '<br>y = %{y:.4f}'+
                                                f'<br>Strength = {strength:.4e}'+
                                                 '<extra></extra>',
                                  showlegend=False,
                                 ),
                      row=[1,1,1], col=[1,2,3]
                     )
        fig2.add_trace(go.Scatter(name=f"Source",
                                  x=[P[0]], y=[P[1]],
                                  mode='markers',
                                  marker=dict(color="green", size=8),
                                  hovertemplate=f'<b>Source</b>'+
                                                 '<br>x = %{x:.4f}'+
                                                 '<br>y = %{y:.4f}'+
                                                f'<br>Strength = {strength:.4e}'+
                                                 '<extra></extra>',
                                  showlegend=False,
                                 ),
                      row=[1,1], col=[1,2]
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

    return fig1, fig2
