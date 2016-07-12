from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.cmds as cmds
import maya.mel as mel
import json, os, sys
import PIL.Image as Image

def save_to():
    return QtGui.QFileDialog().getSaveFileName()
    
path = os.path.splitext(save_to()[0])
if path[1] is not ".fbx":
    print "fuck you!"