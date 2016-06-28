import maya.cmds as cmds

group = cmds.ls(sl=1)[0]
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
cmds.connectAttr(group+'.bbxy', polyCube + 'height')
cmds.connectAttr(group+'.bbsz', polyCube + 'depth')