import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import matplotlib.pyplot as plt

class VortexFilament:
    def __init__(self, strength, point, vector,start=None, end=None, prop = None):
        self.children=[]
        self.Strength = strength
        self.Point = np.array(point)
        self.vector = np.array(vector)
        self.vector = self.vector/np.linalg.norm(self.vector)
        self.start = start
        self.end = end
        self.prop = prop
    def calculate_velocity(self, coord):
        h, sign= self.calculate_h(coord)
        if self.start is not None:
            starting = np.dot(coord-self.start,self.vector)/(np.linalg.norm(coord-self.start)*np.linalg.norm(self.vector))
        elif self.end is not None:
            ending = np.dot(coord-self.end,self.vector)/(np.linalg.norm(coord-self.end)*np.linalg.norm(self.vector))
        
        if self.start is None and self.end is None:
            return self.Strength/(2*np.pi*h)*sign
        elif self.start is not None and self.end is None:
            return self.Strength/(4*np.pi*h)*(starting+1)*sign
        elif self.end is not None and self.start is None:
            return self.Strength/(4*np.pi*h)*(1-ending)*sign
        else:
            return self.Strength/(4*np.pi*h)*(starting-ending)*sign
    def calculate_h(self, coord):
        AP = np.array(coord)-self.Point
        cross_product = np.cross(self.vector,AP)
        sign = np.sign(cross_product[2])
        return np.linalg.norm(cross_product)/(np.linalg.norm(self.vector)), sign
    def eq_of_filament(self,mu):
        return self.point+mu*self.vector
    def check_point_on_line(self, coord):
        mu=np.zeros(3)
        Threshold = 0.000001
        if 0 in self.vector:
            zero_element = np.where(self.vector == 0)[0]
            non_zero_element = np.where(self.vector != 0)[0]
            for i in non_zero_element:
                mu[i] = (coord[i]-self.Point[i])/self.vector[i]
            for i in zero_element:
                if abs(coord[i] -self.Point[i])>Threshold:
                    return False
                else:
                    mu[i]=mu[np.random.choice(non_zero_element)]
        else:
            mu = coord-self.Point/self.vector
        
        if abs(mu[0] - mu[1]) > Threshold or abs(mu[0] - mu[2]) > Threshold or abs(mu[1] - mu[2]) > Threshold:
            return False
        return True, mu[0]
    def split(self, Strengths, coord, angles):
        self.check_point_on_line(coord)
        self.end = coord
        for i in angles:
            if i>np.pi or i<np.pi:
                i=i*np.pi/180
            vec = np.array([self.vector[0]*np.cos(i)-self.vector[1]*np.sin(i),self.vector[0]*np.sin(i)+self.vector[1]*np.cos(i),0])
            self.children.append(VortexFilament(Strengths[i]*self.Strength, coord, vec, start = coord,prop = Strengths[i]))
    def bend(self, coord, vec):
        self.check_point_on_line(coord)
        self.end = coord
        self.children.append(VortexFilament(self.Strength, coord, vec, start = coord))

    def calc_vortex_family(self,parent_strength = None):
        if self.prop is not None and parent_strength is not None:
            self.Strength = self.prop*parent_strength
        for i in self.children:
            i.draw_vortex_family(self.Strength)
    def draw_vortex_family(self, limit_x, limit_y):
        self.calc_vortex_family(self.Strength)
        if self.start is not None and self.end is not None:
            plt.plot([self.start[0],self.end[0]],[self.start[1],self.end[1]],'k')
        elif self.start is not None and self.end is None:
            plt.plot([self.start[0],self.Point[0]],[self.start[1],self.Point[1]],'k')
        elif self.start is None and self.end is not None:
            plt.plot([self.Point[0],self.end[0]],[self.Point[1],self.end[1]],'k')
        else:
            plt.plot([self.Point[0],self.Point[0]+self.vector[0]],[self.Point[1],self.Point[1]+self.vector[1]],'k')

class VortexFilamentCollection:
    def __init__(self):
        self.filaments = []
    def add_filament(self, strength, point, vector, start=None, end=None):
        self.filaments.append(VortexFilament(strength, point, vector, start, end))

def vortfil():
    return html.Div(children=[
    
    #### ============== ####
    #### BUILDING BLOCK ####
    #### ============== ####
    html.H1("Vrotex Filaments"),

    dcc.Markdown('''
    \\[...\\] \n
                 
    The velocity around a source/sink is then given by
                 
    $$
    V_r = \\frac{\\Lambda}{2\\pi r}\\,,
    $$
    $$
    V_\\theta = 0\\,.
    $$

    Which as a set of cartesian velocities can be found by      
    EXAMPLE TEXT: \n
    bla bla bla
    ''',mathjax=True),

    html.Label('Strength Slider:'),
    dcc.Slider(-2, 2,
               value=1,
               id='sourceStrength1',
              ),

    html.Label('Source Position:'),
    dcc.Slider(-1, 1,
               value=0,
               id='Px',
               marks={-1: {'label': '-1'},
                       0: {'label': '0'},
                       1: {'label': '1'}}
              ),
    dcc.Slider(-1, 1,
               value=0,
               id='Py',
               marks={-1: {'label': '-1'},
                       0: {'label': '0'},
                       1: {'label': '1'}}
              ),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourcePS', mathjax=True),
        ], width=4)
    ], justify='center'),
    


    #### ============= ####
    #### APPLICATION 1 ####
    #### ============= ####
    html.Hr(),
    html.H2("Application: Source + Uniform"),

    dcc.Markdown('''
    bla bla bla bla bla, velocity graph 2
    ''',mathjax=True),
    

    html.Label('Source Strength Slider:'),
    dcc.Slider(0, 2,
               value=1,
               id='sourceStrength2',
              ),
    html.Label('Freestream Velocity Slider:'),
    dcc.Slider(0.1, 2,
               value=1,
               id='VelInfMagSourceUniform',
              ),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceuniformV', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceuniformPS', mathjax=True),
        ], width=4)
    ], justify='center'),


    dcc.Markdown('''
    We can also look at quantities over the body contour...
    ''',mathjax=True),

    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceuniformVelS', mathjax=True),
        ], width=6)
    ], justify='center'),
    ## Graph updated via app.callable() in main.py
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sourceuniformCpS', mathjax=True),
        ], width=6)
    ], justify='center')
    ])

if __name__ == '__main__':
    test = VortexFilament(1,[1,1,0],[1,-1,0])
    print(test.calculate_h([0,0,0]))
    print(test.calculate_velocity([0,0,0]))
    print(test.calculate_velocity([2,2,0]))
    test.start = np.array([1,1,0])
    print(test.calculate_velocity([0,0,0]))
    test.start = np.array([0,2,0])
    print(test.calculate_velocity([0,0,0]))
    print(test.check_point_on_line([-1,3,0]))
    
