#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports
import numpy as np
import numpy.typing as npt
from dataclasses import dataclass, field

# Functions / Classes
@dataclass() # Not super necessary to have this decorator for this to work, but it is still nice to have.
class FlowUniform:

    #### ============ ####
    #### Class inputs ####
    #### ============ ####
    Vinfty: float
    angle: float

    type: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.type = 'Uniform'

    def calculate_contribution(self, x, y) -> tuple[float,float,npt.NDArray[np.float32],npt.NDArray[np.float32]]:
        du      = self.Vinfty*np.cos(self.angle)
        dv      = self.Vinfty*np.sin(self.angle)

        dphi_u  = self.Vinfty*np.cos(self.angle)*x
        dphi_v  = self.Vinfty*np.sin(self.angle)*y
        dphi    = dphi_u + dphi_v

        dpsi_u  =  self.Vinfty*np.cos(self.angle)*y
        dpsi_v  = -self.Vinfty*np.sin(self.angle)*x
        dpsi    = dpsi_u + dpsi_v

        return du, dv, dphi, dpsi
