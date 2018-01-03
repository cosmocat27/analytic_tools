# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 22:15:43 2018

@author: cosmo
"""

import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string


# Search a worksheet ws for a cell with value s, return coordinate tuple

def search_xl(ws, s, row_start=1, col_start=1, col_end=0, inst_number=1):
    count = 1
    if col_end == 0:
        col_end = ws.max_column
    
    for row in ws.rows:
        if row[0].row < row_start:
            continue
        for cell in row:
            if column_index_from_string(cell.column) < col_start:
                continue
            if column_index_from_string(cell.column) > col_end:
                break
            if cell.value == s:
                if count < inst_number:
                    count = count + 1
                    continue
                return (cell.row, column_index_from_string(cell.column))
    raise EOFError("Not found")
    