"""
SIMPLE INSTANCE CHECKER

penguinnom@gmail.com
"""

"""
[SHAPES] HAS MANY [TRANSFORM NODE NAME]
version 2 solved the problem caused by group

EX : {u'pCube1|pCube1Shape': [u'|group1|pCube1', u'|group1|pCube1_instance'], 
u'pCube1_duplicatedShape': [u'|group1|pCube1_duplicated']}

The dictionary has [shape DAG node] hashed to the list that has transform DAG paths
        
"""
import maya.api.OpenMaya as om
import maya.cmds as cmds

def getDag(name):
    selectionList = om.MSelectionList()
    try:
        selectionList.add(name)
    except:
        return None
        
    dagPath = selectionList.getDagPath(0)
    dependNode = selectionList.getDependNode(0)
    return dagPath

def get_instance_dict():
    
    shape_list = cmds.ls(g=1)
    shapes = {}
    shape_dagPath_list = []

    for shape in shape_list:
        shape_dagPath_list.append(getDag(shape))

    for path in shape_dagPath_list:
        item = path.partialPathName()
        shapes[item] = []
        dag_node = om.MFnDagNode(path)
        for i in xrange(dag_node.parentCount()):
            #MFnDagNode.parent() returns MObject not MFnDagNode
            parent_node = om.MFnDagNode(dag_node.parent(i))
            path_name = parent_node.getPath().fullPathName()
            shapes[item].append(path_name)
        
    return shapes


#example
dict = get_instance_dict()
print dict


"""
old junk....
"""
# import maya.cmds as cmds

# def get_instance_dict():
#     """
#     [SHAPES] HAS MANY [TRANSFORM NODE NAME]
    
#     EX : {u'pCube1|pCube1Shape': [u'pCube1', u'pCube1_instance'], 
#             u'pCube2Shape': [u'pCube2']}
#     """
#     g_list = cmds.ls(g=1)
#     shapes = {}

#     for item in g_list:
#         shapes[item] = [] # make list for the shape.

#     tr_list = cmds.ls(tr=1, v=1)

#     for item in tr_list:
#         i = cmds.ls(item, dag=1)
#         shapes[i[1]].append(i[0]) # make list for the shape.

#     return shapes


