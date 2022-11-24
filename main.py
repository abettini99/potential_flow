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

    # Prepare image
    utils.prepare_graphs()
    fig, ax = plt.subplots(2,2, sharex=True, sharey=True, squeeze=False, figsize=(16,16))
    for axe in ( ax[0,0], ax[0,1], ax[1,0], ax[1,1] ):
        axe.set_xlim(st.session_state['grid'].xDomain[0], st.session_state['grid'].xDomain[1])
        axe.set_ylim(st.session_state['grid'].yDomain[0], st.session_state['grid'].yDomain[1])
        axe.grid(True,which="major",color="#999999",alpha=0.75)
        axe.grid(True,which="minor",color="#DDDDDD",ls="--",alpha=0.50)
        axe.minorticks_on()
        axe.tick_params(which='major', length=10, width=2, direction='inout')
        axe.tick_params(which='minor', length=5, width=2, direction='in')

    # https://scipython.com/blog/visualizing-a-vector-field-with-matplotlib/
    # Matplotlib streamplots
    ax[0,0].set_title(r'$\psi$, matplotlib.streamplot')
    ax[0,1].set_title(r'$\phi$, matplotlib.streamplot')
    # Potential flow plots
    ax[1,0].set_title(r'$\psi$, potential flow theory')
    ax[1,1].set_title(r'$\phi$, potential flow theory')
    # Save figure
    plt.savefig('images\streamline_potential.png', bbox_inches='tight')

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
    Nx      = 61 # st.number_input("Number of cells in x-direction", value=61)
    Ny      = 61 # st.number_input("Number of cells in y-direction", value=61)
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

    utils.prepare_graphs()
    fig, ax = plt.subplots(2,2, sharex=True, sharey=True, squeeze=False, figsize=(16,16))
    for axe in ( ax[0,0], ax[0,1], ax[1,0], ax[1,1] ):
        axe.set_xlim(st.session_state['grid'].xDomain[0], st.session_state['grid'].xDomain[1])
        axe.set_ylim(st.session_state['grid'].yDomain[0], st.session_state['grid'].yDomain[1])
        axe.grid(True,which="major",color="#999999",alpha=0.75)
        axe.grid(True,which="minor",color="#DDDDDD",ls="--",alpha=0.50)
        axe.minorticks_on()
        axe.tick_params(which='major', length=10, width=2, direction='inout')
        axe.tick_params(which='minor', length=5, width=2, direction='in')

    # https://scipython.com/blog/visualizing-a-vector-field-with-matplotlib/
    # Matplotlib streamplots
    ax[0,0].set_title(r'$\psi$, matplotlib.streamplot')
    ax[0,1].set_title(r'$\phi$, matplotlib.streamplot')
    ax[0,0].streamplot(st.session_state['grid'].x, st.session_state['grid'].y, st.session_state['grid'].u, st.session_state['grid'].v,
        linewidth=1, cmap=plt.cm.inferno, density=1, arrowstyle='->', arrowsize=2.0)
    ax[0,1].streamplot(st.session_state['grid'].x, st.session_state['grid'].y, -st.session_state['grid'].v, st.session_state['grid'].u,
        linewidth=1, cmap=plt.cm.inferno, density=1, arrowstyle='-', arrowsize=0.0) # Using the definition of the streamfunction

    # Potential flow plots
    ax[1,0].set_title(r'$\psi$, potential flow theory')
    ax[1,1].set_title(r'$\phi$, potential flow theory')
    ax[1,0].contour(st.session_state['grid'].x, st.session_state['grid'].y, st.session_state['grid'].psi, levels=30, colors='black', linestyles='-')
    ax[1,1].contour(st.session_state['grid'].x, st.session_state['grid'].y, st.session_state['grid'].phi, levels=30, colors='black', linestyles='-')

    # Save figure
    plt.savefig('images\streamline_potential.png', bbox_inches='tight')

    ## Remove update trigger at the end of update
    st.session_state['update_trigger'] = False


# st.text(st.session_state['path']  + '\images\streamline_potential.png')
image = Image.open('images\streamline_potential.png')
st.image(image, use_column_width = True)

## Do a super-hack:
## I would normally not do the redundant line of making option = flowobj
## but it seems that option is a session-state variable, and not the actual grid object itself
## therefore you cannot modify option, but can modify flowobj
if not len(st.session_state['grid'].flowlist) == 0:
    option = st.selectbox("TEST", options=st.session_state['grid'].flowlist)
    flowobj = [obj for obj in st.session_state['grid'].flowlist if obj == option][0]

    if flowobj.type == 'Uniform':
        speed       = st.number_input("Freestream speed", value=flowobj.Vinfty, key='speed_update')
        angle       = st.number_input("Angle-of-attack in degrees", value=flowobj.angle, key='angle_update')

        if st.button("Update",key='tmp3'):
            flowobj.Vinfty = float(speed)
            flowobj.angle = float(angle)

            st.session_state['update_trigger'] = True

    if flowobj.type == 'Source':
        xpos        = st.number_input("x-coordinate", value=flowobj.x0, key='x_update')
        ypos        = st.number_input("y-coordinate", value=flowobj.y0, key='y_update')
        strength    = st.number_input("Source strength", value=flowobj.strength, key='strength_update')

        if st.button("Update",key='tmp3'):
            flowobj.position = (float(xpos),float(ypos))
            flowobj.x0 = float(xpos)
            flowobj.y0 = float(ypos)
            flowobj.strength = float(strength)

            st.session_state['update_trigger'] = True

    if flowobj.type == 'Doublet':
        xpos        = st.number_input("x-coordinate", value=flowobj.x0, key='x_update')
        ypos        = st.number_input("y-coordinate", value=flowobj.y0, key='y_update')
        strength    = st.number_input("Source strength", value=flowobj.strength, key='strength_update')

        if st.button("Update",key='tmp3'):
            flowobj.position = (float(xpos),float(ypos))
            flowobj.x0 = float(xpos)
            flowobj.y0 = float(ypos)
            flowobj.strength = float(strength)

            st.session_state['update_trigger'] = True

    if flowobj.type == 'Vortex':
        xpos        = st.number_input("x-coordinate", value=flowobj.x0, key='x_update')
        ypos        = st.number_input("y-coordinate", value=flowobj.y0, key='y_update')
        strength    = st.number_input("Source strength", value=flowobj.strength, key='strength_update')

        if st.button("Update",key='tmp3'):
            flowobj.position = (float(xpos),float(ypos))
            flowobj.x0 = float(xpos)
            flowobj.y0 = float(ypos)
            flowobj.strength = float(strength)

            st.session_state['update_trigger'] = True
