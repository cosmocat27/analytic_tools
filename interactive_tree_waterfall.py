# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 21:42:41 2018

@author: cosmo
"""

import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string

from helper_functions import search_xl


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
    
    
    # read in the values from excel file
    wb_path = "Excel_tree_example.xlsx"
    wb = openpyxl.load_workbook(wb_path, data_only=True)
    ws = wb.get_sheet_by_name("Sheet1")
    
    c = search_xl(ws, "Hierarchy")
    hier = []
    cell = ws[get_column_letter(c[1])+str(c[0]+1)]
    hier.append(cell.value)
    cell = ws[cell.column+str(cell.row+1)]
    while not cell.value is None:
        if (cell.value > hier[-1] + 1) or cell.value < 1:
            print("invalid hierarchy!")
            break
        hier.append(cell.value)
        cell = ws[cell.column+str(cell.row+1)]
    print(hier)
    
    c = search_xl(ws, "Index")
    cols = []
    idx = []
    col_num = c[1] + 1
    cell = ws[get_column_letter(col_num)+str(c[0])]
    
    while not cell.value is None:
        cols.append(col_num)
        idx.append(cell.value)
        col_num = col_num + 1
        cell = ws[get_column_letter(col_num)+str(cell.row)]
    print(idx)
        
    df = pd.DataFrame(columns = idx)
    names = []
    cell = ws[get_column_letter(c[1])+str(c[0]+1)]
    
    while not cell.value is None:
        names.append(cell.value)
        
        new_row = []
        for col in cols:
            new_row.append(ws[get_column_letter(col)+str(cell.row)].value)
        df.loc[cell.value] = new_row
        
        cell = ws[cell.column+str(cell.row+1)]
    print(names)
    
    
    # construct the Plot_tree
    tree_ladder = []
    for i, lvl in enumerate(hier):
        new_name = names[i]
        new_row = df.loc[new_name]
        
        new_tree = Plot_tree(idx, new_row, new_name)
        
        while True:
            if lvl == 0:
                tree_ladder.append(new_tree)
                base_tree = new_tree
                break
            if lvl > len(tree_ladder)-1:
                new_tree.add_to_parent(tree_ladder[-1])
                tree_ladder.append(new_tree)
                break
            elif lvl == len(tree_ladder)-1:
                new_tree.add_to_parent(tree_ladder[lvl-1])
                tree_ladder[-1] = new_tree
                break
            else:
                tree_ladder.pop(-1)
    
    
    # plot base tree and children
    
    base_tree.plot_self()
    base_tree.plot_children()
