#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports
import numpy as np
import numpy.typing as npt
from dataclasses import dataclass, field

# Functions / Classes
@dataclass() # Not super necessary to have this decorator for this to work, but it is still nice to have.
class PresetRotatingCylinder:

    #### ============ ####
    #### Class inputs ####
    #### ============ ####
    Vinfty: float
    strength: float
    radius: float
    position: tuple[float,float]

    x0: float = field(init=False, repr=False)
    y0: float = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.x0 = self.position[0]
        self.y0 = self.position[1]

    def calculate_contribution(self, x, y) -> tuple[npt.NDArray[np.float32],npt.NDArray[np.float32],npt.NDArray[np.float32],npt.NDArray[np.float32]]:
        dx      = x - self.x0
        dy      = y - self.y0
        r       = np.sqrt(dx*dx + dy*dy)
        theta   = np.arctan2(dy,dx)

        Vr      = self.Vinfty*r*np.sin(theta) * (1-(self.radius/r)**2)
        Vtheta  = -self.Vinfty*np.sin(theta) * (1+(self.radius/r)**2) - self.strength/(2*np.pi*r)

        du      = Vr*np.cos(theta) - Vtheta*np.sin(theta)
        dv      = Vr*np.sin(theta) + Vtheta*np.cos(theta)
        dphi    = self.Vinfty*r*np.cos(theta) * (1+(self.radius/r)**2) - self.strength/(2*np.pi)*theta
        dpsi    = self.Vinfty*r*np.sin(theta) * (1-(self.radius/r)**2) + self.strength/(2*np.pi)*np.log(r/self.radius) # base e already

        return du, dv, dphi, dpsi
