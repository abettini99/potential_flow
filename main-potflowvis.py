#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports

from numpy import deg2rad, linspace
import streamlit as st

import plotly.express as px

import potentialflowvisualizer as pfv
from lib.flowfield import Flowfield


#### =================== ####
#### Session Information ####
#### =================== ####
# https://docs.streamlit.io/library/advanced-features/session-state

COLOR_SCHEMES = ["viridis"] + sorted(px.colors.named_colorscales())


def initialize_session_state():
    for key, val in zip(
        ["xmin", "xmax", "ymin", "ymax", "xsteps", "field", "update_trigger", "figs", "plot_objects", "colorscheme"],
        [-1.0, 1.0, -1.0, 1.0, 300, Flowfield(), False, {}, True, "Viridis"],
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

    fig1 = st.session_state["field"].draw(
        scalar_to_plot="potential",
        x_points=x_points,
        y_points=y_points,
        show=False,
        colorscheme=st.session_state["colorscheme"],
    )
    fig2 = st.session_state["field"].draw(
        scalar_to_plot="streamfunction",
        x_points=x_points,
        y_points=y_points,
        show=False,
        colorscheme=st.session_state["colorscheme"],
    )

    st.session_state["figs"] = {"Potential Function": fig1, "Stream Function": fig2}


#### ================ ####
#### Main application ####
#### ================ ####

## App title
st.sidebar.title("Potential Flow Theory Tool")

## Create button for superposition of fields
if st.sidebar.button("Clear Grid"):
    # st.session_state["grid"].clear()
    st.session_state["field"].objects = []
    update()

if st.sidebar.button("Update Grid"):
    update()


grid, layout, add_element, presets = st.sidebar.tabs(["Grid", "Layout", "Add Flow Element", "Presets"])

with grid:
    st.header("Grid")
    st.session_state["xmin"] = st.number_input("xmin", value=-1.0)
    st.session_state["xmax"] = st.number_input("xmax", value=1.0)
    st.session_state["ymin"] = st.number_input("ymin", value=-1.0)
    st.session_state["ymax"] = st.number_input("ymax", value=1.0)
    st.session_state["xsteps"] = st.number_input("x-steps", value=300)

with layout:
    st.header("Layout")
    st.session_state["plot_objects"] = st.checkbox("Plot flow elements", True)
    st.session_state["colorscheme"] = st.selectbox("Color Scheme", options=COLOR_SCHEMES)


def flow_element_name(object):
    return str(type(object)).strip(">").strip("'").split(".")[-1]


def default_uniform():
    return pfv.Freestream(1, 0)


def default_source():
    return pfv.Source(1, 0, 0)


def default_sink():
    return pfv.Source(-1, 0, 0)


def default_doublet():
    return pfv.Doublet(1, 0, 0, 0)


def default_vortex():
    return pfv.Vortex(1, 0, 0)


def default_linesource():
    return pfv.LineSource(1, 0, 0, 1, 0)


ELEMENT_DEFAULT_DICT = {
    "Uniform": default_uniform,
    "Source": default_source,
    "Sink": default_sink,
    "Doublet": default_doublet,
    "Vortex": default_vortex,
    "LineSource": default_linesource,
}

ELEMENT_NOTES_DICT = {
    "Uniform": "Specify the x and y velocity components",
    "Source": "Specify the source strength and the x and y coordinates",
    "Sink": "Specify the sink strength and the x and y coordinates. Note that a sink is simply a source with negative strength",
    "Doublet": "Specify the doublet strength, position and angle",
    "Vortex": "Specify the vortex strength and position",
    "LineSource": "Specify the source strength and the start and stop positions of the line",
}


with add_element:
    object_dict = {}

    key = st.selectbox("Select Flow Element", options=ELEMENT_DEFAULT_DICT.keys())

    try:
        flowobj = ELEMENT_DEFAULT_DICT[key]()
        note = ELEMENT_NOTES_DICT[key]

        st.text(note)

        for key, val in flowobj.__dict__.items():
            flowobj.__dict__[key] = st.number_input(f"{key}", value=float(val), key=f"{key}_{key}")

        if st.button("Add ", key="add_element"):
            st.session_state["field"].objects.extend([flowobj])
            update()
    except KeyError:
        pass

# with cylinder:
#     xpos = st.number_input("x-coordinate", value=0.0, key="xcylinder")
#     ypos = st.number_input("y-coordinate", value=0.0, key="ycylinder")
#     speed = st.number_input("Freestream speed", value=1.0, key="speedcylinder")
#     angle = st.number_input("Angle-of-attack in degrees", value=0.0, key="angle")
#     radius = st.number_input("Cylinder radius", value=1.0, key="radiuscylinder")
#     if st.button("Add Non-rotating Cylinder"):
#         st.session_state["field"].objects.extend([pfv.Freestream(speed, angle), pfv.Doublet(radius, xpos, ypos, 0)])
#         update()


# with rotating_cylinder:
#     xpos = st.number_input("x-coordinate", value=0.0, key="xrotatingcylinder")
#     ypos = st.number_input("y-coordinate", value=0.0, key="yrotatingcylinder")
#     speed = st.number_input("Freestream speed", value=1.0, key="speedrotatingcylinder")
#     strength = st.number_input("Vortex strength", value=1.0, key="strengthrotatingcylinder")
#     radius = st.number_input("Cylinder radius", value=1.0, key="radiusrotatingcylinder")
#     if st.button("Add Rotating Cylinder"):
#         st.session_state["field"].objects.extend(
#             [pfv.Freestream(speed, angle), pfv.Doublet(radius, xpos, ypos, 0), pfv.Vortex(strength, xpos, ypos)]
#         )
#         update()


for title, fig in st.session_state["figs"].items():
    st.plotly_chart(fig)


## Do a super-hack:
## I would normally not do the redundant line of making option = flowobj
## but it seems that option is a session-state variable, and not the actual grid object itself
## therefore you cannot modify option, but can modify flowobj
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

        for key, val in flowobj.__dict__.items():
            flowobj.__dict__[key] = st.number_input(f"{key}", value=val, key=f"{key}_update")

        if st.button("Update", key="update"):
            update()

        if st.button("Remove", key="remove"):
            st.session_state["field"].objects.remove(flowobj)
            update()

        st.markdown("""----""")
