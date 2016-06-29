import maya.cmds as cmds

def myfn(arg, arg2):
    print arg + arg2

def recursive(function, obj, *args):
    children = cmds.listRelatives(obj)
    if children is not None:
        function(obj, *args)
        for child in children:
            child = obj + '|' + child
            recursive(function, child, *args)
            
sl = cmds.ls(sl=1)[0]
recursive(myfn, sl, " Hello Mr.Recursive!")