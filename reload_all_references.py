import maya.cmds as cmds
#reload all references
ref = cmds.ls(rf=1)

for item in ref:
    cmds.file(ur = item)
    f = cmds.referenceQuery(item, f=1)
    cmds.file(f, lrd = "asPrefs", lr = item) 


#create reference

filename = "/home/dexter/Desktop/allen_5000_camel_leather_3P.fbx"
cmds.file(filename, r=1) 