# -*- coding: utf-8 -*-

def write_matrix(matrix, sheet, row_index, col_index, title):
    rows, cols = matrix.shape 
    sheet.write(row_index, col_index, title) 
    for i in range(rows):
        for j in range(cols):
            sheet.write(row_index+1+i, col_index+j, matrix[i, j])
            
def write_vector_vertical(vector, sheet, row_index, col_index, title):
    sheet.write(row_index, col_index, title)    
    for i in range(len(vector)):
        sheet.write(row_index+1+i, col_index, vector[i])
        
def write_vector_horizontal(vector, sheet, row_index, col_index, title):
    sheet.write(row_index, col_index, title)      
    for i in range(len(vector)):
        sheet.write(row_index+1, col_index+i, vector[i])