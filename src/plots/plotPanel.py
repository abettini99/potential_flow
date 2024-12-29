import numpy as np
import math as math
from matplotlib import path
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff

#Source panel implementation originally from https://github.com/jte0419/Panel_Methods
#Modified by Valter Somlai for the app's purposes

def STREAMLINE_SPM(XP,YP,XB,YB,phi,S):
    
    # Number of panels
    numPan = len(XB)-1                                                          # Number of panels (control points)
    
    # Initialize arrays
    Mx = np.zeros(numPan)                                                       # Initialize Mx integral array
    My = np.zeros(numPan)                                                       # Initialize My integral array
    
    # Compute Mx and My
    for j in range(numPan):                                                     # Loop over all panels
        # Compute intermediate values
        A = -(XP-XB[j])*np.cos(phi[j]) - (YP-YB[j])*np.sin(phi[j])              # A term
        B  = (XP-XB[j])**2 + (YP-YB[j])**2;                                     # B term
        Cx = -np.cos(phi[j]);                                                   # Cx term (X-direction)
        Dx = XP-XB[j];                                                          # Dx term (X-direction)
        Cy = -np.sin(phi[j]);                                                   # Cy term (Y-direction)
        Dy = YP-YB[j];                                                          # Dy term (Y-direction)
        E  = math.sqrt(B-A**2);                                                 # E term
        if (E == 0 or np.iscomplex(E) or np.isnan(E) or np.isinf(E)):           # If E term is 0 or complex or a NAN or an INF
            Mx[j] = 0                                                           # Set Mx value equal to zero
            My[j] = 0                                                           # Set My value equal to zero
        else:
            # Compute Mx, Ref [1]
            term1 = 0.5*Cx*np.log((S[j]**2 + 2*A*S[j]+B)/B);                    # First term in Mx equation
            term2 = ((Dx-A*Cx)/E)*(math.atan2((S[j]+A),E) - math.atan2(A,E));   # Second term in Mx equation
            Mx[j] = term1 + term2;                                              # Compute Mx integral
            
            # Compute My, Ref [1]
            term1 = 0.5*Cy*np.log((S[j]**2 + 2*A*S[j]+B)/B);                    # First term in My equation
            term2 = ((Dy-A*Cy)/E)*(math.atan2((S[j]+A),E) - math.atan2(A,E));   # Second term in My equation
            My[j] = term1 + term2;                                              # Compute My integral

        # Zero out any problem values
        if (np.iscomplex(Mx[j]) or np.isnan(Mx[j]) or np.isinf(Mx[j])):         # If Mx term is complex or a NAN or an INF
            Mx[j] = 0                                                           # Set Mx value equal to zero
        if (np.iscomplex(My[j]) or np.isnan(My[j]) or np.isinf(My[j])):         # If My term is complex or a NAN or an INF
            My[j] = 0                                                           # Set My value equal to zero
    
    return Mx, My                                                               # Return both Mx and My matrices

def COMPUTE_IJ_SPM(XC,YC,XB,YB,phi,S):
    
    # Number of panels
    numPan = len(XC)                                                                # Number of panels/control points
    
    # Initialize arrays
    I = np.zeros([numPan,numPan])                                                   # Initialize I integral matrix
    J = np.zeros([numPan,numPan])                                                   # Initialize J integral matrix
    
    # Compute integral
    for i in range(numPan):                                                         # Loop over i panels
        for j in range(numPan):                                                     # Loop over j panels
            if (j != i):                                                            # If the i and j panels are not the same
                # Compute intermediate values
                A  = -(XC[i]-XB[j])*np.cos(phi[j])-(YC[i]-YB[j])*np.sin(phi[j])     # A term
                B  = (XC[i]-XB[j])**2 + (YC[i]-YB[j])**2                            # B term
                Cn = np.sin(phi[i]-phi[j])                                          # C term (normal)
                Dn = -(XC[i]-XB[j])*np.sin(phi[i])+(YC[i]-YB[j])*np.cos(phi[i])     # D term (normal)
                Ct = -np.cos(phi[i]-phi[j])                                         # C term (tangential)
                Dt = (XC[i]-XB[j])*np.cos(phi[i])+(YC[i]-YB[j])*np.sin(phi[i])      # D term (tangential)
                E  = np.sqrt(B-A**2)                                                # E term
                if (E == 0 or np.iscomplex(E) or np.isnan(E) or np.isinf(E)):       # If E term is 0 or complex or a NAN or an INF
                    I[i,j] = 0                                                      # Set I value equal to zero
                    J[i,j] = 0                                                      # Set J value equal to zero
                else:
                    # Compute I (needed for normal velocity), Ref [1]
                    term1  = 0.5*Cn*np.log((S[j]**2 + 2*A*S[j] + B)/B)              # First term in I equation
                    term2  = ((Dn-A*Cn)/E)*(math.atan2((S[j]+A),E)-math.atan2(A,E)) # Second term in I equation
                    I[i,j] = term1 + term2                                          # Compute I integral
                    
                    # Compute J (needed for tangential velocity), Ref [2]
                    term1  = 0.5*Ct*np.log((S[j]**2 + 2*A*S[j] + B)/B)              # First term in I equation
                    term2  = ((Dt-A*Ct)/E)*(math.atan2((S[j]+A),E)-math.atan2(A,E)) # Second term in I equation
                    J[i,j] = term1 + term2                                          # Compute J integral
                
            # Zero out any problem values
            if (np.iscomplex(I[i,j]) or np.isnan(I[i,j]) or np.isinf(I[i,j])):      # If I term is complex or a NAN or an INF
                I[i,j] = 0                                                          # Set I value equal to zero
            if (np.iscomplex(J[i,j]) or np.isnan(J[i,j]) or np.isinf(J[i,j])):      # If J term is complex or a NAN or an INF
                J[i,j] = 0                                                          # Set J value equal to zero
    
    return I, J                                                                     # Return both I and J matrices

def plotSourceCylinder(alpha, panels, V):
    # User-defined knowns
    Vinf = V                                                                        # Freestream velocity
    AoA  = alpha                                                                    # Angle of attack [deg]
    numB = panels+1                                                             # Number of boundary points (including endpoint)
    tO   = (360/(numB-1))/2                                                         # Boundary point angle offset [deg]
    AoAR = AoA*(np.pi/180)                                                          # Convert AoA to radians [rad]

    # %% CREATE CIRCLE BOUNDARY POINTS

    # Angles used to compute boundary points
    theta = np.linspace(0,360,numB)                                                 # Create angles for computing boundary point locations [deg]
    theta = theta + tO                                                              # Add panel angle offset [deg]
    theta = theta*(np.pi/180)                                                       # Convert from degrees to radians [rad]

    # Boundary points
    XB = np.cos(theta)                                                              # Compute boundary point X-coordinate [radius of 1]
    YB = np.sin(theta)                                                              # Compute boundary point Y-coordinate [radius of 1]

    # Number of panels
    numPan = len(XB)-1                                                              # Number of panels (control points)

    # %% CHECK PANEL DIRECTIONS - FLIP IF NECESSARY

    # Check for direction of points
    edge = np.zeros(numPan)                                                         # Initialize edge value array
    for i in range(numPan):                                                         # Loop over all panels
        edge[i] = (XB[i+1]-XB[i])*(YB[i+1]+YB[i])                                   # Compute edge values

    sumEdge = np.sum(edge)                                                          # Sum of all edge values

    # If panels are CCW, flip them (don't if CW)
    if (sumEdge < 0):                                                               # If panels are CCW
        XB = np.flipud(XB)                                                          # Flip the X-data array
        YB = np.flipud(YB)                                                          # Flip the Y-data array

    # %% PANEL METHOD GEOMETRY - REF [1]

    # Initialize variables
    XC  = np.zeros(numPan)                                                          # Initialize control point X-coordinate
    YC  = np.zeros(numPan)                                                          # Initialize control point Y-coordinate
    S   = np.zeros(numPan)                                                          # Initialize panel length array
    phi = np.zeros(numPan)                                                          # Initialize panel orientation angle array

    # Find geometric quantities of the airfoil
    for i in range(numPan):                                                         # Loop over all panels
        XC[i]   = 0.5*(XB[i]+XB[i+1])                                               # X-value of control point
        YC[i]   = 0.5*(YB[i]+YB[i+1])                                               # Y-value of control point
        dx      = XB[i+1]-XB[i]                                                     # Change in X between boundary points
        dy      = YB[i+1]-YB[i]                                                     # Change in Y between boundary points
        S[i]    = (dx**2 + dy**2)**0.5                                              # Length of the panel
        phi[i]  = math.atan2(dy,dx)                                                 # Angle of panel (positive X-axis to inside face)
        if (phi[i] < 0):                                                            # Make all panel angles positive [rad]
            phi[i] = phi[i] + 2*np.pi

    # Compute angle of panel normal w.r.t. horizontal and include AoA
    delta                = phi + (np.pi/2)                                          # Angle of panel normal [rad]
    beta                 = delta - AoAR                                             # Angle of panel normal and AoA [rad]
    beta[beta > 2*np.pi] = beta[beta > 2*np.pi] - 2*np.pi                           # Make all panel angles between 0 and 2pi [rad]

    # %% COMPUTE SOURCE PANEL STRENGTHS - REF [5]

    # Geometric integral (normal [I] and tangential [J])
    # - Refs [2] and [3]
    I, J = COMPUTE_IJ_SPM(XC,YC,XB,YB,phi,S)                                        # Compute geometric integrals

    # Populate A matrix
    # - Simpler option: A = I + np.pi*np.eye(numPan,numPan)
    A = np.zeros([numPan,numPan])                                                   # Initialize the A matrix
    for i in range(numPan):                                                         # Loop over all i panels
        for j in range(numPan):                                                     # Loop over all j panels
            if (i == j):                                                            # If the panels are the same
                A[i,j] = np.pi                                                      # Set A equal to pi
            else:                                                                   # If panels are not the same
                A[i,j] = I[i,j]                                                     # Set A equal to geometric integral

    # Populate b array
    # - Simpler option: b = -Vinf*2*np.pi*np.cos(beta)
    b = np.zeros(numPan)                                                            # Initialize the b array
    for i in range(numPan):                                                         # Loop over all panels
        b[i] = -Vinf*2*np.pi*np.cos(beta[i])                                        # Compute RHS array

    # Compute source panel strengths (lam) from system of equations
    lam = np.linalg.solve(A,b)                                                      # Compute all source strength values

    # Check the sum of the source strengths
    # - This should be very close to zero for a closed polygon
    #print("Sum of L: ",sum(lam*S))                                                  # Print sum of all source strengths

    # %% COMPUTE PANEL VELOCITIES AND PRESSURE COEFFICIENTS

    # Compute velocities
    # - Simpler method: Vt = Vinf*np.sin(beta) + np.dot(J,lam)/(2*np.pi)
    #                   Cp = 1 - (Vt/Vinf)**2
    Vt = np.zeros(numPan)                                                           # Initialize tangential velocity array
    Cp = np.zeros(numPan)                                                           # Initialize pressure coefficient array
    for i in range(numPan):                                                         # Loop over all i panels
        addVal = 0                                                                  # Reset the summation value to zero
        for j in range(numPan):                                                     # Loop over all j panels
            addVal = addVal + (lam[j]/(2*np.pi))*J[i,j]                             # Sum all tangential source panel terms
        
        Vt[i] = Vinf*np.sin(beta[i]) + addVal                                       # Compute tangential velocity by adding uniform flow term
        Cp[i] = 1 - (Vt[i]/Vinf)**2                                                 # Compute pressure coefficient

    # Analytical angles and pressure coefficients
    analyticTheta = np.linspace(0,2*np.pi,200)                                      # Analytical theta angles [rad]
    analyticCP    = 1 - 4*np.sin(analyticTheta)**2                                  # Analytical pressure coefficient []

    # %% COMPUTE LIFT AND DRAG

    # Compute normal and axial force coefficients
    CN = -Cp*S*np.sin(beta)                                                         # Normal force coefficient []
    CA = -Cp*S*np.cos(beta)                                                         # Axial force coefficient []

    # Compute lift and drag coefficients
    CL = sum(CN*np.cos(AoAR)) - sum(CA*np.sin(AoAR))                                # Decompose axial and normal to lift coefficient []
    CD = sum(CN*np.sin(AoAR)) + sum(CA*np.cos(AoAR))                                # Decompose axial and normal to drag coefficient []

    #print("CL      : ",CL)                                                          # Display lift coefficient (should be zero)
    #print("CD      : ",CD)                                                          # Display drag coefficient (should be zero)

    # %% COMPUTE STREAMLINES - REF [4]

    # Grid parameters
    nGridX   = 100                                                              # X-grid for streamlines and contours
    nGridY   = 100                                                              # Y-grid for streamlines and contours
    xVals    = [-1.5, 1.5]                                                      # X-grid extents [min, max]
    yVals    = [-1.5, 1.5]                                                      # Y-grid extents [min, max]
        
    # Streamline parameters
    slPct  = 30                                                                 # Percentage of streamlines of the grid
    Ysl    = np.linspace(yVals[0],yVals[1],int((slPct/100)*nGridY))             # Create array of Y streamline starting points
    Xsl    = xVals[0]*np.ones(len(Ysl))                                         # Create array of X streamline starting points
    XYsl   = np.vstack((Xsl.T,Ysl.T)).T                                         # Concatenate X and Y streamline starting points
        
    # Generate the grid points
    Xgrid  = np.linspace(xVals[0],xVals[1],nGridX)                              # X-values in evenly spaced grid
    Ygrid  = np.linspace(yVals[0],yVals[1],nGridY)                              # Y-values in evenly spaced grid
    XX, YY = np.meshgrid(Xgrid, Ygrid)                                          # Create meshgrid from X and Y grid arrays
        
    # Initialize velocities
    Vx     = np.zeros([nGridX,nGridY])                                          # Initialize X velocity matrix
    Vy     = np.zeros([nGridX,nGridY])                                          # Initialize Y velocity matrix
        
    # Path to figure out if grid point is inside polygon or not
    AF     = np.vstack((XB.T,YB.T)).T                                           # Concatenate XB and YB geometry points
    afPath = path.Path(AF)                                                      # Create a path for the geometry
        
    # Solve for grid point X and Y velocities
    for m in range(nGridX):                                                     # Loop over X-grid points
        for n in range(nGridY):                                                 # Loop over Y-grid points
            XP     = XX[m,n]                                                    # Isolate X point
            YP     = YY[m,n]                                                    # Isolate Y point
            Mx, My = STREAMLINE_SPM(XP,YP,XB,YB,phi,S)                          # Compute streamline Mx and My values (Ref [4])
                
            # Check if grid points are in object
            # - If they are, assign a velocity of zero
            if afPath.contains_points([(XP,YP)]):                               # If (XP,YP) is in the polygon body
                Vx[m,n] = 0.0007                                                    # X-velocity is zero
                Vy[m,n] = 0.0007                                                   # Y-velocity is zero
            else:                                                               # If (XP,YP) is not in the polygon body
                Vx[m,n] = Vinf*np.cos(AoAR) + sum(lam*Mx/(2*np.pi))             # Compute X-velocity
                Vy[m,n] = Vinf*np.sin(AoAR) + sum(lam*My/(2*np.pi))             # Compute Y-velocity
        
    # Compute grid point velocity magnitude and pressure coefficient
    Vxy  = np.sqrt(Vx**2 + Vy**2)                                               # Compute magnitude of velocity vector
    CpXY = 1 - (Vxy/Vinf)**2                                                    # Pressure coefficient []


    ## ========================== ##
    ## ADD INFORMATION TO FIGUREs ##
    ## ========================== ##

    fig1 = make_subplots(rows=2, cols=2,
                         subplot_titles=("Panel Geometry", "Surface Pressure Distribution", "Pressure Field", "Airflow streamlines"), 
                         horizontal_spacing=0.3
                        )
    
    #Add plots
    fig1.add_trace(go.Scatter(
                name="Complete Panel Geometry",
                x=XB, y=YB,
                mode="lines",  #Plot as a line
                hovertemplate='x = %{x:.4f}'+
                  '<br>y = %{y:.4f}'+
                  '<extra></extra>',
                        ), row=1, col=1)
    
    fig1.add_trace(go.Scatter(
                name="Panel Boundary Points",
                x=XB, y=YB,
                mode='markers',  #Plot as a point
                hovertemplate='x = %{x:.4f}'+
                  '<br>y = %{y:.4f}'+
                  '<extra></extra>',
                        ), row=1, col=1)
    
    fig1.add_trace(go.Scatter(
                name="Panel Control Points",
                x=XC, y=YC,
                mode="markers",  #Plot as a point
                hovertemplate='x = %{x:.4f}'+
                  '<br>y = %{y:.4f}'+
                  '<extra></extra>',
                        ), row=1, col=1)
    
    fig1.add_trace(go.Scatter(
                name="Analytical Surface Pressure Distribution",
                x=analyticTheta*(180/np.pi), y=analyticCP,
                mode='lines',  #Plot as a line
                hovertemplate='x = %{x:.4f}'+
                  '<br>y = %{y:.4f}'+
                  '<extra></extra>',
                        ), row=1, col=2)
    
    fig1.add_trace(go.Scatter(
                name="Numerical Surface Pressure Distribution",
                x=beta*(180/np.pi), y=Cp,
                mode='markers',  #Plot as a point
                hovertemplate='x = %{x:.4f}'+
                  '<br>y = %{y:.4f}'+
                  '<extra></extra>',
                        ), row=1, col=2)
    
    fig1.add_trace(go.Contour(name="Pressure Field",
                              x=Xgrid, y=Ygrid, z=CpXY,
                              colorscale="RdBu_r", zmin=np.min(CpXY), zmax=np.max(CpXY),
                              contours=dict(start=np.min(CpXY),
                                            end  = np.max(CpXY),
                                            size = abs(np.min(CpXY) + np.max(CpXY)) / 100,
                                           ),
                              contours_showlines=False,
                              showscale=False,
                              hovertemplate='x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            '<br>Cp = %{z:.4e}'+
                                            '<extra></extra>', ## '<extra></extra>' removes the trace name from hover text
                             ),
                   row=2, col=1
                  )
    
    #Append streamline
    Vx = np.where(Vx == 0, np.nan, Vx)
    Vy = np.where(Vy == 0, np.nan, Vy)
    streamlines = ff.create_streamline(Xgrid, Ygrid,
                                        Vx, Vy,
                                        density=1,
                                        arrow_scale=0.1,
                                        hoverinfo='skip',
                                        name='streamlines',
                                        line=dict(color='rgba(0,0,0,1)', width=0.75)
                                        )
    for t in streamlines.data:
        fig1.append_trace(t, row=2, col=2)
  
    
    fig1.add_trace(go.Contour(name="Velocity Field",
                              x=Xgrid, y=Ygrid, z=Vxy,
                              colorscale="RdBu_r", zmin=np.min(Vxy), zmax=np.max(Vxy),
                              contours=dict(start=np.min(Vxy),
                                            end  = np.max(Vxy),
                                            size = (np.min(Vxy) + np.max(Vxy)) / 100,
                                           ), 
                              contours_showlines=False,
                              showscale=False,
                              hovertemplate='x = %{x:.4f}'+
                                            '<br>y = %{y:.4f}'+
                                            '<br>Vmag = %{z:.4e}'+
                                            '<extra></extra>', ## '<extra></extra>' removes the trace name from hover text
                             ),
                   row=2, col=2
                  )

    fig1.add_trace(go.Scatter(
                name="Cylinder",
                x=XB, y=YB,
                mode="lines",  #Plot as a line
                fill="toself",
                fillcolor="black",  # Solid black color
                line=dict(color="black"),  # Line color, optional
                opacity=1 , # Fully opaque,
                hovertemplate='x = %{x:.4f}'+
                  '<br>y = %{y:.4f}'+
                  '<extra></extra>',
                        ), row=[2, 2], col=[1, 2])

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

                     )

    fig1.update_xaxes(range=[np.min(Ygrid), np.max(Ygrid)], scaleanchor="x", row=1, col=1)
    fig1.update_yaxes(range=[np.min(Xgrid), np.max(Xgrid)], scaleanchor="y", row=1, col=1)

    fig1.update_xaxes(range=[np.min(Ygrid), np.max(Ygrid)], scaleanchor="x", row=2, col=1)
    fig1.update_yaxes(range=[np.min(Xgrid), np.max(Xgrid)], scaleanchor="y", row=2, col=1)

    fig1.update_xaxes(range=[np.min(Ygrid), np.max(Ygrid)], scaleanchor="x", row=2, col=2)
    fig1.update_yaxes(range=[np.min(Xgrid), np.max(Xgrid)], scaleanchor="y", row=2, col=2)

    #Update figure layout
    fig1.update_layout(font_color='#000000',
                       plot_bgcolor='rgba(255,255,255,1)',
                       paper_bgcolor='rgba(255,255,255,1)',
                       showlegend=False,
                      )

    return fig1