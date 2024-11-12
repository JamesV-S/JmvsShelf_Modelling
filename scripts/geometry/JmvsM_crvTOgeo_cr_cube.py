
import maya.cmds as cmds 
import importlib

import JmvsM_DBTH
import JmvsM_crvTOgeo_clusterHandle_pos_to_locator as Clus_Loc

importlib.reload(JmvsM_DBTH)
importlib.reload(Clus_Loc)

def crvTogeo_cr_cube( name, size, bevel, fracVal=0.2, segVal=2):
        
        cube = cmds.polyCube(n=name ,w=1 ,h=1, d=1, sx=1, sy=1, sz=1, ax=(0,1,0), 
                      cuv=4, ch=1)
        cubeName = cube[0]
        polyCube = cube[1]
        cube_size_list = ["width", "height", "depth"]
        for x in range(3):
            cmds.setAttr(f"{polyCube}.{cube_size_list[x]}", size)
        cmds.select(cl=1)
        # option to bevel and not bevel
        if bevel:
            print("selection for bevel:> ", cubeName)
            cmds.polyBevel3(cubeName, fraction=fracVal, oaf=1, af=1, depth=1, 
                            mitering=0, miterAlong=0, chamfer=1, segments=segVal, 
                            worldSpace=1, smoothingAngle=30, subdivideNgons=1, 
                            mergeVertices=1, mergeVertexTolerance=0.0001, 
                            miteringAngle=180, angleTolerance=180, ch=1)               
        else:
            print(f"{name} has no bevel")
        cmds.select(cl=1)

        # mTrans the geo to the mid_locator!
        cmds.matchTransform(cubeName, "loc_crvGeo_mid") 
        
        # Select the face & add a cluster
        if bevel:
            cmds.select(f"{cubeName}.f[10:15]", r=1)
            cmds.select(f"{cubeName}.f[18:19]", tgl=1)
            cmds.select(f"{cubeName}.f[25]", tgl=1)
            cmds.select(f"{cubeName}.f[36:47]", tgl=1)
        else:
            cmds.select(f"{cubeName}.f[1]", r=1)
        top_cluster = cmds.cluster()[0]
        if not top_cluster:
            cmds.error("Failed to create top cluster.")
        cmds.select(cl=1)

        # Create the cluster
        if bevel: 
            cmds.select(f"{cubeName}.f[0:3]", r=1)
            cmds.select(f"{cubeName}.f[6:7]", tgl=1)
            cmds.select(f"{cubeName}.f[22:23]", tgl=1)
            cmds.select(f"{cubeName}.f[27]", tgl=1)
            cmds.select(f"{cubeName}.f[30:35]", tgl=1)
            cmds.select(f"{cubeName}.f[48:53]", tgl=1)
        else:
            cmds.select(f"{cubeName}.f[3]", r=1)
        bottom_cluster = cmds.cluster()[0]
        if not bottom_cluster:
            cmds.error("Failed to create bottom cluster.")
        cmds.select(cl=1)
        
        # Move clusters to locators
        top_cluster_handle = cmds.listConnections(top_cluster, type='transform')
        if not top_cluster_handle:
            cmds.error("Failed to get top cluster handle.")
        top_cluster_handle = top_cluster_handle[0]
        Clus_Loc.move_cluster_to_locator(top_cluster_handle, "loc_crvGeo_1")
       
        # Move clusters to locators
        bottom_cluster_handle = cmds.listConnections(bottom_cluster, type='transform')
        if not bottom_cluster_handle:
            cmds.error("Failed to get bottom cluster handle.")
        bottom_cluster_handle = bottom_cluster_handle[0]
        Clus_Loc.move_cluster_to_locator(bottom_cluster_handle, "loc_crvGeo_2")

        # Delete the clusters and locators!
        JmvsM_DBTH.delete_by_type_history(cubeName)
        cmds.delete("loc_crvGeo_1", "loc_crvGeo_2", "loc_crvGeo_mid") 