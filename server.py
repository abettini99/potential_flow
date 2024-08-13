#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors:       A. Bettini
Last Modified: 2024-08-12

Server launcher for the Incompressible flow visualizer.
Utilizes dash for user interface, whereas plotly is used for plotting.
For webpage launching: waitress and webbrowser 

This file is a copy-paste from https://github.com/DouwMarx/dash_by_exe

Second version of the code.
"""
## Import libraries
from waitress import serve
import webbrowser            # For launching web pages
from threading import Timer  # For waiting before launching web page
from src.app import server

def open_browser():
    """
    Open browser to localhost
    """
    
    webbrowser.open_new('http://127.0.0.1:8080/')

## ==== ##
## MAIN ##
## ==== ##
Timer(1, open_browser).start()  # Wait a second and then start the web page
serve(server)
