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
    bla bla bla
    ''',mathjax=True),

    html.Label('Strength Slider:'),
    dcc.Slider(-2, 2,
               value=1,
               id='Lambda_strength',
              ),

    dcc.Markdown('''
    bla bla bla bla bla, velocity graph
    ''',mathjax=True),
    dcc.Graph(id='Velocity-Graph', mathjax=True),

    dcc.Markdown('''
    bla bla bla bla bla, potential graph
    ''',mathjax=True),


    dcc.Graph(id='Potential-Graph', mathjax=True),

    ])
