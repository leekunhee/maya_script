import maya.cmds as cmds

def getAttr(obj, attr): 
    return cmds.getAttr(obj + '.' + attr)

def movePivot(object, x, y, z):
    set_as = {'rpx' : x,'spx' : x,'rpy' : y,'spy' : y,'rpz' : z,'spz' : z}
    for attr in set_as : cmds.setAttr(object + '.' + attr, set_as[attr])
    
def alignObject(selection):
    
    cmds.select(selection)
    tx = getAttr(selection, 'tx')
    ty = getAttr(selection, 'ty')
    tz = getAttr(selection, 'tz')
    
    if tx is not 0.0 or ty is not 0.0 or tz is not 0.0 :
        cmds.makeIdentity(selection, apply=1, t=1,s=1,r=1)
    
    x = getAttr(selection, 'bcx')
    y = getAttr(selection, 'bcy')
    z = getAttr(selection, 'bcz')

    y_min = getAttr(selection, 'bbny')

    movePivot(selection, x, y, z)
    
    cmds.move(-x, -y_min, -z, ls=1)
   
    set_as = {'rpy' : y_min, 'spy' : y_min}
    for attr in set_as : cmds.setAttr(selection + '.' + attr, set_as[attr])
    cmds.makeIdentity(selection, apply=1, t=1,s=1,r=1)
    cmds.move(x, y_min, z, ls=1)
    

def makeBoundingBox(group):
    box = group + '_boundingbox'

    cmds.polyCube(n = box)
    cmds.setAttr(box + '.overrideEnabled', 1)
    cmds.setAttr(box + '.overrideLevelOfDetail', 1)
    cmds.connectAttr(group+'.bcx', box+'.tx')
    cmds.connectAttr(group+'.bcy', box+'.ty')
    cmds.connectAttr(group+'.bcz', box+'.tz')

    shape =  cmds.listRelatives(box)[0]
    polyCube = cmds.listConnections(shape, t='polyCube')[0]

    cmds.connectAttr(group+'.bbsx', polyCube + '.width')
    cmds.connectAttr(group+'.bbxy', polyCube + '.height')
    cmds.connectAttr(group+'.bbsz', polyCube + '.depth')

def recursive(function, obj, *args):
    children = cmds.listRelatives(obj)
    if children is not None:
        function(obj)
        for child in children:
            child = obj + '|' + child
            recursive(function, child)

            
selection = cmds.ls(sl=1)
for group in selection:
    makeBoundingBox(group)
    recursive(alignObject, group)


 


 