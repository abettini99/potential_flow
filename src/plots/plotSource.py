import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
    x = np.linspace(Lx[0], Lx[1], 50)
    y = np.linspace(Ly[0], Ly[1], 50)
    
    # Get coordinates relative to origin of source
    xP = x - P[0]
    yP = y - P[0]

    # Get distance to point for each gridpoint
    XXP, YYP = np.meshgrid(xP,yP)
    r        = np.sqrt(XXP*XXP + YYP*YYP)
    
    # Get velocities
    Vr       = strength/(2*np.pi*r) 
    Vx       = Vr * XXP/r 
    Vy       = Vr * YYP/r 

    ## ==================== ##
    ## ADD TRACES TO FIGURE ##
    ## ==================== ##
    fig1 = make_subplots(rows=1, cols=3,
                         subplot_titles=('Radial Velocity', 'x-Velocity', 'y-Velocity')
                        )
    ## Add Contours
    fig1.add_trace(go.Contour(name="Radial Velocity",
                              x=x, y=y, z=Vr,
                              colorscale="RdBu_r", zmin=-2, zmax=2,
                              contours=dict(start=-2,
                                            end  = 2,
                                            size = 4/10,
                                           ),
                              contours_showlines=False,
                              showscale=False,
                              hovertemplate='x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            '<br>Vr = %{z:.4e}'+
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

    ## Add Source Point
    fig1.add_trace(go.Scatter(name=f"Source",
                              x=[P[0]], y=[P[1]],
                              marker=dict(color="green",
                                          size=8
                                         ),
                              hovertemplate=f'<b>Source</b>'+
                                            '<br>x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            f'<br>strength = {strength:.4e}'+
                                            '<extra></extra>',
                              showlegend=False,
                             ),
                   row=[1,1,1], col=[1,2,3]
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
                      #scaleanchor='y',
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
    
    ## Update figure layout
    fig1.update_layout(font_color='#000000',
                       plot_bgcolor='rgba(255,255,255,1)',
                       paper_bgcolor='rgba(255,255,255,1)',
                       #width=1400,
                       height=500,
                       showlegend=False,
                      )





    fig2 = make_subplots(rows=1, cols=1,
                         subplot_titles=('Potential Plot')
                        )

    return fig1, fig2
