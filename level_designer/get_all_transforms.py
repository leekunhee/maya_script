"""
GET TRANSFORM DICTIONARY

penguinnom@gmail.com
"""

import maya.cmds as cmds

def get_transforms_dict():
    """
    [TRANSFORM] HAS [PIVOT],[TRANSLATE]
    
    EX : {u'pCube1': {'pivot': (0.0, 1.0, 0.0), 'translate': (1.0, 2.0, 3.0)},  
          u'pCube2': {'pivot': (0.0, -1.0, 0.0), 'translate': (4.0, 5.0, 6.0)}}
    """
    transforms = {}
    tr_list = cmds.ls(tr=1, v=1)
    for item in tr_list:
        info = {}
        info['translate'] = cmds.getAttr(item +'.translate')[0]
        info['pivot'] = cmds.getAttr(item +'.scalePivot')[0]
        
        """
        ADDING MORE ATTRIBUTES
        #info['attr'] = cmds.getAttr(item + '.attr')
        """
        transforms[item] = info
        
    return transforms
