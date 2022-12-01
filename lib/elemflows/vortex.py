#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports
import numpy as np
import numpy.typing as npt
from dataclasses import dataclass, field

# Functions / Classes
@dataclass() # Not super necessary to have this decorator for this to work, but it is still nice to have.
class FlowVortex:

    #### ============ ####
    #### Class inputs ####
    #### ============ ####
    strength: float
    position: tuple[float,float]

    x0: float = field(init=False, repr=False)
    y0: float = field(init=False, repr=False)
    type: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.type = 'Vortex'
        self.x0 = self.position[0]
        self.y0 = self.position[1]

    def calculate_contribution(self, x, y) -> tuple[npt.NDArray[np.float32],npt.NDArray[np.float32],npt.NDArray[np.float32],npt.NDArray[np.float32]]:
        dx      = x - self.x0
        dy      = y - self.y0
        r       = np.sqrt(dx*dx + dy*dy)
        theta   = np.arctan2(dy,dx)

        #Vr      = 0
        Vtheta  = -self.strength/(2*np.pi*r)

        du      = -Vtheta*np.sin(theta) # + Vr*np.cos(theta)
        dv      = Vtheta*np.cos(theta) # + Vr*np.sin(theta)
        dphi    = -self.strength/(2*np.pi)*theta
        dpsi    = self.strength/(2*np.pi)*np.log(r) # already base e

        return du, dv, dphi, dpsi
