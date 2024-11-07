
import maya.cmds as cmds

def delete_by_type_history(arg):
    selection = arg
   
    if not selection:
        cmds.warning("no objects selected")
        return
    
    #for obj in selection:
    print(selection)
    history_nodes = cmds.listHistory(selection)
        
    # Filter out shape nodes from the history list
    '''
    if history_nodes:
        print(f"{obj} has shistory {history_nodes}")
    else:
        print(f"{obj} has no history")
    '''
    
    non_shape_history_nodes = [node for node in history_nodes if cmds.nodeType(node) not in ('mesh', 'nurbsCurve', 'nurbsSurface', 'subdiv', 'lattice')]
    
    if non_shape_history_nodes:
        print(f"{selection} Had history {history_nodes}")
        try:
            cmds.delete(selection, ch=1)
        except Exception as e:
            print(f"Had an issue trying to delete the hisoty on {selection}: {e}")
    else:
        print(f"{selection} Has no history to delete")
        
# delete_by_type_history(cmds.ls(sl=1))