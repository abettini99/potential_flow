import potentialflowvisualizer as pfv
from myflowfield import Flowfield

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd


app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

field = pfv.Flowfield(
    [
        pfv.Freestream(1, 0),
        # pfv.Vortex(20, 0, 0),
        pfv.Doublet(-100, 0, 0, 0),
    ]
)
fig = field.draw("streamfunction", show=False)

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="example-graph", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run_server()
