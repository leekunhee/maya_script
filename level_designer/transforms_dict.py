"""
GET TRANSFORM DICTIONARY

penguinnom@gmail.com
"""

import maya.cmds as cmds

def transforms_dict(tr_list, attr_list):
    
    #TO-DO : input inspector

    get_attr = lambda tr,attr : cmds.getAttr(tr + '.' + attr)[0]
    
    return {tr: {attr: get_attr(tr, attr) for attr in attr_list}
        for tr in tr_list}


#EXAMPLE INPUT
attr_list = ['translate', 'scalePivot']
tr_list = cmds.ls(tr=1, v=1)

#EXAMPLE USAGE
print transforms_dict(tr_list, attr_list)

#EXAMPLE OUTPUT
"""
{
    "pPyramid1": {
        "scalePivot": [
            0.0, 
            0.0, 
            0.0
        ], 
        "translate": [
            0.0, 
            0.0, 
            0.0
        ]
    }, 
    "pTorus1": {
        "scalePivot": [
            0.0, 
            0.0, 
            0.0
        ], 
        "translate": [
            0.0, 
            0.0, 
            0.0
        ]
    }
}
"""
    