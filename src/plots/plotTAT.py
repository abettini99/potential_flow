import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff

def plotFlappedAirfoil(c, flap_angle, Vinf, flap_ratio, alpha):
    
    ## ================= ##
    ## MAIN CALCULATIONS ##
    ## ================= ##

    #c = airfoil chord
    #flap_angle = angle of the flap (small angle approximation)
    #flap_ratio = ratio of the length along the x axis of the flap chord length versus the total chord
    #alpha = angle of attack

    alpha = alpha * (2*np.pi / 360) #Convert to radians
    flap_angle = flap_angle * (2*np.pi / 360) #Convert to radians

    #Create the airfoil shape
    x_unflapped = np.linspace(0.1, c*(1-flap_ratio), 50)
    x_flapped = np.linspace(c*(1-flap_ratio), c, 50)
    x = np.concatenate((x_unflapped, x_flapped))

    camber_unflapped = x_unflapped * 0
    camber_flapped = -flap_angle*x_flapped + flap_angle*c*(1-flap_ratio)
    camber_line = np.concatenate((camber_unflapped, camber_flapped))

    x_rotated = np.cos(-alpha) * x - np.sin(-alpha) * camber_line
    camber_line_rotated = np.sin(-alpha) * x + np.cos(-alpha) * camber_line

    theta_flap = np.arccos(1 - 2*(1-flap_ratio)) #Theta coordinate of the point where the flap begins

    #Calculate the camber line constants
    A = np.zeros(1000) #Contains the constants
    A[0] = alpha + (flap_angle/np.pi)*(np.pi - theta_flap)
    for i in range(1, 1000):
        A[i] = (2/np.pi)*(-flap_angle/i)*(np.sin(i*np.pi) - np.sin(i*theta_flap))

    #Calculate pressure difference distribution (lift distribution)
    
    def sine_fourier(A, theta): #Function to calculate the Fourier Sine Series sum at each theta coordinate
        AFS = 0
        for j in range(len(A)):
            AFS += A[j]*np.sin(j*theta)
        return AFS

    theta_coordinates = np.arccos(1-(2/c)*x) #Coordinate transformation
    delta_cp = np.zeros(len(theta_coordinates)) #Array for the pressure difference distribution
    for k in range(len(theta_coordinates)):
        AFS = sine_fourier(A, theta_coordinates[k])
        delta_cp[k] = 4*((alpha + (flap_angle/np.pi)*(np.pi - theta_flap))*((1+np.cos(theta_coordinates[k]))/(np.sin(theta_coordinates[k]))) + AFS)

    #Calculate airfoil coefficients

    cl = 2*np.pi*(A[0]+0.5*A[1])
    cm = (np.pi/4)*(A[2]-A[1])
    xcp = c*(0.25-(cm/cl))
    xcp_rotated = [np.cos(-alpha) * xcp - np.sin(-alpha) * 0]
    ycp_rotated = [np.sin(-alpha) * xcp + np.cos(-alpha) * 0]

    coefficients_names = ["Cl", "Cm(c/4)"]
    coefficient_values = [cl, cm]

    ## ========================== ##
    ## ADD INFORMATION TO FIGUREs ##
    ## ========================== ##

    fig1 = make_subplots(rows=1, cols=3,
                         subplot_titles=("Flapped Airfoil Camber Line", "Pressure Difference Distribution", "Airfoil Coefficients"), 
                         horizontal_spacing=0.4
                        )
    
    #Add plots
    fig1.add_trace(go.Scatter(
                name="Flapped Airfoil Camber Line Position",
                x=x_rotated, y=camber_line_rotated,
                mode='lines',  #Plot as a line
                hovertemplate='x = %{x:.4f}'+
                  '<br>y = %{y:.4f}'+
                  '<extra></extra>',
                        ), row=1, col=1)
    
    fig1.add_trace(go.Scatter(
                name="Flapped Airfoil Center of Pressure",
                x=xcp_rotated, y=ycp_rotated,
                mode="markers",  #Plot as a point
                hovertemplate='x = %{x:.4f}'+
                  '<br>y = %{y:.4f}'+
                  '<extra></extra>',
                        ), row=1, col=1)

    fig1.add_trace(go.Scatter(
                name="Pressure Difference Distribution",
                x=x/c, y=delta_cp,
                mode='lines',  #Plot as a line
                hovertemplate='x = %{x:.4f}'+
                  '<br>y = %{y:.4f}'+
                  '<extra></extra>',
                        ), row=1, col=2)
    
    fig1.add_trace(go.Bar(
                    x=coefficients_names,  # X-axis categories
                    y=coefficient_values,      # Y-axis values
                    name="Airfoil Coefficients",  # Trace name
                    ), row=1, col=3
)

    #Update x-axis properties
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
                      range=[0, 1], 
                      row=1, col=1
                     )
    
    #Update y-axis properties
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
                      range=[-1, 1], 
                      row=1, col=1
                     )
    
    #Update figure layout
    fig1.update_layout(font_color='#000000',
                       plot_bgcolor='rgba(255,255,255,1)',
                       paper_bgcolor='rgba(255,255,255,1)',
                       height=500,
                       width=900,
                       showlegend=False,
                      )
    return fig1