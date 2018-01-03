# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 21:42:41 2018

@author: cosmo
"""

import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl.utils import get_column_letter, column_index_from_string


class Plot_tree:
    def __init__(self, axis=[], values=[], name=None):
        self.axis = axis
        self.values = values
        self.name = name
        self.children = {}
        self.parent = None
    
    def get_name(self):
        return self.name
    
    def rename(self, new_name):
        self.name = new_name

    def plot_self(self):
        plt.plot(self.axis, self.values)
        if self.name:
            plt.title(self.name + " (aggregate)")
        plt.show()
    
    def plot_children(self):
        for child in self.children:
            plt.plot(self.children[child].axis, self.children[child].values)
            plt.legend([self.children[child].name])
        if self.name:
            plt.title(self.name)
        plt.show()
    
    def get_parent(self):
        return self.parent
    
    def add_to_parent(self, parent):
        parent.add_child(self.name, self)
    
    def get_children(self):
        return self.children
    
    def add_child(self, new_child_label, new_child_tree):
        if new_child_label in self.children:
            print("child already exists")
            return
        self.children[new_child_label] = new_child_tree
        new_child_tree.parent = self
    
    def remove_child(self, child_label):
        if not child_label in self.children:
            print("child doesn't exist")
            return
        del self.children[child_label]


if __name__ == '__main__':
    axis_test = [-2, -1, -0, 1, 2]
    values_test = [10, 20, 30, 40, 50]
    
    test_plot_tree = Plot_tree(axis_test, values_test, "Base Tree")
    #test_plot_tree.plot_self()
    
    test_branch1 = Plot_tree(axis_test, [x/3 for x in values_test], "branch1")
    test_branch2 = Plot_tree(axis_test, [2*x/3 for x in values_test], "branch2")
    
    test_plot_tree.add_child(test_branch1.get_name(), test_branch1)
    test_plot_tree.add_child(test_branch2.get_name(), test_branch2)
    
    print(test_plot_tree.get_children())
