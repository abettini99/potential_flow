#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports
import potentialflowvisualizer as pfv
import math as m

## Dictionaries
"""
String name attached to flow objects from potentialflowvisualizer module.
Dictionary used in the flow_element_type() function.
"""
TYPE_NAME_DICT = {
    pfv.Freestream  : "Uniform",
    pfv.Source      : "Source",
    pfv.Doublet     : "Doublet",
    pfv.Vortex      : "Vortex",
    pfv.LineSource  : "LineSource",
}

"""
String name used in main.py for adding presets to the flow.
"""
## TODO: Default values for presets
PRESET_DEFAULT_DICT = {
    "Cylinder"          : [pfv.Freestream(1, 0), pfv.Doublet(1*(2*m.pi*1), 0, 0, m.pi)],
    "Rotating Cylinder" : [pfv.Freestream(1, 0), pfv.Doublet(1*(2*m.pi*1), 0, 0, m.pi), pfv.Vortex(4*m.pi*1*1, 0, 0)],
}

"""
String name used in main.py for adding elements to the flow.
"""
ELEMENT_DEFAULT_DICT = {
    "Uniform"   : pfv.Freestream(1, 0),
    "Source"    : pfv.Source(1, 0, 0),
    "Sink"      : pfv.Source(-1, 0, 0),
    "Doublet"   : pfv.Doublet(1, 0, 0, m.pi),
    "Vortex"    : pfv.Vortex(1, 0, 0),
    "LineSource": pfv.LineSource(1, 0, 0, 1, 0),
}

"""
Full names of plot titles used in the draw() function.
"""
LONG_NAME_DICT = {
    "potential": "Velocity Potential",
    "streamfunction": "Stream Function",
    "xvel": "x Velocity",
    "yvel": "y Velocity",
    "velmag": "Velocity Magnitude",
    "pressure": "Pressure Coefficient",
}
