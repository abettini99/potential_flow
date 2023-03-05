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
from src.commondicts import PRESET_DICT, ELEMENT_DEFAULT_DICT
from src.commonfuncs import flow_element_type
import copy

#### =================== ####
#### Session Information ####
#### =================== ####
COLOR_SCHEMES = ["viridis"] + sorted(px.colors.named_colorscales())

def initialize_session_state():
    default_dict = {"xmin": -1.0,
                    "xmax": 1.0,
                    "ymin": -1.0,
                    "ymax": 1.0,
                    "xsteps": 300,
                    "field": Flowfield(),
                    "update_trigger": False,
                    "figs": {},
                    "plot_objects": True,
                    "colorscheme": "Viridis",
                    "n_contour_lines": 15,
                    "show_potential": False,
                    "show_streamfunction": False,
                    "show_velmag": True,
                    "show_pressure": True,
                    "show_xvel": False,
                    "show_yvel": False,
                    "Graphing_Mode": 'Easy Mode'
                   }

    for key, val in default_dict.items():
        if not key in st.session_state:
            st.session_state[key] = val

    return

initialize_session_state()

#### ================== ####
#### Update Information ####
#### ================== ####
def update():
    ## Recalculate gridpoint positions
    y_steps = int(st.session_state["xsteps"]
                  * (st.session_state["ymax"] - st.session_state["ymin"])
                  / (st.session_state["xmax"] - st.session_state["xmin"])
                 )
    x_points = linspace(st.session_state["xmin"], st.session_state["xmax"], st.session_state["xsteps"])
    y_points = linspace(st.session_state["ymin"], st.session_state["ymax"], y_steps)

    ## Clear dictionary of figures to display and redraw them
    st.session_state["figs"].clear()
    for name in ["potential", "streamfunction", "xvel", "yvel", "velmag", "pressure"]:
        if st.session_state[f"show_{name}"]:
            st.session_state["figs"][f"{name}"] = st.session_state["field"].draw(
                scalar_to_plot=name,
                x_points=x_points,
                y_points=y_points,
                show=False,
                colorscheme=st.session_state["colorscheme"],
                n_contour_lines=st.session_state["n_contour_lines"],
                plot_flow_elements=st.session_state["plot_objects"],
            )
    return

#### ================ ####
#### Main application ####
#### ================ ####
## App title
st.sidebar.title("Potential Flow Tool")

## App footer
footer = """
<style>
    #MainMenu {visibility: hidden;}
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
## Buttons to clear and update in sidebar
sb_col1, sb_col2 = st.sidebar.columns([1,1]) # sb = sidebar
with sb_col1:
    if st.button("Clear Flow"):
        st.session_state["field"].objects.clear()
        update()
with sb_col2:
    if st.button("Update Flow"):
        update()

## Create sidebar tabs
welcome, graphing, add_element, presets = st.sidebar.tabs(
    ["Welcome", "Graphing", "Add Flow Element", "Generic Flows"]
)

## Welcome sidebar tab
with welcome:
    ## Truncated README.md file used
    with open("README.md", "r") as ifstream:
        text = ifstream.read()
        text = text.split("---")
    st.markdown(text[0] +"---"+ text[2])
    ## TUD logo at bottom of sidebar
    st.image("images/TU_Delft_Logo.png", width=200)

## Graphing Sidebar tab
with graphing:
    st.radio("Graphing Mode:",
             key='Graphing_Mode',
             options=['Easy Mode', 'Expert Mode']
            )

    st.markdown("""----""")
    if st.session_state["Graphing_Mode"] == 'Easy Mode':
        st.session_state["plot_objects"]        = True
        st.session_state["show_potential"]      = False
        st.session_state["show_streamfunction"] = False
        st.session_state["show_velmag"]         = True
        st.session_state["show_pressure"]       = True
        st.session_state["show_xvel"]           = False
        st.session_state["show_yvel"]           = False
        st.session_state["colorscheme"]         = st.selectbox("Color Scheme", options=COLOR_SCHEMES)
        st.session_state["n_contour_lines"]     = st.number_input("Number of contour lines", value=15)

        update()

    if st.session_state["Graphing_Mode"] == 'Expert Mode':
        st.header("Grid")
        st.session_state["xmin"]                = st.number_input("x minimum", value=-1.0)
        st.session_state["xmax"]                = st.number_input("x maximum", value=1.0)
        st.session_state["ymin"]                = st.number_input("y minimum", value=-1.0)
        st.session_state["ymax"]                = st.number_input("y maximum", value=1.0)
        st.session_state["xsteps"]              = st.number_input("x-steps on the grid", value=300)

        st.markdown("""----""")
        st.header("Layout")
        st.session_state["plot_objects"]        = st.checkbox("Plot flow objects", True)
        st.session_state["show_potential"]      = st.checkbox("Plot potential function", True)
        st.session_state["show_streamfunction"] = st.checkbox("Plot stream function", True)
        st.session_state["show_velmag"]         = st.checkbox("Plot velocity magnitude", True)
        st.session_state["show_pressure"]       = st.checkbox("Plot pressure coefficient", True)
        st.session_state["show_xvel"]           = st.checkbox("Plot x velocity", False)
        st.session_state["show_yvel"]           = st.checkbox("Plot y velocity", False)
        st.session_state["colorscheme"]         = st.selectbox("Color scheme", options=COLOR_SCHEMES)
        st.session_state["n_contour_lines"]     = st.number_input("Number of contour lines", value=15)

        update()

def adjust_objects(objects, id=None):
    for flowobj in objects:
        ## Add divider
        st.markdown("""----""")
        ## Extra divider in case a preset is used
        if id == "preset":
            st.subheader(flow_element_type(obj))
        ## Fields to be edited
        for key, val in flowobj.__dict__.items():
            flowobj.__dict__[key] = st.number_input(f"{key}", value=float(val), key=f"{id}_{key}_{flowobj}")
    return

## TODO: ASK SIMON TO ANNOTATE BELOW
## Add element sidebar tab
with add_element:
    key = st.selectbox("Select Flow Element", options=ELEMENT_DEFAULT_DICT.keys())

    try:
        flowobj = copy.deepcopy(ELEMENT_DEFAULT_DICT[key])
        name    = adjust_objects([flowobj], "element")
        if st.button("Add ", key="add_element"):
            st.session_state["field"].objects.extend([flowobj])
            update()

    except KeyError:
        pass

## Add preset sidebar tab
with presets:
    key = st.selectbox("Select Preset", options=PRESET_DICT.keys())

    try:
        objects = PRESET_DICT[key]
        for i, obj in enumerate(objects):
            name = adjust_objects([obj], "preset")

        if st.button("Add ", key="add_preset"):
            st.session_state["field"].objects.extend(objects)
            update()

    except KeyError:
        pass

## =========== ##
## Main Screen ##
## =========== ##
## Plot the figures
if st.session_state["figs"]:
    st.subheader("Contour Plots")
for title, fig in st.session_state["figs"].items():
    st.plotly_chart(fig)

## Adjust the flow elemetns
if not len(st.session_state["field"].objects) == 0:
    st.markdown("""----""")
    st.subheader("Adjust your flow elements")

    dropdown_dict = {}
    for i, obj in enumerate(st.session_state["field"].objects):
        dropdown_dict[f"{i + 1}. [{flow_element_type(obj)}]"] = obj

    key     = st.selectbox("Select Flow Element", options=dropdown_dict.keys())
    flowobj = dropdown_dict[key]
    name    = adjust_objects([flowobj], "adjust")

    ae_col1, ae_col2 = st.columns([1,1]) # ae = adjust element
    with ae_col1:
        if st.button("Update Flow", key="update"):
            update()
    with ae_col2:
        if st.button("Remove Flow", key="remove"):
            # print(st.session_state["field"].objects)
            # print(flowobj)
            st.session_state["field"].objects.remove(flowobj)
            update()

    st.markdown("""----""")
