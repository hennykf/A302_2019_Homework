import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from ipywidgets import interact, fixed


def load_and_prepare_cmd(filename):
    """format the data for making a cmd. output is a list of g, and a list of g-r"""
    col_names = ['g', 'r']
    file = pd.read_csv(filename, sep=',', usecols=col_names)
    file['g_r'] = file.g - file.r
    # subset the data according to conditionals
    grop = file[file.g_r < 2.5]
    grop = grop[grop.g_r > -0.5]
    grop = grop[grop.g > 14]
    grop = grop[grop.g < 24]
    grop = grop[['g', 'g_r']]
    return grop.g, grop.g_r

def interactive_hess(g, g_r):
    """create an interactive Hess Diagram where the hexbins can vary from 50 to 300"""
    def plot(g, g_r, grid=100):
        plt.hexbin(g_r, g, bins='log', gridsize=grid)
        plt.gca().invert_yaxis()
    interact(plot, g=fixed(g), g_r=fixed(g_r), grid=(50, 300, 1))
