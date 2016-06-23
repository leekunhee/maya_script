import json

json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
parsed_json = json.loads(json_string)
json_to_string = json.dumps(parsed_json)

print json_string
print parsed_json
print json_to_string


from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.cmds as cmds
import maya.mel as mel
import json

def export_json(dict, outputname):
    dir = QtGui.QFileDialog.getExistingDirectory()
    filename = dir + '/' + outputname + '.json'
    with open(filename, 'w') as outfile:
        json.dump(dict, outfile, indent=4, sort_keys=True)
        

#loading?
# with open('filename.txt', 'r') as handle:
#     parsed = json.load(handle)