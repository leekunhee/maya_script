import maya.OpenMayaUI as omui
import maya.cmds as cmds
from PySide import QtCore, QtGui
from shiboken import wrapInstance
import math
#todo : escape cologne

def getVertexPosition(obj, num):
    v = cmds.select(obj +'.vtx[{0}]'.format(num))
    p = cmds.xform(v, q=True, ws=True, t=True)
    return p

def getVertexDistance(obj, num1, num2):
    p1 = getVertexPosition(obj, num1)
    p2 = getVertexPosition(obj, num2)
    distance = math.sqrt(diffSquare(p2[0],p1[0])
                         +diffSquare(p2[1],p1[1])
                         +diffSquare(p2[2],p1[2]))
    return distance

def diffSquare(num1, num2):
    return (num2 - num1) * (num2 - num1)   
    
def setLocators(plane):
    cmds.select(plane)
    fn = cmds.polyInfo(fn=True)
    #get face normal direction
    fn_x = float(fn[0].split(" ")[7])
    fn_y = float(fn[0].split(" ")[8])
    fn_z = float(fn[0].split(" ")[9])

    #get face center position
    p0 = getVertexPosition(plane, 0)
    p1 = getVertexPosition(plane, 1)
    p2 = getVertexPosition(plane, 2)
    
    px = (p0[0]+p1[0]+p2[0])/3
    py = (p0[1]+p1[1]+p2[1])/3
    pz = (p0[2]+p1[2]+p2[2])/3
    
    p = [px,py,pz] 
    #p = np.average(np.array((p0,p1,p2)), axis = 0)

    #calc locator position
    lo_x = fn_x + p[0]
    lo_y = fn_y + p[1]
    lo_z = fn_z + p[2]

    #create normal aim locator
    cmds.spaceLocator(n = 'locator_normal_aim_' + plane)
    cmds.move(lo_x, lo_y, lo_z, 'locator_normal_aim_' + plane)
    cmds.scale(0.1,0.1,0.1,'locator_normal_aim_' + plane)

    #create locator center
    cmds.spaceLocator(n = 'locator_center_' + plane)
    cmds.move(p[0], p[1], p[2], 'locator_center_' + plane)
    cmds.scale(0.1,0.1,0.1,'locator_center_' + plane)

    #create world up object 
    #(todo : get front edge center)
    cmds.spaceLocator(n = 'locator_for_z_' + plane)
    vert = cmds.select(plane +'.vtx[0]')
    p = cmds.xform(vert, q=True, ws=True, t=True)
    cmds.move(p[0],p[1],p[2], 'locator_for_z_' + plane)
    cmds.scale(0.1,0.1,0.1,'locator_for_z_' + plane)

    #set aim constraint
    cmds.aimConstraint('locator_normal_aim_' + plane, 'locator_center_' + plane,
                       wut='object', wuo='locator_for_z_' + plane, 
                       n = 'aim_node_' + plane)

    cmds.parent(plane, 'aim_node_' + plane)
    
def drawTriangle(mesh, v1, v2, v3):
    p1 = getVertexPosition(mesh, v1)
    p2 = getVertexPosition(mesh, v2)
    p3 = getVertexPosition(mesh, v3)
    cmds.polyCreateFacet(p =(p1,p2,p3), n = 'triangle_' + mesh)
    cmds.parent(mesh, 'triangle_' + mesh)

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)


class Ui(QtGui.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(Ui, self).__init__(parent)
        
        self.setWindowTitle("  ")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setGeometry(400,300,400,350)
        
        self.create_layout()
        self.create_connections()
    
    def create_layout(self):
        
        self.lbl_source = QtGui.QLabel("SOURCE MESH")
        self.lbl_target = QtGui.QLabel("TARGET MESH")
        self.lbl_source_vtx = QtGui.QLabel("SOURCE MESH VERTEX")
        self.lbl_target_vtx = QtGui.QLabel("TARGET MESH VERTEX")
        
        self.cb_source = QtGui.QComboBox()
        self.cb_target = QtGui.QComboBox()
        
        self.sb_source_v1 = QtGui.QSpinBox()
        self.sb_source_v2 = QtGui.QSpinBox()
        self.sb_source_v3 = QtGui.QSpinBox()
        self.sb_target_v1 = QtGui.QSpinBox()
        self.sb_target_v2 = QtGui.QSpinBox()
        self.sb_target_v3 = QtGui.QSpinBox()
        
        
        self.sb_source_v1.setMaximum(9999999)
        self.sb_source_v2.setMaximum(9999999)
        self.sb_source_v3.setMaximum(9999999)
        self.sb_target_v1.setMaximum(9999999)
        self.sb_target_v2.setMaximum(9999999)
        self.sb_target_v3.setMaximum(9999999)
        
        self.sb_source_v1.setValue(0)
        self.sb_source_v2.setValue(1)
        self.sb_source_v3.setValue(2)
        self.sb_target_v1.setValue(0)
        self.sb_target_v2.setValue(1)
        self.sb_target_v3.setValue(2)
        
        
        list = cmds.ls(tr=1)
        no = ["persp","top","front","side"]
        for item in list:
            if item == "persp" or item == "top" or item == "front" or item == "side":
                pass
            else:
                self.cb_source.addItem(item)
                self.cb_target.addItem(item)
        
        self.cb_source.setCurrentIndex(0)
        self.cb_target.setCurrentIndex(1)
        
        self.btn_source = QtGui.QPushButton("SELECT")
        self.btn_target = QtGui.QPushButton("SELECT")

        self.btn_apply = QtGui.QPushButton("APPLY")
        
        main_layout = QtGui.QVBoxLayout()
        
        layout_source = QtGui.QHBoxLayout()
        layout_target = QtGui.QHBoxLayout()
        layout_source_v = QtGui.QHBoxLayout()
        layout_target_v = QtGui.QHBoxLayout()
        
        layout_source.addWidget(self.lbl_source)
        layout_source.addWidget(self.cb_source)
        layout_source.addWidget(self.btn_source)
        
        layout_target.addWidget(self.lbl_target)
        layout_target.addWidget(self.cb_target)
        layout_target.addWidget(self.btn_target)
        
        layout_source_v.addWidget(self.lbl_source_vtx)
        layout_source_v.addWidget(self.sb_source_v1)
        layout_source_v.addWidget(self.sb_source_v2)
        layout_source_v.addWidget(self.sb_source_v3)
        
        layout_target_v.addWidget(self.lbl_target_vtx)
        layout_target_v.addWidget(self.sb_target_v1)
        layout_target_v.addWidget(self.sb_target_v2)
        layout_target_v.addWidget(self.sb_target_v3)
        
        #it's awesome!!
           
        awesomeLabel = QtGui.QLabel("This plug-in is totally awesome!")
        awesomeAgree = QtGui.QLabel("Yes, It is AWESOME!")
        self.awesomeCheckbox = QtGui.QCheckBox() 

        legendaryAgree = QtGui.QLabel("No, It is legendary")
        self.legendaryCheckbox = QtGui.QCheckBox() 
        
        awesomeLayout = QtGui.QHBoxLayout()
        
        title = QtGui.QLabel("AWESOME ALIGNER")
        title.setStyleSheet("font-size: 30px; font-weight:600")
        
        help = QtGui.QLabel("""
Align two same structured meshes!
HOW TO USE IT :
after 3 vertices of (source/target)mesh and click the following select button.
                            """)
        
        titleLayout = QtGui.QHBoxLayout()
        titleLayout.addWidget(title)
        
        helpLayout = QtGui.QHBoxLayout()
        helpLayout.addWidget(help)
        
        
        awesomeLayout.addWidget(awesomeLabel)
        awesomeLayout.addWidget(self.awesomeCheckbox)
        awesomeLayout.addWidget(awesomeAgree)
        awesomeLayout.addWidget(self.legendaryCheckbox)
        awesomeLayout.addWidget(legendaryAgree)
        
        main_layout.addLayout(titleLayout)
        main_layout.addLayout(helpLayout)
        main_layout.addLayout(layout_source)
        main_layout.addLayout(layout_source_v)
        main_layout.addLayout(layout_target)
        main_layout.addLayout(layout_target_v)
        main_layout.addLayout(awesomeLayout)
        main_layout.addWidget(self.btn_apply)
        
        self.setLayout(main_layout)
    
    def create_connections(self):
        self.btn_apply.clicked.connect(self.apply)
        self.btn_source.clicked.connect(self.source_select)
        self.btn_target.clicked.connect(self.target_select)
        
    #@classmethod <<--wtf is it?
    def source_select(self):
        selected = cmds.ls(sl=1)[0].split('.')[0]
        self.cb_source.addItem(selected)
        n = self.cb_source.count()
        self.cb_source.setCurrentIndex(n-1)
        s= cmds.ls(os=1)
        if len(s) == 3:
            v1 = int(s[0].split('[')[1].split(']')[0])
            v2 = int(s[1].split('[')[1].split(']')[0])
            v3 = int(s[2].split('[')[1].split(']')[0])
            self.sb_source_v1.setValue(v1)
            self.sb_source_v2.setValue(v2)
            self.sb_source_v3.setValue(v3)
        else:
            cmds.error("please select 3 vertecies")
            
    
    def target_select(self):
        selected = cmds.ls(sl=1)[0].split('.')[0]
        self.cb_target.addItem(selected)
        n = self.cb_target.count()
        self.cb_target.setCurrentIndex(n-1)
        s= cmds.ls(os=1)
        if len(s) == 3:
            v1 = int(s[0].split('[')[1].split(']')[0])
            v2 = int(s[1].split('[')[1].split(']')[0])
            v3 = int(s[2].split('[')[1].split(']')[0])
            self.sb_target_v1.setValue(v1)
            self.sb_target_v2.setValue(v2)
            self.sb_target_v3.setValue(v3)
        else:
            cmds.error("please select 3 vertecies")
    
    def apply(self):
        if self.awesomeCheckbox.isChecked() == 1 and self.legendaryCheckbox.isChecked() == 1:
            cmds.error("lawyered!")
        
        if self.cb_source.currentText() == self.cb_target.currentText():
            cmds.error("source and target objects are same!")
        else:
            #setup variables 
            m_sub = self.cb_source.currentText()
            m_obj = self.cb_target.currentText()
            drawTriangle(m_sub, 
                            self.sb_source_v1.value(), 
                            self.sb_source_v2.value(), 
                            self.sb_source_v3.value())
            drawTriangle(m_obj, 
                            self.sb_target_v1.value(), 
                            self.sb_target_v2.value(), 
                            self.sb_target_v3.value())
            #setting up the locators for align two meshes.
            sub = 'triangle_' + m_sub
            obj = 'triangle_' + m_obj
            setLocators(sub)
            setLocators(obj)

            #move subjector's locators to object's locators
            sl = 'locator_normal_aim_' + sub
            ol = 'locator_normal_aim_' + obj
            cmds.copyAttr(ol, sl,values=True,attribute=['tx','ty','tz'])

            sl = 'locator_center_' + sub
            ol = 'locator_center_' + obj
            cmds.copyAttr(ol, sl,values=True,attribute=['tx','ty','tz'])

            sl = 'locator_for_z_' + sub
            ol = 'locator_for_z_' + obj
            cmds.copyAttr(ol, sl,values=True,attribute=['tx','ty','tz'])

            #set subject pivot to object center
            goto = cmds.getAttr('locator_center_' + obj +'.t')
            
            #g = np.array(goto[0])
            g = [float(goto[0][0]), float(goto[0][1]), float(goto[0][2])]
            
            cmds.move(g[0],g[1],g[2], sub + '.scalePivot')
            cmds.move(g[0],g[1],g[2], sub + '.rotatePivot')

            #set scale of subject
            s = getVertexDistance(obj,0,1) / getVertexDistance(sub,0,1)
            cmds.makeIdentity(sub, apply=1, t=0,s=1,r=0)
            cmds.scale(s,s,s, sub)
            cmds.parent(m_sub, world=1)
            cmds.parent(m_obj, world=1)
            
            sl = 'locator_normal_aim_' + sub
            ol = 'locator_normal_aim_' + obj
            cmds.delete(sl)
            cmds.delete(ol)

            sl = 'locator_center_' + sub
            ol = 'locator_center_' + obj
            cmds.delete(sl)
            cmds.delete(ol)

            sl = 'locator_for_z_' + sub
            ol = 'locator_for_z_' + obj
            cmds.delete(sl)
            cmds.delete(ol)
            
            cmds.makeIdentity(m_sub, apply=1, t=1,s=1,r=1)
            cmds.select(m_sub)
            cmds.move(0,0,0, m_sub + '.scalePivot')
            cmds.move(0,0,0, m_sub + '.rotatePivot')
            cmds.DeleteHistory()


if __name__ == "__main__":
    
    try:
        ui.close()
    except:
        pass
        
    ui = Ui()
    ui.show()
    

    