import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import scipy.spatial.transform as transform_sp

class VortexFilament:
    def __init__(self, strength, point, vector,start=None, end=None, prop = None):
        self.children=[]
        self.parent = None
        self.Strength = strength
        self.Point = np.array(point)
        self.vector = np.array(vector)
        self.vector = self.vector/np.linalg.norm(self.vector)
        if start is not None:
            self.start = np.array(start)
        else:
            self.start = start
        if end is not None:
            self.end = np.array(end)
        else:
            self.end = end
        self.prop = prop

        self.new_vector = None
        self.new_Point = None
        self.new_start = None
        self.new_end = None

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
        coord = np.array(coord)
        self.end = coord
        for i in range(len(angles)):
            if angles[i]>np.pi or angles[i]<-np.pi:
                angles[i]=angles[i]*np.pi/180
            vec = np.array([self.vector[0]*np.cos(angles[i])-self.vector[1]*np.sin(angles[i]),self.vector[0]*np.sin(angles[i])+self.vector[1]*np.cos(angles[i]),0])
            self.children.append(VortexFilament(Strengths[i]*self.Strength, coord, vec, start = coord,prop = Strengths[i]))
        for i in self.children:
            i.parent = self

    def bend(self, coord, angle):
        self.check_point_on_line(coord)
        coord = np.array(coord)
        self.end = coord
        angle=angle*np.pi/180
        vec = np.array([self.vector[0]*np.cos(angle)-self.vector[1]*np.sin(angle),self.vector[0]*np.sin(angle)+self.vector[1]*np.cos(angle),0])
        self.children.append(VortexFilament(self.Strength, coord, vec, start = coord))
        for i in self.children:
            i.parent = self

    def calc_vortex_family(self,parent_strength = None):
        if self.prop is not None and parent_strength is not None:
            self.Strength = self.prop*parent_strength
        for i in self.children:
            i.calc_vortex_family(self.Strength)
        
    def draw_vortex_family(self, limit_x, limit_y,fig=None, transform = None):
        if transform is not None:

            self.new_vector = np.dot(transform,self.vector)
            self.new_Point = np.dot(transform,self.Point)

            if self.start is not None:
                self.new_start = np.dot(transform,self.start)
            if self.end is not None:
                self.new_end = np.dot(transform,self.end)
        else:
            self.new_vector = self.vector
            self.new_Point = self.Point
            if self.start is not None:
                self.new_start = self.start
            if self.end is not None:
                self.new_end = self.end
        
        
        self.calc_vortex_family(self.Strength)
        box = self.calculate_box_intersection(limit_x, limit_y)
        if self.start is not None and self.end is not None:
            limit = np.array([self.new_start[0],self.new_end[0],self.new_start[1],self.new_end[1]])
        elif self.start is not None and self.end is None:
            limit = np.array([self.new_start[0],box[1][0],self.new_start[1],box[1][1]])
        elif self.start is None and self.end is not None:
            limit = np.array([box[0][0],self.new_end[0],box[0][1],self.new_end[1]])
        else:
            limit = np.array([box[0][0],box[1][0],box[0][1],box[1][1]])
            
        # Add a trace for the straight line
        x_arr = np.linspace(limit[0], limit[1], 100)
        y_arr = np.linspace(limit[2], limit[3], 100)

        # plt.plot(x_arr,y_arr)
        
        if fig is None: 
            fig = go.Figure()        
            fig.update_layout(xaxis_title='X-axis',
                              yaxis_title='Y-axis',
                              title='Straight Line Plot'
                              )
            fig.update_xaxes(range=[limit_x[0]*transform[0,0], limit_x[1]*transform[0,0]])  # Set x-axis limits
            fig.update_yaxes(range=[limit_y[0]*transform[1,1], limit_y[1]*transform[1,1]])  # Set y-axis limits

            fig.update_xaxes(range=[limit_x[0], limit_x[1]])  # Set x-axis limits
            fig.update_yaxes(range=[limit_y[0], limit_y[1]])  # Set y-axis limits

            limit_interval_x = limit_x[1]-limit_x[0]
            limit_interval_y = limit_y[1]-limit_y[0]

            grids_x = np.linspace(limit_x[0], limit_x[1], int(limit_interval_x))
            grids_y = np.linspace(limit_y[0], limit_y[1], int(limit_interval_y))
            for i in grids_x:
                x_arr_grid = ([i*transform[0,0]-10*transform[0,1], i*transform[0,0]+10*transform[0,1]])
                y_arr_grid = ([-10*transform[1,1]+i*transform[1,0], 10*transform[1,1]+i*transform[1,0]])
                
                fig.add_shape(type="line", x0=x_arr_grid[0], y0=y_arr_grid[0], x1=x_arr_grid[1], y1=y_arr_grid[1], line=dict(color="grey", width=0.5))
            for i in grids_y:

                x_arr_grid = ([-10*transform[0,0]+i*transform[0,1], 10*transform[0,0]+i*transform[0,1]])
                y_arr_grid = ([i*transform[1,1]-10*transform[1,0], i*transform[1,1]+10*transform[1,0]])

                fig.add_shape(type="line", x0=x_arr_grid[0], y0=y_arr_grid[0], x1=x_arr_grid[1], y1=y_arr_grid[1], line=dict(color="grey", width=0.5))
        

        fig.add_trace(go.Scatter(x=x_arr, y=y_arr,
                                mode='lines', 
                                line=dict(color='blue', width=2),
                                name='Straight Line'))
        
        # Set axis labels

        for i in self.children:
            i.draw_vortex_family(limit_x, limit_y, fig, transform)
        return fig

    def calculate_box_intersection(self, limit_x, limit_y):
        box_intersection = []
        y_intersects = []
        x_intersects = []
        if self.new_vector is not None:
            for i in limit_x:
                y_intersects.append((i-self.new_Point[0])/self.new_vector[0]*self.new_vector[1]+self.new_Point[1])
            for i in limit_y:
                x_intersects.append((i-self.new_Point[1])/self.new_vector[1]*self.new_vector[0]+self.new_Point[0])
        else:
            for i in limit_x:
                y_intersects.append((i-self.Point[0])/self.vector[0]*self.vector[1]+self.Point[1])
            for i in limit_y:
                x_intersects.append((i-self.Point[1])/self.vector[1]*self.vector[0]+self.Point[0])

        if y_intersects[0]>limit_y[0] and y_intersects[0]<limit_y[1]:
            box_intersection.append([limit_x[0],y_intersects[0]])
        if y_intersects[1]>limit_y[0] and y_intersects[1]<limit_y[1]:
            box_intersection.append([limit_x[1],y_intersects[1]])
        if x_intersects[0]>limit_x[0] and x_intersects[0]<limit_x[1]:
            box_intersection.append([x_intersects[0],limit_y[0]])
        if x_intersects[1]>limit_x[0] and x_intersects[1]<limit_x[1]:
            box_intersection.append([x_intersects[1],limit_y[1]])
        
        t_box = []
        

        for i in box_intersection:
            t_box.append((i[0]-self.new_Point[0])/self.new_vector[0])
        if t_box[0]>t_box[1]:
            box_intersection[0],box_intersection[1] = box_intersection[1],box_intersection[0]
        # print("t_box",t_box)

        return np.array(box_intersection)
    
    def to_dict(self):
        # Convert the VortexFilament object to a dictionary for storage
        dict = {
            'Gamma': self.Strength,
            'Point': self.Point.tolist(),  # Convert numpy arrays to lists
            'vec': self.vector.tolist()  # Convert numpy arrays to lists
        }
        if self.start is not None:
            dict['start'] = self.start.tolist()
        else:
            dict['start'] = None
        if self.end is not None:
            dict['end'] = self.end.tolist()
        else:
            dict['end'] = None
        if self.prop is not None:
            dict['prop'] = self.prop
        else:
            dict['prop'] = None
        dict['children'] = []

        for i in self.children:
            dict['children'].append(i.to_dict())
        return dict

    @staticmethod
    def from_dict(data):
        # Recreate the VortexFilament object from a dictionary
        vec = np.array(data['vec'])
        obj = VortexFilament(data['Gamma'], data['Point'], vec, data['start'], data['end'], data['prop'])
        for i in data['children']:
            obj.children.append(VortexFilament.from_dict(i))
        return obj
        

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
    html.H1("Vortex Filaments"),

    dcc.Markdown('''
    \\[...\\] \n
    Helmholtz's vortex theorems: \n
    The circulation strength $\\Gamma$ remains constant along the filament \n
    a vortex filament cannot end in the flow, but: \n
    extends to infinity\n
    ends at a boundary\n
    forms a closed loop\n

    Bior Savart Law: \n

    $$
    d\\vec{V} = \\frac{\\Gamma}{4\\pi} \\frac{d\\vec{l} \\times \\vec{r}}{|\\vec{r}|^3}
    $$
    For a straight filament, the velocity field is given by: \n
    $$
    \\vec{V} = \\frac{\\Gamma}{4\\pi} \\int_{A}^{B} \\frac{sin(\\theta)}{r^2} d\\vec{l}
    $$
    ''',mathjax=True),
    
    html.H2("Vortex Filament tool"),
    dcc.Markdown('''
                 ''',mathjax=True),    
    html.Div(
        style={'display': 'flex', 'justifyContent': 'center', 'gap': '10px', 'alignItems': 'center', 'marginTop': '20px'},
        children=[
            html.Label('x:', style={'marginRight': '5px'}),
            dcc.Input(id='x_point_intercept', type='number', step=0.1, value=0),
            html.Label('y:', style={'marginLeft': '20px', 'marginRight': '5px'}),
            dcc.Input(id='y_point_intercept', type='number', step=0.1, value=0)
        ]),

    html.Br(),

    dcc.Store(id='filam-store'),  # Hidden store for Filam object
    dcc.Store(id='transform-store'),  # Hidden store for Filam object
    
    html.Label('Strength Slider:'),
    dcc.Slider(-2, 2,
               value=1,
               id='VortexStrength',
              ),

    html.Label('Angle Slider:    '),
    dcc.Slider(-180, 180,
                value=0,
                id='VortexAngle',
                ),

    html.Button('Draw', id='draw-button', n_clicks=0),

    ## Graph updated via app.callable() in main.py
    dcc.Graph(id='vort', config={'clickmode': 'event+select'}),  # Enable clickmode to select points
    
    html.Div(id='selected-point-output'),  # Output the selected point here
    html.Label('First split angle:'),
    dcc.Slider(-180, 180,
               value=1,
               id='angle_1',
              ),

    html.Label('Angle Slider:    '),
    dcc.Slider(-180, 180,
                value=0,
                id='angle_2',
                ),
    html.Button('Split', id='split-button', n_clicks=0),




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
    roll_angle = -np.deg2rad(60)
    pitch_angle = -np.deg2rad(20)
    roll_angle2 = np.deg2rad(0)

    roll_transform = np.array([[1,0,0],[0,np.cos(roll_angle),-np.sin(roll_angle)],[0,np.sin(roll_angle),np.cos(roll_angle)]])
    pitch_transform = np.array([[np.cos(pitch_angle),0,np.sin(pitch_angle)],[0,1,0],[-np.sin(pitch_angle),0,np.cos(pitch_angle)]])

    transform = np.dot(pitch_transform, roll_transform)

    roll_transform2 = np.array([[1,0,0],[0,np.cos(roll_angle2),-np.sin(roll_angle2)],[0,np.sin(roll_angle2),np.cos(roll_angle2)]])
    transform = np.dot(roll_transform2,transform)

    transform_test = transform_sp.Rotation.from_euler('xyz', [np.rad2deg(roll_angle),np.rad2deg(pitch_angle),0], degrees=True)
    print(transform)
    print(transform_test.as_matrix())

    print(np.dot(transform,np.array([0,1,0])))



    test = VortexFilament(1,[1,1,0],[0.,1,0])
    test.split([0.8,0,2],[1,3,0],[-90,90])
    test.children[1].bend([0.5,3,0],90)
    test.children[0].bend([2,3,0],-90)
    # test.children[0].bend([3,1,0],90)
    test.draw_vortex_family([0,4],[0,4],transform=transform)
    plt.grid()
    plt.axis('scaled')
    plt.gca().set_aspect('equal', 'box')
    plt.xlim([0,4])
    plt.ylim([0,4])
    plt.show()
    # test.end = [1,1,0]
    dictionario = test.to_dict()
    print(dictionario)
    test = VortexFilament.from_dict(dictionario)
    test.draw_vortex_family([0,4],[0,4])
    plt.show()
    
    
