# -*- coding: utf-8 -*-

class Camera:
    def __init__(self, intrinsics=None):
        if intrinsics == None:
            self.camera_matrix = None
            self.dist_coefs = None
        else:
            self.set_intrinsics(intrinsics)
    
    def set_intrinsics(self, intrinsics):
        self.camera_matrix, self.dist_coefs = intrinsics
        
    @property
    def intrinsics(self):
        return (self.camera_matrix, self.dist_coefs)