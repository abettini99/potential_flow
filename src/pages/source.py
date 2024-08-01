import dash
from dash import html, dcc

def source():
    return html.Div(children=[
    
    html.H1("Source Flow"),

    dcc.Markdown('''
    \\[...\\] The velocity around a source/sink is then given by
    $$
    V_r = \\frac{\\Lambda}{2\\pi r}
    $$
    EXAMPLE TEXT: \n
    LOREM LOREM LOREM
    ''',mathjax=True),



    ])
