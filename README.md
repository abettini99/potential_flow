<<<<<<< Updated upstream
# AE2130-I - Potential Flow Tool 
=======
<<<<<<< Updated upstream
# Potential Flow Tool (AE2130-I Aerodynamics)
 Potential Flow, method of superposition
=======
# AE2130-I - Potential Flow Tool
>>>>>>> Stashed changes
>>>>>>> Stashed changes

This tool is meant to help visualize potential flow theory using an intuitive interface. It was developed for the introductory aerodynamics course AE2130-I at Delft University of Technology.


<<<<<<< Updated upstream
## How to use
You can launch a web instance of the application through [this link](https://abettini99-potential-flow-tool.streamlit.app/). If the application hasn't been used in a while, the booting proces might take several minutes.

The functionality is very straigtforward:
* Use the `Clear Grid` and `Update Grid` buttons to remove or update all flow elements
* Use the `Grid` tab to change the domain and mesh to compute the field
* Use the `Layout` tab to adjust the looks of the output 
* Add individual flow elements in the `Add Flow Element` tab
* Add Pre-defined combinations of elements in the `Add Preset` tab
=======
<<<<<<< Updated upstream
 ```bash
 pip3 install -r requirements.txt
 ```

 Note that if you are utilizing old versions of Numpy, modules like Scipy and Numba need to be updated.
=======
## How to use
You can launch a web instance of the application through [this link](https://ae2130i-potential-flow-tool.streamlit.app/). If the application hasn't been used in a while, the booting process might take several minutes.

The functionality is very straightforward:
* Use the `Clear Grid` and `Update Grid` buttons to remove or update all flow elements
* Use the `Grid` tab to change the domain and mesh to compute the field
* Use the `Layout` tab to adjust the looks of the output
* Add individual flow elements in the `Add Flow Element` tab
* Add Pre-defined combinations of elements in the `Add Preset` tab
>>>>>>> Stashed changes
>>>>>>> Stashed changes

* Below the plots, a dropdown menu will allow you to adjust previously added flow elements.

---
## From source code
If you prefer to start the application from source or interact with the code yourself, feel free to clone [this Github Repository](https://github.com/abettini99/potential_flow_tool).  

```bash
git clone https://github.com/abettini99/potential_flow_tool.git
```




#### Dependencies
Install the required dependencies using

<<<<<<< Updated upstream
```bash
pip3 install -r requirements.txt
```
The application relies on an adapted version of the python package [PotentialFlowVisualiser](https://pypi.org/project/PotentialFlowVisualizer/) for most of the backend and uses [Streamlit](https://streamlit.io/) for building the app itself.

#### Execution

To run the code, execute the following command on terminal/prompt:

```bash
python3 -m streamlit run main.py
```

or execute the following command if you are utilizing anaconda:

```bash
streamlit run main.py
```

This will output a localhost window on your browser.


---

## Contribute

If you wish to contribute and help make this app better and more useful, don't hesitate to do so.
=======
<<<<<<< Updated upstream
You can use the following URL to get a web instance of application:
>>>>>>> Stashed changes


<<<<<<< Updated upstream
=======
If it takes time to load, it is likely that the application is being booted up after a long time, so give it some time (e.g. 1-2 minutes)
=======
```bash
pip3 install -r requirements.txt
```
The application relies on an adapted version of the python package [PotentialFlowVisualiser](https://pypi.org/project/PotentialFlowVisualizer/) for most of the backend and uses [Streamlit](https://streamlit.io/) for building the app itself.

#### Execution

To run the code, execute the following command on terminal/prompt:

```bash
python3 -m streamlit run main.py
```

or execute the following command if you are utilizing anaconda:

```bash
streamlit run main.py
```

This will output a localhost window on your browser.


---

## Contribute

If you wish to contribute and help make this app better and more useful, don't hesitate to do so.
>>>>>>> Stashed changes
>>>>>>> Stashed changes
