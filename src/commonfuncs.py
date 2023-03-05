#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports
from src.commondicts import TYPE_NAME_DICT

## Functions
def flow_element_type(object):
    """
    Given a flow object, returns the name of the flow type.

    Parameters:
        object : pfv.object
            Flow object that belongs to the potentialflowvisualizer
            module.
    Returns:
        name   : string
            Corresponding string name from the TYPE_NAME_DICT[] dictionary
            of said object.
    """
    try:
        name = TYPE_NAME_DICT[object.__class__]
    except KeyError:
        raise ValueError("The given object is not a flow element")

    if name == "Source" and object.strength < 0:
        name = "Sink"

    return name
