import maya.cmds as cmds

def create_locator_at_edge_center():
    selected_edges = cmds.ls(selection=True, flatten=True)
    if not selected_edges:
        cmds.error("Please select edge loops.")

    bbox = cmds.exactWorldBoundingBox(selected_edges)
    '''Returns: [minX, minY, minZ, maxX, maxY, maxZ].'''
    
    center = [(bbox[0] + bbox[3]) / 2, (bbox[1] + bbox[4]) / 2, (bbox[2] + bbox[5]) / 2]
    '''Calc centre of: ^x-axis^                ^y-axis^                   ^z-axis^   '''
    
    loc = cmds.spaceLocator(n="temp_edgePos_")[0]
    cmds.setAttr(f"{loc}.translate", center[0], center[1], center[2], type="double3")
    cmds.setAttr(f"{loc}.overrideEnabled", 1)
    cmds.setAttr(f"{loc}.overrideColor", 9)

# Run the function
# create_locator_at_edge_center()