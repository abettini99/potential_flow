import numpy as np
import plotly as ply
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = (
    "browser"  # Feel free to disable this if you're running in notebook mode or prefer a different frontend.
)


import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

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

    def draw(
        self,
        scalar_to_plot="potential",  # "potential", "streamfunction", "xvel", "yvel", "velmag"
        x_points=np.linspace(-10, 10, 200),
        y_points=np.linspace(-10, 10, 200),
        show=True,
        colorscheme="Viridis",
        n_contour_lines=40,
        plot_flow_elements=False,
    ):
        X, Y = np.meshgrid(x_points, y_points)
        X_r = np.reshape(X, -1)
        Y_r = np.reshape(Y, -1)
        points = np.vstack((X_r, Y_r)).T

        scalar_to_plot_value = np.zeros_like(X_r)
        if scalar_to_plot == "velmag":
            x_vels = np.zeros_like(X_r)
            y_vels = np.zeros_like(X_r)
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
            else:
                raise Exception

        if scalar_to_plot == "velmag":
            scalar_to_plot_value = np.sqrt(x_vels**2 + y_vels**2)

        min = np.nanpercentile(scalar_to_plot_value, 10)
        max = np.nanpercentile(scalar_to_plot_value, 90)

        fig = go.Figure()
        if min == max:
            return fig

        fig.add_trace(
            go.Contour(
                x=x_points,
                y=y_points,
                z=np.reshape(scalar_to_plot_value, X.shape),
                colorscale=colorscheme,
                contours=dict(start=min, end=max, size=(max - min) / n_contour_lines),
                colorbar=dict(title=scalar_to_plot, titleside="top", ticks="outside"),
            ),
        )

        for object in self.objects if plot_flow_elements else []:
            try:
                fig.add_trace(
                    go.Scatter(
                        x=[object.x],
                        y=[object.y],
                        marker=dict(color=line_color(object), size=dot_size(object)),
                        showlegend=False,
                    )
                )
            except AttributeError:
                pass

            try:
                fig.add_trace(
                    go.Line(
                        x=[object.x1, object.x2],
                        y=[object.y1, object.y2],
                        line=dict(color=line_color(object), width=line_width(object)),
                        showlegend=False,
                    )
                )
            except AttributeError:
                pass

        # fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1))
        if show:
            fig.show()

        return fig
