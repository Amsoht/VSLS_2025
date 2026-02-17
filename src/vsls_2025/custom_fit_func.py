import numpy as np
from math import pi

def higher(x, a, b, c, e, f, g, h):
    """fit function from IAU_baseline filter, shift input by 2023"""
    x = np.array(x) - 2023
    return a+b*x + c*x**2\
                + e*np.cos(2*pi*x)+f*np.sin(2*pi*x) \
                + g*np.cos(4*pi*x)+h*np.sin(4*pi*x)