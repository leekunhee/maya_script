"""
using Pyside QFileDialog

https://srinikom.github.io/pyside-docs/PySide/QtGui/QFileDialog.html
"""
from PySide import QtCore, QtGui
from shiboken import wrapInstance

fileDialog = QtGui.QFileDialog()

dir = fileDialog.getExistingDirectory()


