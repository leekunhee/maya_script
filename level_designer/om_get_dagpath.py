import maya.api.OpenMaya as om

def getDag(name):
    selectionList = om.MSelectionList()
    try:
        selectionList.add(name)
    except:
        return None
        
    dagPath = selectionList.getDagPath(0)
    dependNode = selectionList.getDependNode(0)
    return dagPath