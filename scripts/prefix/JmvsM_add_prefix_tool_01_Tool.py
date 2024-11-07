
import maya.cmds as cmds 

def front_layout_prefix(before, hi, prefix):
    side = before
    hierarchy = hi
    fst_selection = cmds.ls(sl=1)
    
    if hierarchy:
        cmds.select(fst_selection, hi=1)
    else:
        pass
    
    full_list = cmds.ls(sl=1, type='transform')
    undo_num = len(full_list)
    
    if side == 1:
        [cmds.rename(full_list[i], prefix + '_' + 
                    full_list[i]) for i in 
                    range(len(full_list)
                    )
        ]
    else:
        new_name_list = [cmds.rename(full_list[i], 
                        full_list[i] + '_' + prefix) 
                        for i in range(len(full_list))
                        ]
    return undo_num
    #print(new_name_list)
#front_layout_prefix(1, 0, "Elbow")

