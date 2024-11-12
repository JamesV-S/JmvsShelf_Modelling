
import maya.cmds as cmds
import sys
import importlib
import find_driver_letter_modelling as driver
importlib.reload(driver)

A_driver = driver.get_folder_letter("Jmvs_current_file_path_modelling")
custom_path = f'{A_driver}JmvsShelfTools_Modelling' 
another_path = f'{A_driver}JmvsShelfTools_Modelling\\JmvsM_modules' 
print(f"module imported from {custom_path}")
sys.path.append(custom_path)
sys.path.append(another_path)

'''
import JmvsM_connect_attr_if_not_connected as CA
import JmvsM_check_add_Utility_node as Add_Util
import JmvsM_DBTH
import JmvsM_crvTOgeo_clusterHandle_pos_to_locator as Clus_Loc
'''
# --------------------------------------------------------------
# imports I actually need:
import JmvsM_crvTOgeo_locator_guides as loc_guides
import JmvsM_crvTOgeo_cr_cylinder as crv_cylinder
import JmvsM_crvTOgeo_cr_cube as crv_cube

importlib.reload(loc_guides)
importlib.reload(crv_cylinder)
importlib.reload(crv_cube)

# split up the functions even further so when the ui is setup it's easier to do!
# using arguments to determine what the functions do and allow the ui options 
# to provide those arguments!

class linear_curve_into_geometry():
    def __init__(self):
            
        isCylinder = 1
        loc_guides.space_locator_end_guides(cmds.ls(sl=1, type="transform"))
        
        if isCylinder:
            crv_cylinder.crvTogeo_cr_cylinder("geo_cylinder_", 5)
            
        else:
            crv_cube.crvTogeo_cr_cube("geo_cube_", 5, True)
            
linear_curve_into_geometry()