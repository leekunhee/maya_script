import os, sys
import PIL.Image as Image
import maya.cmds as cmds

texlist = cmds.ls(tex=1)

size = 1024, 1024

for tex in texlist: 
    infile = cmds.getAttr(tex + '.fileTextureName')
    outfile = os.path.splitext(infile)[0] + ".thumbnail"

    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, "JPEG")
        except IOError:
            print "cannot create thumbnail for '%s'" % infile
    cmds.setAttr(tex + '.fileTextureName', outfile, type='string')
