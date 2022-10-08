#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports
import numpy as np
import numpy.typing as npt
from dataclasses import dataclass, field
try:
    from flow_uniform import *
    from flow_source import *
    from flow_doublet import *
    from flow_vortex import *
except ModuleNotFoundError:
    from lib.flow_uniform import *
    from lib.flow_source import *
    from lib.flow_doublet import *
    from lib.flow_vortex import *

# Functions / Classes
@dataclass() # Not super necessary to have this decorator for this to work, but it is still nice to have.
class Grid:

    #### ============ ####
    #### Class inputs ####
    #### ============ ####
    xDomain: tuple[float,float]          ## Domain boundaries (start, end)
    yDomain: tuple[float,float]          ## Domain boundaries (start, end)
    Ncells: tuple[int,int]               ## Number of cells in (x,y)

    #### =================== ####
    #### Post-init variables ####
    #### =================== ####
    x: npt.NDArray[np.float32]        = field(init=False, repr=False)
    y: npt.NDArray[np.float32]        = field(init=False, repr=False)
    u: npt.NDArray[np.float32]        = field(init=False, repr=False)
    v: npt.NDArray[np.float32]        = field(init=False, repr=False)
    phi: npt.NDArray[np.float32]      = field(init=False, repr=False)
    psi: npt.NDArray[np.float32]      = field(init=False, repr=False)
    flowlist: list[object]            = field(init=False, repr=False)

    def __post_init__(self) -> None:
        x_arr = np.linspace( self.xDomain[0], self.xDomain[1], self.Ncells[0]+1, dtype=np.float32 )
        y_arr = np.linspace( self.yDomain[0], self.yDomain[1], self.Ncells[1]+1, dtype=np.float32 )
        self.x, self.y = np.meshgrid(x_arr,y_arr)

        self.u     = np.empty( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 ) # Remember, rows -> variation in y, columns -> variation in x
        self.v     = np.empty( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 )
        self.phi   = np.empty( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 )
        self.psi   = np.empty( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 )

        self.flowlist = []

    def add_UniformFlow(self, Vinfty: float, angle: float) -> None:
        self.flowlist.append( FlowUniform(Vinfty, angle) )

    def add_SourceFlow(self, strength: float, position: tuple[float,float] ) -> None:
        self.flowlist.append( FlowSource(strength, position) )

    def add_DoubletFlow(self, strength: float, position: tuple[float,float] ) -> None:
        self.flowlist.append( FlowDoublet(strength, position) )

    def add_VortexFlow(self, strength: float, position: tuple[float,float] ) -> None:
        self.flowlist.append( FlowVortex(strength, position) )

    def calculate_fields(self) -> None:
        self.u *= 0
        self.v *= 0
        self.phi *= 0
        self.psi *= 0
        for flow in self.flowlist:
            du, dv, dphi, dpsi = flow.calculate_contribution(self.x, self.y)
            self.u += du
            self.v += dv
            self.phi += dphi
            self.psi += dpsi

if __name__ == "__main__":


    grid: Grid = Grid((-1,1),(-1,1),(30,35))
    grid.add_UniformFlow(1, np.deg2rad(0))
    # grid.add_SourceFlow(1, (0.5,0))
    # grid.add_SourceFlow(-1, (-0.5,0))
    grid.add_DoubletFlow(1, (0,0))
    grid.add_VortexFlow(1, (0,0))

    grid.calculate_fields()

    import matplotlib.pyplot as plt

    plt.contour(grid.x,grid.y, grid.psi, levels = 50)
    plt.show()
