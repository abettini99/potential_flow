#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Library imports
import numpy as np
import numpy.typing as npt
from dataclasses import dataclass, field
try:
    from elemflows.uniform import *
    from elemflows.source import *
    from elemflows.doublet import *
    from elemflows.vortex import *
    from presets.cylinder import *
    from presets.rotatingcylinder import *
except ModuleNotFoundError:
    from lib.elemflows.uniform import *
    from lib.elemflows.source import *
    from lib.elemflows.doublet import *
    from lib.elemflows.vortex import *
    from lib.presets.cylinder import *
    from lib.presets.rotatingcylinder import *

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
    presets: list[object]             = field(init=False, repr=False)

    def __post_init__(self) -> None:
        x_arr = np.linspace( self.xDomain[0], self.xDomain[1], self.Ncells[0]+1, dtype=np.float32 )
        y_arr = np.linspace( self.yDomain[0], self.yDomain[1], self.Ncells[1]+1, dtype=np.float32 )
        self.x, self.y = np.meshgrid(x_arr,y_arr)

        self.u     = np.zeros( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 ) # Remember, rows -> variation in y, columns -> variation in x
        self.v     = np.zeros( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 )
        self.phi   = np.zeros( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 )
        self.psi   = np.zeros( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 )

        self.flowlist = []
        self.presets = []

    def add_UniformFlow(self, Vinfty: float, angle: float) -> None:
        self.flowlist.append( FlowUniform(Vinfty, angle) )
    def add_SourceFlow(self, strength: float, position: tuple[float,float] ) -> None:
        self.flowlist.append( FlowSource(strength, position) )
    def add_DoubletFlow(self, strength: float, position: tuple[float,float] ) -> None:
        self.flowlist.append( FlowDoublet(strength, position) )
    def add_VortexFlow(self, strength: float, position: tuple[float,float] ) -> None:
        self.flowlist.append( FlowVortex(strength, position) )
    def add_Cylinder(self, Vinfty: float, radius: float, position: tuple[float,float] ) -> None:
        self.presets.append( PresetCylinder(Vinfty, radius, position) )
    def add_RotatingCylinder(self, Vinfty: float, strength: float, radius: float, position: tuple[float,float] ) -> None:
        self.presets.append( PresetRotatingCylinder(Vinfty, strength, radius, position) )

    def update_general(self, xDomain: tuple[float,float], yDomain: tuple[float,float], Ncells: tuple[float,float]) -> None:
        self.xDomain = xDomain
        self.yDomain = yDomain
        self.Ncells = Ncells

        x_arr = np.linspace( self.xDomain[0], self.xDomain[1], self.Ncells[0]+1, dtype=np.float32 )
        y_arr = np.linspace( self.yDomain[0], self.yDomain[1], self.Ncells[1]+1, dtype=np.float32 )
        self.x, self.y = np.meshgrid(x_arr,y_arr)

        self.u     = np.zeros( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 ) # Remember, rows -> variation in y, columns -> variation in x
        self.v     = np.zeros( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 )
        self.phi   = np.zeros( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 )
        self.psi   = np.zeros( (self.Ncells[1]+1, self.Ncells[0]+1), dtype=np.float32 )

    def clear(self) -> None:
        self.flowlist = []
        self.presets = []

    def superimpose_fields(self) -> None:
        self.u *= 0
        self.v *= 0
        self.phi *= 0
        self.psi *= 0
        for flow in (self.flowlist + self.presets):
            du, dv, dphi, dpsi = flow.calculate_contribution(self.x, self.y)
            self.u += du
            self.v += dv
            self.phi += dphi
            self.psi += dpsi

if __name__ == "__main__":
    grid: Grid = Grid((-2,2),(-2,2),(121,141))
    # grid.add_UniformFlow(1, 0)
    # grid.add_SourceFlow(2, (0.5,0))
    # grid.add_SourceFlow(-1, (-0.5,0))
    # grid.add_DoubletFlow(1, (0,0))
    # grid.add_VortexFlow(1, (0,0))
    # grid.add_Cylinder(1, 0.5, (0,1))
    grid.add_RotatingCylinder(1, 4*np.pi*1*0.5, 0.5, (0,0))

    grid.superimpose_fields()

    import matplotlib.pyplot as plt

    # plt.contourf(grid.x,grid.y, grid.u, levels = 30)
    plt.contour(grid.x,grid.y, grid.psi, levels = 30, colors='black', linestyles='-')
    plt.show()
