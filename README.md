# AE2130-I - Potential Flow Tool

This tool is meant to help visualize potential flow theory using an intuitive interface. It was developed for the introductory aerodynamics course AE2130-I at Delft University of Technology.


## How to use
You can launch a web instance of the application through [this link](https://ae2130i-potential-flow-tool.streamlit.app/). If the application hasn't been used in a while, the booting process might take several minutes.

The functionality is very straigtforward:
* Use the `Clear Grid` and `Update Grid` buttons to remove or update all flow elements
* Use the `Grid` tab to change the domain and mesh to compute the field
* Use the `Layout` tab to adjust the looks of the output
* Add individual flow elements in the `Add Flow Element` tab
* Add Pre-defined combinations of elements in the `Add Preset` tab

* Below the plots, a dropdown menu will allow you to adjust previously added flow elements.

---
## From source code
If you prefer to start the application from source or interact with the code yourself, feel free to clone [this Github Repository](https://github.com/abettini99/potential_flow_tool).  

```bash
git clone https://github.com/abettini99/potential_flow_tool.git
```




#### Dependencies
Install the required dependencies using

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
