from src.commondicts import TYPE_NAME_DICT

def flow_element_type(object):
    try:
        name = TYPE_NAME_DICT[object.__class__]
    except KeyError:
        raise ValueError("The given object is not a flow element")

    if name == "Source" and object.strength < 0:
        name = "Sink"

    return name
