"""
using Pyside QFileDialog

https://srinikom.github.io/pyside-docs/PySide/QtGui/QFileDialog.html
"""
from PySide import QtCore, QtGui
from shiboken import wrapInstance

def open_dir():
    return QtGui.QFileDialog().getExistingDirectory()

def main_func(folder):
    if folder : 
        #do something
        print folder 

main_func(open_dir())

