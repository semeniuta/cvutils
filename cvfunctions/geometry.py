# -*- coding: utf-8 -*-

def get_line_equation(x, y):
    slope = (y[1] - y[0]) / (x[1] - x[0])
    intercept = y[0] - slope * x[0]
    return (slope, intercept)