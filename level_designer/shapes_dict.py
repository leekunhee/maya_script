"""
Shapes Dictionary

penguinnom@gmail.com
"""

import maya.api.OpenMaya as om
import maya.cmds as cmds

def dag_path(name):
    selectionList = om.MSelectionList()
    try:
        selectionList.add(name)
    except:
        return None

    return selectionList.getDagPath(0)


def shapes_dict(shape_list):
    
    shape_dagpath_list = [dag_path(shape) for shape in shape_list]
    
    #lamdba expressions
    name = lambda MDagPath: MDagPath.partialPathName()
    node = lambda MObject: om.MFnDagNode(MObject)
    full_path = lambda MFnDagNode: MFnDagNode.getPath().fullPathName()
    parent_node = lambda MObject, p_id: node(node(MObject).parent(p_id))
    parent_count = lambda MFnDagNode: xrange(MFnDagNode.parentCount())

    return {name(shape): 
                [full_path(parent_node(shape,id)) for id in parent_count(node(shape))]
            for shape in shape_dagpath_list}


#EXAMPLE INPUT
shape_list = cmds.ls(g=1)
sh_dagpath_list = [dag_path(shape) for shape in shape_list]


#EXAMPLE USAGE
print shapes_dict(sh_dagpath_list)

#EXAMPLE OUTPUT
"""
{
    "pPyramidShape1": [
        "|group1|pPyramid1"
    ], 
    "pTorus1|pTorusShape1": [
        "|group1|pTorus1", 
        "|group1|pTorus2"
    ]
}
"""

