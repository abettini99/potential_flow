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
import plotly.subplots

import potentialflowvisualizer as pfv
from lib.flowfield import Flowfield

#### =================== ####
#### Session Information ####
#### =================== ####
# https://docs.streamlit.io/library/advanced-features/session-state


for key, val in zip(
    ["xmin", "xmax", "ymin", "ymax", "xsteps", "field", "update_trigger", "figs"],
    [-1.0, 1.0, -1.0, 1.0, 300, Flowfield(), False, []],
):
    if not key in st.session_state:
        st.session_state[key] = val

#### ================== ####
#### Update Information ####
#### ================== ####


def update():
    y_steps = int(
        st.session_state["xsteps"]
        * (st.session_state["ymax"] - st.session_state["ymin"])
        / (st.session_state["xmax"] - st.session_state["xmin"])
    )
    x_points = np.linspace(st.session_state["xmin"], st.session_state["xmax"], st.session_state["xsteps"])
    y_points = np.linspace(st.session_state["ymin"], st.session_state["ymax"], y_steps)

    fig1 = st.session_state["field"].draw(scalar_to_plot="potential", x_points=x_points, y_points=y_points, show=False)
    fig2 = st.session_state["field"].draw(
        scalar_to_plot="streamfunction", x_points=x_points, y_points=y_points, show=False
    )

    st.session_state["figs"] = [fig1, fig2]


#### ================ ####
#### Main application ####
#### ================ ####

## App title
st.sidebar.title("Potential Flow Theory Tool")

## Create button for superposition of fields
if st.sidebar.button("Clear grid"):
    # st.session_state["grid"].clear()
    st.session_state["field"].objects = []
    update()

## General Test Cases
general, uniform, source, sink, doublet, vortex, linesource, cylinder, rotating_cylinder = st.sidebar.tabs(
    ["General", "Uniform", "Source", "Sink", "Doublet", "Vortex", "Line Source", "Cylinder", "Rotating Cylinder"]
)

with general:
    st.session_state["xmin"] = st.number_input("xmin", value=-1.0)
    st.session_state["xmax"] = st.number_input("xmax", value=1.0)
    st.session_state["ymin"] = st.number_input("ymin", value=-1.0)
    st.session_state["ymax"] = st.number_input("ymax", value=1.0)
    st.session_state["xsteps"] = st.number_input("x-steps", value=300)
    if st.button("Update Grid"):
        update()


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

for fig in st.session_state["figs"]:
    st.plotly_chart(fig)


## Do a super-hack:
## I would normally not do the redundant line of making option = flowobj
## but it seems that option is a session-state variable, and not the actual grid object itself
## therefore you cannot modify option, but can modify flowobj
if not len(st.session_state["field"].objects) == 0:
    with st.container():
        st.markdown("""----""")

        optionlist = [
            f"{str(i + 1)}. " + str(type(obj)).strip(">").strip("'").split(".")[-1]
            for i, obj in enumerate(st.session_state["field"].objects)
        ]
        option = st.selectbox("TEST", options=optionlist)
        # flowobj = [obj for obj in st.session_state["field"].objects if obj == option][0]
        flowobj = [obj for obj in st.session_state["field"].objects][0]

        if type(flowobj) == pfv.Freestream:

            u = st.number_input("Velocity x-component", value=flowobj.u, key="u_update")
            v = st.number_input("Velocity y-component", value=flowobj.v, key="v_update")

            if st.button("Update", key="tmp3"):
                flowobj.u = float(u)
                flowobj.v = float(v)

                update()

        if type(flowobj) == pfv.Source:
            xpos = st.number_input("x-coordinate", value=flowobj.x, key="x_update")
            ypos = st.number_input("y-coordinate", value=flowobj.y, key="y_update")
            strength = st.number_input("Source strength", value=flowobj.strength, key="strength_update")

            if st.button("Update", key="tmp3"):
                flowobj.x = float(xpos)
                flowobj.y = float(ypos)
                flowobj.strength = float(strength)

                update()

        if type(flowobj) == pfv.Doublet:
            xpos = st.number_input("x-coordinate", value=flowobj.x, key="x_update")
            ypos = st.number_input("y-coordinate", value=flowobj.y, key="y_update")
            strength = st.number_input("Source strength", value=flowobj.strength, key="strength_update")
            alpha = st.number_input("Doublet angle", value=flowobj.alpha, key="update_alphadoublet")

            if st.button("Update", key="tmp3"):
                flowobj.x = float(xpos)
                flowobj.y = float(ypos)
                flowobj.strength = float(strength)
                flowobj.alpha = float(alpha)

                update()

        if type(flowobj) == pfv.Vortex:
            xpos = st.number_input("x-coordinate", value=flowobj.x, key="x_update")
            ypos = st.number_input("y-coordinate", value=flowobj.y, key="y_update")
            strength = st.number_input("Source strength", value=flowobj.strength, key="strength_update")

            if st.button("Update", key="tmp3"):
                flowobj.x = float(xpos)
                flowobj.y = float(ypos)
                flowobj.strength = float(strength)

                update()

        st.markdown("""----""")
