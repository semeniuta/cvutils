# -*- coding: utf-8 -*-

from xlsxwriter.workbook import Workbook
import cPickle as pickle

class Camera:
    def __init__(self, intrinsics=None):
        if intrinsics == None:
            self.camera_matrix = None
            self.dist_coefs = None
        else:
            self.set_intrinsics(intrinsics)
        
    @property
    def intrinsics(self):
        return (self.camera_matrix, self.dist_coefs)
        
    def set_intrinsics(self, intrinsics):
        self.camera_matrix, self.dist_coefs = intrinsics
        
    def pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.intrinsics, f) 
    
    def unpickle(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        self.set_intrinsics(data)   
    
    def save_to_excel_file(self, filename):
        wb = Workbook(filename)
        sheet = wb.add_worksheet()
        bold = wb.add_format({'bold': 1})
        sheet.write('B2', 'Camera matrix', bold)
        
        rows, cols = self.camera_matrix.shape
        for i in range(rows):
            for j in range(cols):
                sheet.write(2+i, 1+j, self.camera_matrix[i, j])
                
        sheet.write('F2', 'Distortion coeffitients', bold)
        for i in range(len(self.dist_coefs)):
            sheet.write(2, 5+i, self.dist_coefs[i])
            
        wb.close()