import maya.cmds as cmds

iff = cmds.render('persp', x=360,  y=240, rep=1 )
cmds.convertIffToPsd(ifn = iff, pfn='/media/backup/crew/KH/Simon/FBX/test.psd', xr= 360, yr = 240)
