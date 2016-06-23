"""
FBX EXPORTER

penguinnom@gmail.com
"""
import os
import maya.cmds as cmds
import maya.mel as mel

def exportFBX(shapes, outdir):
    if not os.path.exists(outdir + '/fbx/'):
        os.mkdir(outdir + '/fbx/')
    if type(shapes) is not list:
        shapes = [shapes]

    for shape in shapes:
        cmds.select(shape)
        filename = outdir + '/fbx/' + shape + '.fbx'
        mel.eval(('FBXExportInAscii -v true'))
        mel.eval(('FBXExport -f \"{}\" -s').format(filename))
 
#example       
ss = [u'pCube1|pCube1Shape', u'pCube1_duplicatedShape']
exportFBX(ss, dir)
"""
// Logfile: "/home/dexter/maya/FBX/Logs/2016.1.2/maya2016exp.log" //
// Logfile: "/home/dexter/maya/FBX/Logs/2016.1.2/maya2016exp.log" //
"""