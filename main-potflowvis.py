#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports

from numpy import deg2rad, linspace
import streamlit as st
import plotly.express as px
import potentialflowvisualizer as pfv
from flowfield import Flowfield
import copy


#### =================== ####
#### Session Information ####
#### =================== ####

COLOR_SCHEMES = ["viridis"] + sorted(px.colors.named_colorscales())

ELEMENT_DEFAULT_DICT = {
    "Uniform": pfv.Freestream(1, 0),
    "Source": pfv.Source(1, 0, 0),
    "Sink": pfv.Source(-1, 0, 0),
    "Doublet": pfv.Doublet(1, 0, 0, 0),
    "Vortex": pfv.Vortex(1, 0, 0),
    "LineSource": pfv.LineSource(1, 0, 0, 1, 0),
}

ELEMENT_NAME_DICT = {
    pfv.Freestream: "Uniform",
    pfv.Source: "Source",
    pfv.Doublet: "Doublet",
    pfv.Vortex: "Vortex",
    pfv.LineSource: "LineSource",
}

def initialize_session_state():
    for key, val in zip(
        [
            "xmin",
            "xmax",
            "ymin",
            "ymax",
            "xsteps",
            "field",
            "update_trigger",
            "figs",
            "plot_objects",
            "colorscheme",
            "n_contour_lines",
            "show_potential",
            "show_streamfunction",
        ],
        [-1.0, 1.0, -1.0, 1.0, 300, Flowfield(), False, {}, True, "Viridis", 40, True, True],
    ):
        if not key in st.session_state:
            st.session_state[key] = val


initialize_session_state()

#### ================== ####
#### Update Information ####
#### ================== ####


def update():

    y_steps = int(
        st.session_state["xsteps"]
        * (st.session_state["ymax"] - st.session_state["ymin"])
        / (st.session_state["xmax"] - st.session_state["xmin"])
    )
    x_points = linspace(st.session_state["xmin"], st.session_state["xmax"], st.session_state["xsteps"])
    y_points = linspace(st.session_state["ymin"], st.session_state["ymax"], y_steps)

    if st.session_state["show_potential"]:
        st.session_state["figs"]["Potential Function"] = st.session_state["field"].draw(
            scalar_to_plot="potential",
            x_points=x_points,
            y_points=y_points,
            show=False,
            colorscheme=st.session_state["colorscheme"],
            n_contour_lines=st.session_state["n_contour_lines"],
            plot_flow_elements=st.session_state["plot_objects"],
        )

    if st.session_state["show_streamfunction"]:
        st.session_state["figs"]["Stream Function"] = st.session_state["field"].draw(
            scalar_to_plot="streamfunction",
            x_points=x_points,
            y_points=y_points,
            show=False,
            colorscheme=st.session_state["colorscheme"],
            n_contour_lines=st.session_state["n_contour_lines"],
            plot_flow_elements=st.session_state["plot_objects"],
        )


#### ================ ####
#### Main application ####
#### ================ ####

## App title
st.sidebar.title("Potential Flow Theory Tool")

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


## Buttons to clear and update in sidebar
if st.sidebar.button("Clear Grid"):
    st.session_state["field"].objects = []
    update()

if st.sidebar.button("Update Grid"):
    update()

## Create sidebar tabs
welcome, grid, layout, add_element, presets = st.sidebar.tabs(["Welcome", "Grid", "Layout", "Add Flow Element", "Add Presets"])

with welcome:
    with open("README.md", 'r') as ifstream:
        text = ifstream.read()
    st.markdown(text)

with grid:
    st.header("Grid")
    st.session_state["xmin"] = st.number_input("xmin", value=-1.0)
    st.session_state["xmax"] = st.number_input("xmax", value=1.0)
    st.session_state["ymin"] = st.number_input("ymin", value=-1.0)
    st.session_state["ymax"] = st.number_input("ymax", value=1.0)
    st.session_state["xsteps"] = st.number_input("x-steps on the grid", value=300)

with layout:
    st.header("Layout")
    st.session_state["plot_objects"] = st.checkbox("Plot flow elements", True)
    st.session_state["show_potential"] = st.checkbox("Plot the potential", True)
    st.session_state["show_streamfunction"] = st.checkbox("Plot the stream function", True)
    st.session_state["colorscheme"] = st.selectbox("Color Scheme", options=COLOR_SCHEMES)
    st.session_state["n_contour_lines"] = st.number_input("Number of contour lines", value=40)





def flow_element_name(object):
    name = ELEMENT_NAME_DICT[object.__class__]
    if name == "Source" and object.strength < 0:
        name = "Sink"
    return name

PRESET_DICT = {
    "Cylinder": [pfv.Freestream(1, 0), pfv.Doublet(1, 0, 0, 0)],
    "Rotating Cylinder": [pfv.Freestream(1, 0), pfv.Doublet(1, 0, 0, 0), pfv.Vortex(1, 0, 0)],
}


def adjust_object(flowobj, id=None):
    for key, val in flowobj.__dict__.items():
        flowobj.__dict__[key] = st.number_input(f"{key}", value=float(val), key=f"{id}_{key}_{key}")

    st.text("")


with add_element:
    key = st.selectbox("Select Flow Element", options=ELEMENT_DEFAULT_DICT.keys())

    try:
        flowobj = copy.deepcopy(ELEMENT_DEFAULT_DICT[key])

        adjust_object(flowobj, "element")

        if st.button("Add ", key="add_element"):
            st.session_state["field"].objects.extend([flowobj])
            update()

    except KeyError:
        pass

with presets:

    key = st.selectbox("Select Preset", options=PRESET_DICT.keys())
    try:
        objects = PRESET_DICT[key]

        for i, obj in enumerate(objects):
            st.subheader(flow_element_name(obj))

            adjust_object(obj, "preset")

        if st.button("Add ", key="add_preset"):
            st.session_state["field"].objects.extend(objects)
            update()

    except KeyError:
        pass

## Plot the figures
if st.session_state["figs"]:
    st.subheader("Contour Plots")
for title, fig in st.session_state["figs"].items():
    st.plotly_chart(fig)

## Adjust the flow elemetns
if not len(st.session_state["field"].objects) == 0:
    with st.container():
        st.markdown("""----""")

        st.subheader("Adjust your flow elements")
        object_dict = {}
        for i, object in enumerate(st.session_state["field"].objects):
            key = f"{str(i + 1)}. " + flow_element_name(object)
            object_dict[key] = object

        key = st.selectbox("Select Flow Element", options=object_dict.keys())
        flowobj = object_dict[key]

        adjust_object(flowobj, "adjust")

        if st.button("Update", key="update"):
            update()

        if st.button("Remove", key="remove"):
            st.session_state["field"].objects.remove(flowobj)
            update()

        st.markdown("""----""")
