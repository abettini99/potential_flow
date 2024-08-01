import dash
from dash import html, dcc

def cylinder():
    return html.Div(children=[
    
    html.H1("Flow around a cylinder"),
    
    dcc.Markdown(''' EXAMPLE LATEX:
    $$
    \\frac{1}{(\\sqrt{\\phi \\sqrt{5}}-\\phi) e^{\\frac25 \\pi}} =
    1+\\frac{e^{-2\\pi}} {1+\\frac{e^{-4\\pi}} {1+\\frac{e^{-6\\pi}}
    {1+\\frac{e^{-8\\pi}} {1+\\ldots} } } }
    $$
    EXAMPLE TEXT: \n
    LOREM LOREM LOREM
    ''',mathjax=True),
    
    ])
