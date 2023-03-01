import numpy as np
import plotly as ply
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from src.commondicts import TYPE_NAME_DICT, LONG_NAME_DICT
from src.commonfuncs import flow_element_type
import potentialflowvisualizer as pfv

pio.renderers.default = (
    "browser"  # Feel free to disable this if you're running in notebook mode or prefer a different frontend.
)

def line_color(object):
    try:
        color = "green" if object.strength > 0 else "red"
    except AttributeError:
        color = "black"

    return color

def dot_size(object):
    try:
        strength = abs(object.strength) / 10
    except AttributeError:
        strength = 1

    return 10 + np.tanh(strength) * 10

def line_width(object):
    try:
        strength = abs(object.strength) / 10
    except AttributeError:
        strength = 1

    return 10 + np.tanh(strength) * 10


class Flowfield:
    def __init__(self, objects=[]):
        self.objects = objects

    def draw(self,
             scalar_to_plot="potential",  # "potential", "streamfunction", "xvel", "yvel", "velmag"
             x_points=np.linspace(-10, 10, 200),
             y_points=np.linspace(-10, 10, 200),
             show=True,
             colorscheme="Viridis",
             n_contour_lines=40,
             plot_flow_elements=False,
            ):

        ## System variables
        X, Y    = np.meshgrid(x_points, y_points)
        X_r     = np.reshape(X, -1)
        Y_r     = np.reshape(Y, -1)
        points  = np.vstack((X_r, Y_r)).T

        scalar_to_plot_value = np.zeros_like(X_r)
        if scalar_to_plot == "velmag":
            x_vels          = np.zeros_like(X_r)
            y_vels          = np.zeros_like(X_r)
            streamfunction  = np.zeros_like(X_r)
        elif scalar_to_plot == "pressure":
            x_vels          = np.zeros_like(X_r)
            y_vels          = np.zeros_like(X_r)
            u_cumulative    = 0
            v_cumulative    = 0
            V2_infty        = 1

        ## Get plotting values
        for object in self.objects:
            if scalar_to_plot == "potential":
                scalar_to_plot_value += object.get_potential_at(points)
            elif scalar_to_plot == "streamfunction":
                scalar_to_plot_value += object.get_streamfunction_at(points)
            elif scalar_to_plot == "xvel":
                scalar_to_plot_value += object.get_x_velocity_at(points)
            elif scalar_to_plot == "yvel":
                scalar_to_plot_value += object.get_y_velocity_at(points)
            elif scalar_to_plot == "velmag":
                x_vels += object.get_x_velocity_at(points)
                y_vels += object.get_y_velocity_at(points)

                streamfunction += object.get_streamfunction_at(points)
                scalar_to_plot_value = np.sqrt(x_vels**2 + y_vels**2) ## Gets overwritten

                min2 = np.nanpercentile(streamfunction, 5)
                max2 = np.nanpercentile(streamfunction, 95)
            elif scalar_to_plot == "pressure":
                x_vels += object.get_x_velocity_at(points)
                y_vels += object.get_y_velocity_at(points)
                V2      = x_vels**2 + y_vels**2                      ## Gets overwritten

                if flow_element_type(object) == "Uniform":
                    u_cumulative += object.u
                    v_cumulative += object.v
                    V2_infty      = u_cumulative**2 + v_cumulative**2
                    if V2_infty == 0: V2_infty = 1

                scalar_to_plot_value = 1 - V2/V2_infty

            else:
                raise Exception

        ## Calculate percentiles used to display graphs
        min = np.nanpercentile(scalar_to_plot_value, 5)
        max = np.nanpercentile(scalar_to_plot_value, 95)

        #### ================ ####
        #### Plotting Routine ####
        #### ================ ####
        fig = make_subplots(rows=1, cols=1,
                            subplot_titles=(LONG_NAME_DICT[scalar_to_plot],)
                           )
        if len(self.objects) == 0:
            return fig

        ## Plot contours
        if scalar_to_plot == "velmag":
                fig.add_trace(go.Contour(name=LONG_NAME_DICT[scalar_to_plot],
                                         x=x_points, y=y_points, z=np.reshape(scalar_to_plot_value, X.shape),
                                         colorscale=colorscheme,
                                         contours=dict(start=min,
                                                       end=max,
                                                       size=(max - min) / n_contour_lines,
                                                      ),
                                         contours_showlines=False,
                                         showscale=False,
                                         hovertemplate='x = %{x:.4f}'+
                                                       '<br>y = %{y:.4f}'+
                                                       '<br>f(x,y) = %{z:.4e}'+
                                                       '<extra></extra>', ## '<extra></extra>' removes the trace name from hover text
                                         # colorbar=dict(ticks     = "inside",
                                         #               len       = 1,                          ## vertical height of colorbar, expressed in a fraction of graph height, final height reduced by ypad
                                         #               ypad      = 0,                          ## y-padding of colorbar, reduces colorbar height
                                         #               tickwidth = 2,
                                         #               ticklen   = 10
                                         #              ),
                                        ),
                              row=1, col=1
                             )
                fig.add_trace(go.Contour(x=x_points, y=y_points, z=np.reshape(streamfunction, X.shape),
                             colorscale=[[0,'#000000'],[1,'#000000']],
                             contours=dict(start=min2,
                                           end=max2,
                                           size=(max2 - min2) / n_contour_lines,
                                          ),
                             showscale=False,
                             contours_coloring='lines',
                             hoverinfo='skip'
                            ),
                  row=1, col=1
                 )
        elif scalar_to_plot == "pressure":
            fig.add_trace(go.Contour(name=LONG_NAME_DICT[scalar_to_plot],
                                     x=x_points, y=y_points, z=np.reshape(scalar_to_plot_value, X.shape),
                                     colorscale=colorscheme,
                                     contours=dict(start=min,
                                                   end=max,
                                                   size=(max - min) / n_contour_lines,
                                                  ),
                                     contours_showlines=False,
                                     showscale=False,
                                     hovertemplate='x = %{x:.4f}'+
                                                   '<br>y = %{y:.4f}'+
                                                   '<br>f(x,y) = %{z:.4e}'+
                                                   '<extra></extra>',
                                     # colorbar=dict(ticks     = "inside",
                                     #               len       = 1,                          ## vertical height of colorbar, expressed in a fraction of graph height, final height reduced by ypad
                                     #               ypad      = 0,                          ## y-padding of colorbar, reduces colorbar height
                                     #               tickwidth = 2,
                                     #               ticklen   = 10
                                     #              ),
                                    ),
                          row=1, col=1
                         )
        else:
            fig.add_trace(go.Contour(name=LONG_NAME_DICT[scalar_to_plot],
                                     x=x_points, y=y_points, z=np.reshape(scalar_to_plot_value, X.shape),
                                     colorscale=colorscheme,
                                     contours=dict(start=min,
                                                   end=max,
                                                   size=(max - min) / n_contour_lines,
                                                  ),
                                     showscale=False,
                                     hovertemplate='x = %{x:.4f}'+
                                                   '<br>y = %{y:.4f}'+
                                                   '<br>f(x,y) = %{z:.4e}'+
                                                   '<extra></extra>',
                                     # colorbar=dict(ticks     = "inside",
                                     #               len       = 1,                          ## vertical height of colorbar, expressed in a fraction of graph height, final height reduced by ypad
                                     #               ypad      = 0,                          ## y-padding of colorbar, reduces colorbar height
                                     #               tickwidth = 2,
                                     #               ticklen   = 10
                                     #              ),
                                    ),
                          row=1, col=1
                         )

        ## Plot flow element origins
        if plot_flow_elements:
            for i, object in enumerate(self.objects):
                try:
                    fig.add_trace(go.Scatter(name=f"{i + 1}. [{flow_element_type(object)}]",
                                             x=[object.x], y=[object.y],
                                             marker=dict(color=line_color(object),
                                                         size=dot_size(object)
                                                        ),
                                             hovertemplate=f'<b>{i + 1}. [{flow_element_type(object)}]</b>'+
                                                           '<br>x = %{x:.4f}'+
                                                           '<br>y = %{y:.4f}'+
                                                           f'<br>strength = {object.strength:.4e}'+
                                                           '<br>%{text}'
                                                           '<extra></extra>',
                                                           text = [f'alpha = {object.alpha:.4e}' if flow_element_type(object) == "Doublet" else ''],
                                            ),
                                  row=1, col=1
                                 )
                except AttributeError:
                    pass

                try:
                    fig.add_trace(go.Line(name=f"{i + 1}. [{flow_element_type(object)}]",
                                          x=[object.x1, object.x2], y=[object.y1, object.y2],
                                          line=dict(color=line_color(object),
                                                    width=line_width(object)
                                                   ),
                                          hovertemplate=f'<b>{i + 1}. [{flow_element_type(object)}]</b>'+
                                                        '<br>x = %{x:.4f}'+
                                                        '<br>y = %{y:.4f}'+
                                                        f'<br>strength = {object.strength:.4e}'+
                                                        '<extra></extra>',
                                         ),
                                  row=1, col=1
                                 )
                except AttributeError:
                    pass

        ## Update x-axis properties
        fig.update_xaxes(title_text='x',
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
                         range=[x_points.min(),x_points.max()],
                        )


        ## Update y-axis properties
        fig.update_yaxes(title_text='y',
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
                         range=[y_points.min(),y_points.max()],
                        )

        ## Update figure layout
        fig.update_layout(font_color='#000000',
                          plot_bgcolor='rgba(255,255,255,1)',
                          paper_bgcolor='rgba(255,255,255,1)',
                          autosize=False,
                          width=800,
                          height=800,
                          showlegend=False,
                         )

        if show:
            fig.show()

        return fig
