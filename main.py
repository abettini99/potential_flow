#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors:       A. Bettini and S. Van Hulle
Last Modified: 2023-03-03

Incompressible flow visualizer using the potentialflowvisualizer module.
Utilizes streamlit for user interface, whereas plotly is used for plotting.

First version of the code.
"""

# Library imports
from numpy import deg2rad, linspace
import streamlit as st
import plotly.express as px
import potentialflowvisualizer as pfv
from src.flowfield import Flowfield
from src.commondicts import PRESET_DEFAULT_DICT, ELEMENT_DEFAULT_DICT
from src.commonfuncs import flow_element_type

#### =================== ####
#### Session Information ####
#### =================== ####
COLOR_SCHEMES = sorted(px.colors.named_colorscales())

def initialize_session_state():
    default_dict = {"xmin": -2.0,
                    "xmax": 2.0,
                    "ymin": -2.0,
                    "ymax": 2.0,
                    "xsteps": 100,
                    "field": Flowfield(),
                    "figs": {},
                    "colorscheme": "rainbow",
                    "n_contour_lines": 15,
                    "n_streamline_density": 0.5,
                    "potential_streamline_bool": False
                   }

    for key, val in default_dict.items():
        if not key in st.session_state:
            st.session_state[key] = val

    return

initialize_session_state()

#### =========== ####
#### Draw Graphs ####
#### =========== ####
def draw():

    ## Recalculate gridpoint positions
    y_steps = int(st.session_state["xsteps"]
                  * (st.session_state["ymax"] - st.session_state["ymin"])
                  / (st.session_state["xmax"] - st.session_state["xmin"])
                 )
    x_points = linspace(st.session_state["xmin"], st.session_state["xmax"], st.session_state["xsteps"])
    y_points = linspace(st.session_state["ymin"], st.session_state["ymax"], y_steps)

    ## Clear dictionary of figures to display and redraw them
    st.session_state["figs"].clear()

    st.session_state["figs"][f"Graphs"] = st.session_state["field"].draw(x_points                  = x_points,
                                                                         y_points                  = y_points,
                                                                         colorscheme               = st.session_state["colorscheme"],
                                                                         n_contour_lines           = st.session_state["n_contour_lines"],
                                                                         n_streamline_density      = st.session_state["n_streamline_density"],
                                                                         potential_streamline_bool = st.session_state["potential_streamline_bool"]
                                                                        )

#### ================ ####
#### Main application ####
#### ================ ####
## App title
st.sidebar.title("Potential Flow Tool")

## App footer
footer = """
<style>
    # MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {
        content:'Made with Streamlit by Andrea Bettini and Simon Van Hulle';
        visibility: visible;display: block;position: relative;#background-color: red;padding: 5px;top: 2px;
    }
</style>
"""
st.markdown(footer, unsafe_allow_html=True)

## =========== ##
## Sidebar Tab ##
## =========== ##
## Buttons to clear and draw in sidebar
sb_col1, sb_col2 = st.sidebar.columns([1,1]) # sb = sidebar
with sb_col1:
    if st.button("Clear Flow"):
        st.session_state["field"].objects.clear()
        draw()

with sb_col2:
    if st.button("Draw Flow"):
        draw()

## Create sidebar tabs
welcome, add_element, presets, settings = st.sidebar.tabs(
    ["Welcome", "Add Flow Element", "Generic Flows", "Settings"]
)

## Welcome sidebar tab
with welcome:
    ## Include the README file into the application
    with open("README.md", "r") as ifstream:
        text = ifstream.read()
        text = text.split("---")
    st.markdown(text[0] +"---"+ text[2])
    ## TUD logo at bottom of sidebar
    st.image("images/TU_Delft_Logo.png", width=200)

## Graphing Sidebar tab
with settings:
    st.header("Layout")
    st.session_state["colorscheme"]               = st.selectbox("Color scheme", options=COLOR_SCHEMES, index=COLOR_SCHEMES.index("rainbow"))
    st.session_state["n_contour_lines"]           = st.number_input("Number of filled contours", value=15, min_value=5)
    st.session_state["n_streamline_density"]      = st.number_input("Streamline density", value=0.5, min_value=0.01)
    st.session_state["potential_streamline_bool"] = st.checkbox("Potential 'streamlines'", value=False)

    st.markdown("""----""")
    st.header("Grid")
    st.session_state["xmin"]   = st.number_input("$x$ minimum", value=-2.0)
    st.session_state["xmax"]   = st.number_input("$x$ maximum", value=2.0)
    st.session_state["ymin"]   = st.number_input("$y$ minimum", value=-2.0)
    st.session_state["ymax"]   = st.number_input("$y$ maximum", value=2.0)
    st.session_state["xsteps"] = st.number_input("$x$-steps on the grid", value=100, min_value=50)

## Add element sidebar tab
with add_element:
    # Get user input on what element to add
    key = st.selectbox("Select Flow Element", options=ELEMENT_DEFAULT_DICT.keys())

    # Retrieve necessary arguments for class using default values from a default element
    proto_elem  = ELEMENT_DEFAULT_DICT[key]
    args        = [None]*len(proto_elem.__dict__)
    # Create input fields
    for i, (k, v) in enumerate(proto_elem.__dict__.items()):
        # usually strength has some condition, i.e. Sources / Sinks are defined by their sign, so we add case studies
        if k == 'strength':
            if   flow_element_type(proto_elem) == 'Source':
                args[i] = st.number_input(f"{k}", value=float(v), min_value= 0.01, key=f"addelement_{key}_{i}")
            elif flow_element_type(proto_elem) == 'Sink':
                args[i] = st.number_input(f"{k}", value=float(v), max_value=-0.01, key=f"addelement_{key}_{i}")
        # otherwise it is inputs
        else:
            args[i] = st.number_input(f"{k}", value=float(v), key=f"addelement_{key}_{i}")

    # Add element
    if st.button("Add", key="add_element"):
        add_authority = True

        ## Ensure Source / Sink overlap does not happen, as it causes an issue with ff.create_streamline()
        if flow_element_type(proto_elem) == 'Source' or flow_element_type(proto_elem) == 'Sink':
            keys = list(st.session_state["field"].objects.keys())
            for key in keys:
                elem = st.session_state["field"].objects[key]
                # Compare arguments with all other sources/sink
                if flow_element_type(elem) == 'Source' or flow_element_type(elem) == 'Sink':
                    x0 = args[0]; y0 = args[1]                # Wish it could be more elegant, but this works.
                    x1 = elem.x;  y1 = elem.y

                    if abs(x0-x1) < 0.01 or abs(y0-y1) < 0.01:
                        add_authority = False

        ## Add item to flowfield dictionary
        if add_authority:
            elem = proto_elem.__class__
            num  = len(st.session_state["field"].objects) + 1
            name = f"{num}. [{flow_element_type(proto_elem)}]"
            st.session_state["field"].objects[name] = elem(*args)

            st.markdown(f'Added {name}')

        else:
            st.markdown(f'Did not add element -- check that Source/Sink position does not conflict with already existing Source/Sink positions')

## Add preset sidebar tab
with presets:
    # Get user input on what preset to add
    key = st.selectbox("Select Preset", options=PRESET_DEFAULT_DICT.keys())

    # Retrieve necessary arguments for preset using default values from default elements
    proto_preset = PRESET_DEFAULT_DICT[key] # proto_preset is a list of elements
    args         = [None]*len(proto_preset)
    for i, proto_elem in enumerate(proto_preset):
        args[i]  = [None]*len(proto_elem.__dict__)

        # Subdivide all elements that make up the preset via a header
        st.subheader(flow_element_type(proto_elem))
        for j, (k, v) in enumerate(proto_elem.__dict__.items()):
            args[i][j] = st.number_input(f"{k}", value=float(v), key=f"addpreset_{key}_{i}_{j}")

    # Add preset
    if st.button("Add ", key="add_preset"):
        for i, proto_elem in enumerate(proto_preset):
            elem = proto_elem.__class__
            num  = len(st.session_state["field"].objects) + 1
            name = f"{num}. [{flow_element_type(proto_elem)}]"
            st.session_state["field"].objects[name] = elem(*args[i])

            st.markdown(f'Added {name}')

## =========== ##
## Main Screen ##
## =========== ##
## Plot the figures
st.subheader("Contour Plots")
st.markdown('Hover over the graph to see information on the shown field itself, if there are no elements, add them in yourself.')
for title, fig in st.session_state["figs"].items():
    st.plotly_chart(fig)

## Adjust the flow elements
if not len(st.session_state["field"].objects) == 0:
    st.markdown("""----""")
    st.subheader("Adjust your flow elements")

    key     = st.selectbox("Select Flow Element", options=st.session_state["field"].objects.keys(), key='adjust_selectbox')
    elem    = st.session_state["field"].objects[key]

    # Adjustment field
    for k, v in elem.__dict__.items():
        elem.__dict__[k] = st.number_input(f"{k}", value=float(v), key=f"adjust_{elem}_{k}")

    # Removal field
    if st.button("Remove Flow", key="remove"):

        del st.session_state["field"].objects[key]
        st.markdown(f'Removed {key}')

        ## Rename all keys such that numbering is correct
        old_keys = list(st.session_state["field"].objects.keys()) # Ensure that the keys aren't changed at the same time as entries (hence the list)
        for i, k_old in enumerate( old_keys ):
            elem = st.session_state["field"].objects[k_old]
            k_new = f'{i+1}. [{flow_element_type(elem)}]'

            # Remove first, then add: if not, then del (...) will remove all entries with the same name!
            del st.session_state["field"].objects[k_old]
            st.session_state["field"].objects[k_new] = elem

    st.markdown("""----""")
