import maya.cmds as cmds

sel = cmds.ls(sl=1)
min = len(sel[0])
index = -1

for i in sel:
    if len(i) < min : min = len(i)

for i in xrange(min):
    tmp = [j[i] for j in sel]
    if tmp[0] is not tmp[1]:
        index = i
        break;

grp = sel[0][:index] + "GRP"
        
cmds.group(sel, n = grp)