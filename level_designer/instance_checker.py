"""
SIMPLE INSTANCE CHECKER

penguinnom@gmail.com
"""

import maya.cmds as cmds

def get_instance_dict():
    """
    [SHAPES] HAS MANY [TRANSFORM NODE NAME]
    
    EX : {u'pCube1|pCube1Shape': [u'pCube1', u'pCube1_instance'], 
            u'pCube2Shape': [u'pCube2']}
    """
    g_list = cmds.ls(g=1)
    shapes = {}

    for item in g_list:
        shapes[item] = [] # make list for the shape.

    tr_list = cmds.ls(tr=1, v=1)

    for item in tr_list:
        i = cmds.ls(item, dag=1)
        shapes[i[1]].append(i[0]) # make list for the shape.

    return shapes


dict = get_instance_dict()
print dict