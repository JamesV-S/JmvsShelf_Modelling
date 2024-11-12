
import maya.cmds as cmds
import importlib

import JmvsM_DBTH
import JmvsM_crvTOgeo_clusterHandle_pos_to_locator as Clus_Loc

importlib.reload(JmvsM_DBTH)
importlib.reload(Clus_Loc)

def crvTogeo_cr_cylinder( name, size):
        cylinder = cmds.polyCylinder(n=name, r=size, h=2, sx=8, sy=1, sz=1, 
                        ax=(0,1,0), rcp=0, cuv=3, ch=1)[0]
        cmds.select(cl=1)
        
        # mTrans the geo to the mid_locator!
        cmds.matchTransform(cylinder, "loc_crvGeo_mid")

        # Delete edges to create quads:    
        top_edge_List = ["32", "34", "36", "38"]
        bottom_edge_list = ["24", "26", "28", "30"]
        
        for edge in top_edge_List:
            cmds.select(f"{cylinder}.e[{edge}]", tgl=1)
        cmds.delete()

        for edge in bottom_edge_list:
            cmds.select(f"{cylinder}.e[{edge}]", tgl=1)
        cmds.delete()
        
        # Select the face & add a cluster
        cmds.select(f"{cylinder}.f[12:15]", r=1)
        top_cluster = cmds.cluster()[0]
        if not top_cluster:
            cmds.error("Failed to create top cluster.")
        cmds.select(cl=1)

        # Create the cluster 
        cmds.select(f"{cylinder}.f[8:11]", r=1)
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
        JmvsM_DBTH.delete_by_type_history(cylinder)
        cmds.delete("loc_crvGeo_1", "loc_crvGeo_2", "loc_crvGeo_mid") 