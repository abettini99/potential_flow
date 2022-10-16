#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports
from lib.grid import *
from numpy import deg2rad
import streamlit as st
import matplotlib.pyplot as plt

#### =================== ####
#### Session Information ####
#### =================== ####
# https://docs.streamlit.io/library/advanced-features/session-state

## Grid:
if 'grid' not in st.session_state:
    st.session_state['grid'] = Grid((-1,1),(-1,1),(61,61))

## Update trigger:
if 'update_trigger' not in st.session_state:
    st.session_state['update_trigger'] = False

#### ================ ####
#### Main application ####
#### ================ ####

## App title
st.sidebar.title("Potential Flow Theory Tool")

## Create button for superposition of fields
if st.sidebar.button("Clear grid"):
    st.session_state['grid'].clear()
    st.session_state['update_trigger'] = True
    # st.sidebar.text(grid.flowlist)

## General Test Cases
general, uniform, source, sink, doublet, vortex, cylinder, rotating_cylinder = st.sidebar.tabs(["General", "Uniform", "Source", "Sink", "Doublet", "Vortex", "Cylinder", "Rotating Cylinder"])

with general:
    xmin    = st.number_input("xmin", value=-1.)
    xmax    = st.number_input("xmax", value=1.)
    ymin    = st.number_input("ymin", value=-1.)
    ymax    = st.number_input("ymax", value=1.)
    Nx      = st.number_input("Number of cells in x-direction", value=61.)
    Ny      = st.number_input("Number of cells in y-direction", value=61.)
    if st.button("Update Grid"):
        st.session_state['grid'].update_general( (xmin,xmax), (ymin,ymax), (Nx,Ny) )
        st.session_state['update_trigger'] = True

with uniform:
    speed       = st.number_input("Freestream speed", value=1.)
    angle       = st.number_input("Angle-of-attack in degrees", value=0.)
    if st.button("Add Uniform Flow"):
        st.session_state['grid'].add_UniformFlow( speed, deg2rad(angle) )
        st.session_state['update_trigger'] = True

with source:
    xpos        = st.number_input("x-coordinate", value=0., key='xsource')
    ypos        = st.number_input("y-coordinate", value=0., key='ysource')
    strength    = st.number_input("Source strength", value=1., key='strengthsource')
    if st.button("Add Source"):
        st.session_state['grid'].add_SourceFlow( strength, (xpos,ypos) )
        st.session_state['update_trigger'] = True

with sink:
    xpos        = st.number_input("x-coordinate", value=0., key='xsink')
    ypos        = st.number_input("y-coordinate", value=0., key='ysink')
    strength    = st.number_input("Sink strength", value=1., key='strengthsink')
    if st.button("Add Sink"):
        st.session_state['grid'].add_SourceFlow( -strength, (xpos,ypos) )
        st.session_state['update_trigger'] = True

with doublet:
    xpos        = st.number_input("x-coordinate", value=0., key='xdoublet')
    ypos        = st.number_input("y-coordinate", value=0., key='ydoublet')
    strength    = st.number_input("Doublet strength", value=1., key='strengthdoublet')
    if st.button("Add Doublet"):
        st.session_state['grid'].add_DoubletFlow( strength, (xpos,ypos) )
        st.session_state['update_trigger'] = True

with vortex:
    xpos        = st.number_input("x-coordinate", value=0., key='xvortex')
    ypos        = st.number_input("y-coordinate", value=0., key='yvortex')
    strength    = st.number_input("Vortex strength", value=1., key='strengthvortex')
    if st.button("Add Vortex"):
        st.session_state['grid'].add_VortexFlow( strength, (xpos,ypos) )
        st.session_state['update_trigger'] = True

with cylinder:
    xpos        = st.number_input("x-coordinate", value=0., key='xcylinder')
    ypos        = st.number_input("y-coordinate", value=0., key='ycylinder')
    speed       = st.number_input("Freestream speed", value=1., key='speedcylinder')
    radius      = st.number_input("Cylinder radius", value=1., key='radiuscylinder')
    if st.button("Add Non-rotating Cylinder"):
        st.session_state['grid'].add_Cylinder( speed, radius, (xpos,ypos) )
        st.session_state['update_trigger'] = True

with rotating_cylinder:
    xpos        = st.number_input("x-coordinate", value=0., key='xrotatingcylinder')
    ypos        = st.number_input("y-coordinate", value=0., key='yrotatingcylinder')
    speed       = st.number_input("Freestream speed", value=1., key='speedrotatingcylinder')
    strength    = st.number_input("Vortex strength", value=1., key='strengthrotatingcylinder')
    radius      = st.number_input("Cylinder radius", value=1., key='radiusrotatingcylinder')
    if st.button("Add Rotating Cylinder"):
        st.session_state['grid'].add_RotatingCylinder( speed, strength, radius, (xpos,ypos))
        st.session_state['update_trigger'] = True


#### ================== ####
#### Update Information ####
#### ================== ####

## Update important things
if st.session_state['update_trigger']:
    ## Superimpose solutions
    st.session_state['grid'].superimpose_fields()

    ## Plot
    fig, ax = plt.subplots(2,2, sharex=True, sharey=True, squeeze=False)
    ax[0,0].contourf(st.session_state['grid'].x, st.session_state['grid'].y, st.session_state['grid'].u, levels=10)
    ax[0,0].set_title('u')
    ax[0,1].contourf(st.session_state['grid'].x, st.session_state['grid'].y, st.session_state['grid'].v, levels=10)
    ax[0,1].set_title('v')
    ax[1,0].contour(st.session_state['grid'].x, st.session_state['grid'].y, st.session_state['grid'].psi, levels=30, colors='black', linestyles='-')
    ax[1,0].set_title(r'$\psi$')
    ax[1,1].contour(st.session_state['grid'].x, st.session_state['grid'].y, st.session_state['grid'].phi, levels=30, colors='black', linestyles='-')
    ax[1,1].set_title(r'$\phi$')
    st.pyplot(fig)

    ## Remove update trigger at the end of update
    st.session_state['update_trigger'] = False
