#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports
from lib.grid import *
from numpy import deg2rad
from PIL import Image
import lib.utils as utils
import streamlit as st
import matplotlib.pyplot as plt
import math as m

import plotly as ply
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


#### ================== ####
#### Update Information ####
#### ================== ####


initialize_session_state()


def update():

    y_steps = int(
        st.session_state["xsteps"]
        * (st.session_state["ymax"] - st.session_state["ymin"])
        / (st.session_state["xmax"] - st.session_state["xmin"])
    )
    x_points = np.linspace(st.session_state["xmin"], st.session_state["xmax"], st.session_state["xsteps"])
    y_points = np.linspace(st.session_state["ymin"], st.session_state["ymax"], y_steps)

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

## General Test Cases
general, uniform, source, sink, doublet, vortex, linesource, cylinder, rotating_cylinder = st.sidebar.tabs(
    ["General", "Uniform", "Source", "Sink", "Doublet", "Vortex", "Line Source", "Cylinder", "Rotating Cylinder"]
)

with general:
    st.header("Grid")
    st.session_state["xmin"] = st.number_input("xmin", value=-1.0)
    st.session_state["xmax"] = st.number_input("xmax", value=1.0)
    st.session_state["ymin"] = st.number_input("ymin", value=-1.0)
    st.session_state["ymax"] = st.number_input("ymax", value=1.0)
    st.session_state["xsteps"] = st.number_input("x-steps", value=300)

    st.header("Layout")
    st.session_state["plot_objects"] = st.checkbox("Plot flow elements", True)
    st.session_state["colorscheme"] = st.selectbox("Color Scheme", options=COLOR_SCHEMES)

    st.text("")


def flow_element_name(object): 
    return str(type(object)).strip(">").strip("'").split(".")[-1]

def default_uniform():
    return pfv.Freestream(1, 0)

# for element in [default_uniform]:
#     object = default_uniform()
#     name = flow_element_name(object)

#     with st.sidebar.tabs[name]:
#         for key, val in object.__dict__.items():
#             object.__dict__[key] = st.number_input(f"{key}", value=val, key=f"{key}_{name}")

#         if st.button(f"Add {name}", key="update"):
#             st.session_state["field"].objects.extend([object])
#             update()



with uniform:
    u = st.number_input("Velocity x-component", value=1.0)
    v = st.number_input("Velocity y-component", value=0.0)

    if st.button("Add Uniform Flow"):
        st.session_state["field"].objects.extend([pfv.Freestream(u, v)])
        update()

with source:
    xpos = st.number_input("x-coordinate", value=0.0, key="xsource")
    ypos = st.number_input("y-coordinate", value=0.0, key="ysource")
    strength = st.number_input("Source strength", value=1.0, key="strengthsource")
    if st.button("Add Source"):
        st.session_state["field"].objects.extend([pfv.Source(strength, xpos, ypos)])
        update()

with sink:
    xpos = st.number_input("x-coordinate", value=0.0, key="xsink")
    ypos = st.number_input("y-coordinate", value=0.0, key="ysink")
    strength = st.number_input("Sink strength", value=1.0, key="strengthsink")
    if st.button("Add Sink"):
        st.session_state["field"].objects.extend([pfv.Source(-strength, xpos, ypos)])
        update()

with doublet:
    xpos = st.number_input("x-coordinate", value=0.0, key="xdoublet")
    ypos = st.number_input("y-coordinate", value=0.0, key="ydoublet")
    strength = st.number_input("Doublet strength", value=1.0, key="strengthdoublet")
    alpha = st.number_input("Doublet angle", value=0.0, key="alphadoublet")
    if st.button("Add Doublet"):
        st.session_state["field"].objects.extend([pfv.Doublet(strength, xpos, ypos, alpha)])
        update()

with vortex:
    xpos = st.number_input("x-coordinate", value=0.0, key="xvortex")
    ypos = st.number_input("y-coordinate", value=0.0, key="yvortex")
    strength = st.number_input("Vortex strength", value=1.0, key="strengthvortex")
    if st.button("Add Vortex"):
        st.session_state["field"].objects.extend([pfv.Vortex(strength, xpos, ypos)])
        update()

with linesource:
    x1 = st.number_input("x1", value=0.0, key="x1")
    y1 = st.number_input("x2", value=0.0, key="y1")
    x2 = st.number_input("x2", value=1.0, key="x2")
    y2 = st.number_input("y2", value=0.0, key="y2")
    strength = st.number_input("Source strength", value=1.0, key="strengthlinesource")

    if st.button("Add Line source"):
        st.session_state["field"].objects.extend([pfv.LineSource(strength, x1, y1, x2, y2)])
        update()


with cylinder:
    xpos = st.number_input("x-coordinate", value=0.0, key="xcylinder")
    ypos = st.number_input("y-coordinate", value=0.0, key="ycylinder")
    speed = st.number_input("Freestream speed", value=1.0, key="speedcylinder")
    angle = st.number_input("Angle-of-attack in degrees", value=0.0, key="angle")
    radius = st.number_input("Cylinder radius", value=1.0, key="radiuscylinder")
    if st.button("Add Non-rotating Cylinder"):
        st.session_state["field"].objects.extend([pfv.Freestream(speed, angle), pfv.Doublet(radius, xpos, ypos, 0)])
        update()


with rotating_cylinder:
    xpos = st.number_input("x-coordinate", value=0.0, key="xrotatingcylinder")
    ypos = st.number_input("y-coordinate", value=0.0, key="yrotatingcylinder")
    speed = st.number_input("Freestream speed", value=1.0, key="speedrotatingcylinder")
    strength = st.number_input("Vortex strength", value=1.0, key="strengthrotatingcylinder")
    radius = st.number_input("Cylinder radius", value=1.0, key="radiusrotatingcylinder")
    if st.button("Add Rotating Cylinder"):
        st.session_state["field"].objects.extend(
            [pfv.Freestream(speed, angle), pfv.Doublet(radius, xpos, ypos, 0), pfv.Vortex(strength, xpos, ypos)]
        )
        update()


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
