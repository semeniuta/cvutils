# -*- coding: utf-8 -*-

from xlsxwriter.workbook import Workbook
import cPickle as pickle
from generalfunctions import excel

class StereoVisionSystem:
    def __init__(self):
        ''' Calibration parameters '''        
        self.R = None
        self.T = None
        self.E = None
        self.F = None
        ''' Rectification transofrms '''        
        self.R1 = None
        self.R2 = None
        self.P1 = None
        self.P2 = None
        self.Q = None
        
    @property
    def calib_params(self):
        return (self.R, self.T, self.E, self.F)
    
    @property
    def rotation_matrices(self):
        return (self.R1, self.R2)
        
    @property
    def projection_matrices(self):
        return (self.P1, self.P2)
        
    def set_calibration_parameters(self, stereocalibrate_res):
        self.R, self.T, self.E, self.F = stereocalibrate_res[5:]
        
    def set_rectification_transforms(self, stereorectify_res):
        self.R1, self.R2, self.P1, self.P2, self.Q = stereorectify_res[:-2]
        
    def pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)
            
    def unpickle(self, filename):
        with open(filename, 'rb') as f:
            unpickled_dict = pickle.load(f)
            self.__dict__ = unpickled_dict
            
    def save_to_excel_file(self, filename):
        wb = Workbook(filename)
        sheet = wb.add_worksheet()
        bold = wb.add_format({'bold': 1})
        
        sheet.write(1, 1, 'Calibration parameters', bold) 
        excel.write_matrix(self.R, sheet, 3, 1, 'Rotation matrix')                
        excel.write_vector_vertical(self.T, sheet, 3, 5, 'Translation vector')        
        excel.write_matrix(self.E, sheet, 8, 1, 'Essential matrix')
        excel.write_matrix(self.F, sheet, 14, 1, 'Fundamental matrix')
        
        sheet.write(1, 8, 'Rectification transforms', bold)  
        excel.write_matrix(self.R1, sheet, 3, 8, 'R1')
        excel.write_matrix(self.R2, sheet, 3, 13, 'R2')
        excel.write_matrix(self.P1, sheet, 8, 8, 'P1')
        excel.write_matrix(self.P2, sheet, 8, 13, 'P2')
        excel.write_matrix(self.Q, sheet, 15, 8, 'Q')
            
        wb.close()
        
    def __srr__(self):
        pass