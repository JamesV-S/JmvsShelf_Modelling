
import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from shiboken6 import wrapInstance
import os.path

import sys
import importlib
from Jmvs_letter_driver_script import find_driver_letter_modelling
importlib.reload(find_driver_letter_modelling)

A_driver = find_driver_letter_modelling.get_folder_letter("Jmvs_current_file_path_modelling")
custom_path = f'{A_driver}JmvsShelfTools_Modelling' 
another_path = f'{A_driver}JmvsShelfTools_Modelling\\JmvsM_modules' 
print(f"module imported from {custom_path}")
sys.path.append(custom_path)
sys.path.append(another_path)

import JmvsM_crvTOgeo_locator_guides as loc_guides
import JmvsM_crvTOgeo_cr_cylinder as crv_cylinder
import JmvsM_crvTOgeo_cr_cube as crv_cube

importlib.reload(loc_guides)
importlib.reload(crv_cylinder)
importlib.reload(crv_cube)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

class QtSampler(QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSampler,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.initUI()
        # Add this variable to track the state of the Undo button
        self.undo_clicked = False
        
        # By default set the cylinder to be created 
        self.isCylinder = True
        self.ui.cylinder_radio_btn.clicked.connect(self.cylinder_radio_button)
        self.ui.cube_radio_btn.clicked.connect(self.cube_radio_button)
        self.ui.size_spnbx.valueChanged.connect(self.geo_size)
        self.ui.bevel_checkBx.stateChanged.connect(self.bevel)
        self.ui.apply_btn.clicked.connect(self.apply_func)
        self.ui.undo_btn_1.clicked.connect(self.undo_func)

        # Set default values
        self.ui.size_spnbx.setValue(5)
        self.ui.cylinder_radio_btn.setChecked(True)
        self.ui.cube_radio_btn.setChecked(False)
        self.ui.bevel_checkBx.setEnabled(False)
        self.ui.bevel_checkBx.setChecked(True)
        

    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_FILE = f'{A_driver}JmvsShelfTools_Modelling\\JmvsM_ui_scripts\\jmvsM_linear_crv_to_geo.ui' 
        file = QFile(UI_FILE)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)
        file.close()
    
    
    # Function for before checkbox   
    def cylinder_radio_button(self):
                      
        geo_type = self.ui.cylinder_radio_btn.isChecked()
        
        if geo_type == True:
            print("create cylinder")
            self.isCylinder = 1
            # disable the cube button:
            self.ui.cylinder_radio_btn.setEnabled(True)
            self.ui.bevel_checkBx.setEnabled(False)
            
        else:
            print("hide cube button")
            self.isCylinder = 0
            # disable the cylinder button:
            self.ui.cube_radio_btn.setEnabled(False)
            
        return self.isCylinder
    

    def cube_radio_button(self):
                      
        geo_type = self.ui.cube_radio_btn.isChecked()
        
        if geo_type == True:
            print("create cube")
            self.isCylinder = 0
            # disable the cube button:
            self.ui.cube_radio_btn.setEnabled(True)
            self.ui.bevel_checkBx.setEnabled(True)
        else:
            print("hide cylinder button")
            self.isCylinder = 1
            # disable the cylinder button:
            self.ui.cylinder_radio_btn.setEnabled(False)
            
        return self.isCylinder
    

    def geo_size(self):
        try:
            self.ctrl_size = self.ui.size_spnbx.value()
            self.ctrl_size = float(self.ctrl_size)
            print(f"scale: {self.ctrl_size}")
        except ValueError:
            print( 'no string values allowed' )
    

    def bevel(self):
        is_bevel = self.ui.bevel_checkBx.isChecked()
        if is_bevel:
            self.apply_bevel = 1
            print("apply bevel to cube")
        else:
            self.apply_bevel = 0
            print("DONT apply bevel to cube")


    def apply_func(self):
        print("apply buttoon pressed")
        
        loc_guides.space_locator_end_guides(cmds.ls(sl=1, type="transform"))
        if self.isCylinder:
            crv_cylinder.crvTogeo_cr_cylinder("geo_cylinder_", self.ctrl_size)
        else:
            crv_cube.crvTogeo_cr_cube("geo_cube_", self.ctrl_size, self.apply_bevel)
        
        # Re-enable the Undo button
        self.ui.undo_btn_1.setEnabled(True)
        self.undo_clicked = False


    def undo_func(self):
        applied = 56
        if self.undo_clicked:
            return
        # Disable the Undo button
        self.ui.undo_btn_1.setEnabled(False)
        
        self.undo_clicked = True
        print(f"undo this many times: _ {applied+1} _ ")
        
        for x in range(applied+1):
            cmds.undo()

def main():
    ui = QtSampler()
    ui.show()
    return ui
    
if __name__ == '__main__':
    main()