"""
FBX EXPORTER

penguinnom@gmail.com
"""

from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.cmds as cmds
import maya.mel as mel

def exportFBX(shapes):
    if type(shapes) is not list:
        shapes = [shapes]
        
    dir = QtGui.QFileDialog.getExistingDirectory()
    
    for shape in shapes:
        cmds.select(shape)
        filename = dir + '/' + shape + '.fbx'
        mel.eval(('FBXExportInAscii -v true'))
        mel.eval(('FBXExport -f \"{}\" -s').format(filename))
 
#example       
ss = [u'pCube1|pCube1Shape', u'pCube1_duplicatedShape']
exportFBX(ss)
"""
// Logfile: "/home/dexter/maya/FBX/Logs/2016.1.2/maya2016exp.log" //
// Logfile: "/home/dexter/maya/FBX/Logs/2016.1.2/maya2016exp.log" //
"""