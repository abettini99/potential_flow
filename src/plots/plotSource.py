import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plotSource(Lx, Ly, strength):
    
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

    ## ==================== ##
    ## ADD TRACES TO FIGURE ##
    ## ==================== ##
    fig1 = make_subplots(rows=1, cols=1,
                        subplot_titles=('Velocity Contours')
                       )
    fig2 = make_subplots(rows=1, cols=1,
                        subplot_titles=('Potential Plot')
                       )

    return fig1, fig2
