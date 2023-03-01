import potentialflowvisualizer as pfv

TYPE_NAME_DICT = {
    pfv.Freestream  : "Uniform",
    pfv.Source      : "Source",
    pfv.Doublet     : "Doublet",
    pfv.Vortex      : "Vortex",
    pfv.LineSource  : "LineSource",
}

PRESET_DICT = {
    "Cylinder"          : [pfv.Freestream(1, 0), pfv.Doublet(1, 0, 0, 0)],
    "Rotating Cylinder" : [pfv.Freestream(1, 0), pfv.Doublet(1, 0, 0, 0), pfv.Vortex(1, 0, 0)],
}

ELEMENT_DEFAULT_DICT = {
    "Uniform"   : pfv.Freestream(1, 0),
    "Source"    : pfv.Source(1, 0, 0),
    "Sink"      : pfv.Source(-1, 0, 0),
    "Doublet"   : pfv.Doublet(1, 0, 0, 0),
    "Vortex"    : pfv.Vortex(1, 0, 0),
    "LineSource": pfv.LineSource(1, 0, 0, 1, 0),
}

LONG_NAME_DICT = {
    "potential": "Velocity Potential",
    "streamfunction": "Stream Function",
    "xvel": "x Velocity",
    "yvel": "y Velocity",
    "velmag": "Velocity Magnitude",
    "pressure": "Pressure Coefficient",
}
