import maya.cmds as cmds
import importlib

import JmvsM_check_add_Utility_node as Add_Util
import JmvsM_connect_attr_if_not_connected as CA

importlib.reload(Add_Util)
importlib.reload(CA)

def space_locator_end_guides( curve_sel, loc1="loc_crvGeo_1", 
                            loc2="loc_crvGeo_2", loc3="loc_crvGeo_mid"):
        
        # curve_sel = cmds.ls(sl=1, type="transform")
        
        if not curve_sel:
            cmds.error("Please select a curve.")
            return

        try:
            # Define the CV positions
            cv0_position = cmds.pointPosition(f"{curve_sel[0]}.cv[0]", w=1)
            cv1_position = cmds.pointPosition(f"{curve_sel[0]}.cv[1]", w=1)

            # Match the transforms of first locator to the first CV[0] of the curve
            if not cmds.objExists(loc1):
                    # make the locator
                    cmds.spaceLocator(n=loc1)
            cmds.xform(loc1, worldSpace=1, translation=cv0_position)

            if not cmds.objExists(loc2):
                    # make the locator
                    cmds.spaceLocator(n=loc2)
            cmds.xform(loc2, worldSpace=1, translation=cv1_position)

            cmds.aimConstraint(loc2, loc1, aimVector=[0, -1, 0], upVector=[1, 0, 0], worldUpType="scene")
            cmds.matchTransform(loc2, loc1, rot=1, scl=0, pos=0)
            cmds.delete(f"{loc1}_aimConstraint*")
            

            # Create the middle locator! 
            if not cmds.objExists(loc3):
                    # make the locator
                    cmds.spaceLocator(n=loc3)
            mid_pos_pma = "PMA_midAverage_pos"
            Add_Util.cr_node_if_not_exists("plusMinusAverage", mid_pos_pma, {"operation":3})
            CA.connect_attr(f"{loc1}.translate", f"{mid_pos_pma}.input3D[0]")
            CA.connect_attr(f"{loc2}.translate", f"{mid_pos_pma}.input3D[1]")
            CA.connect_attr(f"{mid_pos_pma}.output3D", f"{loc3}.translate")
            cmds.matchTransform(loc3, loc2)
        
            return curve_sel
        
        except TypeError:
            print("Select a curve!")