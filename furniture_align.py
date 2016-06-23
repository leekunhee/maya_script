import maya.OpenMayaUI as omui
import maya.cmds as cmds
from PySide import QtCore, QtGui
from shiboken import wrapInstance

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)


class Ui(QtGui.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(Ui, self).__init__(parent)
        
        self.setWindowTitle("  ")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setGeometry(400,300,400,200)
        
        self.create_layout()
        self.create_connections()
    
    def create_layout(self):
        ###########################################
        #TITLE
        title = QtGui.QLabel("FUNITURE ALIGNER")
        title.setStyleSheet("font-size: 30px; font-weight:600")
        
        #HELP
        help = QtGui.QLabel("""
HOW TO USE IT :
select 4 vertices and put the number of height as centimeter.
                            """)
        
        titleLayout = QtGui.QHBoxLayout()
        titleLayout.addWidget(title)
        
        helpLayout = QtGui.QHBoxLayout()
        helpLayout.addWidget(help)
        ############################################
        
        #BODY
        self.lbl_height = QtGui.QLabel("HEIGHT")
        self.float_height = QtGui.QDoubleSpinBox()
        self.float_height.setMaximum(5000.0)
        self.btn_apply = QtGui.QPushButton("APPLY")
        
        bodyLayout = QtGui.QHBoxLayout()
        bodyLayout.addWidget(self.lbl_height)
        bodyLayout.addWidget(self.float_height)
        
        

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(titleLayout)
        main_layout.addLayout(helpLayout)
        main_layout.addLayout(bodyLayout)
        main_layout.addWidget(self.btn_apply)
        
        self.setLayout(main_layout)
    
    def create_connections(self):
        self.btn_apply.clicked.connect(self.mainFunc)
        
  

    def align_plane(self, plane):
        cmds.select(plane)
        fn = cmds.polyInfo(fn=True)
        fn_x = float(fn[0].split(" ")[7])
        fn_y = float(fn[0].split(" ")[8])
        fn_z = float(fn[0].split(" ")[9])

        #create normal aim locator
        cmds.spaceLocator(n = 'locator_normal_aim')
        cmds.move(fn_x, fn_y, fn_z, 'locator_normal_aim')
        cmds.scale(0.1,0.1,0.1,'locator_normal_aim')

        #create locator center
        cmds.spaceLocator(n = 'locator_center')
        cmds.scale(0.1,0.1,0.1,'locator_center')

        #create world up object 
        #(todo : get front edge center)
        cmds.spaceLocator(n = 'locator_for_z')
        
        vert1 = cmds.select(plane +'.vtx[0]')
        vert1_pos = cmds.xform(vert1, q=True, ws=True, t=True)
        vert2 = cmds.select(plane +'.vtx[1]')
        vert2_pos = cmds.xform(vert2, q=True, ws=True, t=True)
        
        p_x = (vert1_pos[0] + vert2_pos[0])/2
        p_y = (vert1_pos[1] + vert2_pos[1])/2
        p_z = (vert1_pos[2] + vert2_pos[2])/2
        
        p = [p_x, p_y, p_z]
        #p = np.average(np.array((vert1_pos, vert2_pos)), axis = 0)
        
        cmds.move(p[0],p[1],p[2], 'locator_for_z')
        cmds.scale(0.1,0.1,0.1,'locator_for_z')

        #set aim constraint
        cmds.aimConstraint('locator_normal_aim', 'locator_center',
                           wut='object', wuo='locator_for_z', n = 'aim_node')

        #parent the plane and align
        cmds.parent(plane, 'aim_node')
        cmds.move(0,fn_y,0, 'locator_normal_aim')
        cmds.move(0,0,1, 'locator_for_z')

    def movePivot(self, c, obj):
        cmds.move(c[0], c[1], c[2], obj + '.scalePivot')
        cmds.move(c[0], c[1], c[2], obj + '.rotatePivot')

    def mainFunc(self):
        original_height = float(self.float_height.value())
        #define values
        verts = cmds.ls(os = True)
        verts_pos = cmds.xform(verts, q=True, ws = True, t = True)
        v0 = cmds.xform(verts[0], q=True, ws = True, t = True)
        v1 = cmds.xform(verts[1], q=True, ws = True, t = True)
        v2 = cmds.xform(verts[2], q=True, ws = True, t = True)
        v3 = cmds.xform(verts[3], q=True, ws = True, t = True)
        print v0, v1, v2, v3
        
        """not using numpy
        """
        cp_x = (v0[0]+v1[0]+v2[0]+v3[0])/4
        cp_y = (v0[1]+v1[1]+v2[1]+v3[1])/4
        cp_z = (v0[2]+v1[2]+v2[2]+v3[2])/4
        
        cp = [cp_x, cp_y, cp_z]
        
        """ using numpy
        verts_pos = np.reshape(np.array(verts_pos), (len(verts_pos)/3,3))
        cp = np.average(verts_pos, axis = 0)
        """
        
        object = verts[0].split('.vtx')[0]
        plane = 'bottom_plane'

        #create plane for alignment
        cmds.polyCreateFacet(p =(v0,v1,v2,v3), n = plane)
        self.movePivot(cp, object)
        self.movePivot(cp, plane)
        cmds.parent(object, plane)
        cmds.move(-cp[0],-cp[1],-cp[2], plane)
        self.align_plane(plane)

        #clean up the aid objects
        cmds.parent(plane + '|' + object, world = True)
        #cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=2)
        cmds.delete(plane)
        cmds.delete('locator_center')
        cmds.delete('locator_normal_aim')
        cmds.delete('locator_for_z')
        
        
        bb = cmds.exactWorldBoundingBox()
        height = bb[4] - bb[1]
        print height
        s = original_height/height
        print s
        cmds.scale(s,s,s, object)
        #cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=2)

if __name__ == "__main__":
    
    try:
        ui.close()
    except:
        pass
        
    ui = Ui()
    ui.show()

    

    