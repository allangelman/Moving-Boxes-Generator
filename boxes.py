#boxes.py
import maya.cmds as cmds
import functools
import math

def UI(pWindowTitle, makeBox):
    """
    Creating the user Interface to input various paramters to create a mushroom
    """
    windowID = 'Box'
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
        
    #UI window  
    cmds.window(windowID, title = pWindowTitle, sizeable=True, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,20), (2,200), (3,200)],
                         columnOffset = [(1,'right', 3)])
    
    #input fields
    cmds.separator(h=10,style='none')
    
    cmds.text(label='width: ')
    width = cmds.floatField()
    cmds.separator(h=10,style='none')
    
    cmds.text(label='height: ')
    hieght = cmds.floatField()
    cmds.separator(h=10,style='none')
    
    cmds.text(label='depth: ')
    depth = cmds.floatField()
    cmds.separator(h=10,style='none')
    
    cmds.text(label='angle: ')
    angle = cmds.intSlider(min = 10, max = 80, value=10, step=1) 
    cmds.separator(h=10,style='none')

    cmds.text(label='lid_or_slabs: ')
    lid_or_slabs = cmds.optionMenu( w = 100)
    cmds.menuItem( label='lid' )
    cmds.menuItem( label='slabs' )
    cmds.separator(h=10,style='none') 
    
    cmds.text(label='up_or_down: ')
    up_or_down = cmds.optionMenu( w = 100)
    cmds.menuItem( label='up' )
    cmds.menuItem( label='down' )
    cmds.separator(h=10,style='none') 
    
    #apply button calls makeMushroom
    cmds.button(label='Apply', command=functools.partial(makeBox, width, hieght, depth, 
                                                            angle, lid_or_slabs, up_or_down))
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    cmds.button(label='Cancel', command=cancelCallback)
    cmds.showWindow()
    
def makeBox(width, hieght, depth, angle, lid_or_slabs, up_or_down, *pArgs):
    
    """
    Constructing a mushroom model based on user input on a variety of parameters
    """
    width = cmds.floatField(width, query=True,value = True)
    hieght = cmds.floatField(hieght, query=True,value = True)
    depth = cmds.floatField(depth, query=True,value = True)
    angle = cmds.intSlider(angle, query=True,value = True) 
    lid_or_slabs = cmds.optionMenu(lid_or_slabs, query=True,value = True)
    up_or_down = cmds.optionMenu(up_or_down, query=True,value = True)
   
    #width = 4.0
    #hieght = 5.0
    #depth = 5.0
    #angle = 20
    #slabs = True
    #lid = False
    #up_or_down = 'down'
    
    thickness = min(width,hieght,depth)/30
    
    box_main_inst = cmds.group(empty = True, name ="box_main#")
    box_main_name = cmds.ls(box_main_inst)
    
    Box_inst = cmds.group(empty = True, name ="Box")
    Box_inst_name = cmds.ls(Box_inst)


    #box
    box_inst = cmds.polyCube(n='box', w = width, h = hieght, d = depth)
    box_name = cmds.ls(box_inst[0])
    cmds.delete(box_name[0] +  '.f[' + str(1) + ':' +  str(1)+ ']')
    cmds.move(0, hieght/2.0, 0,  box_inst[0])
    cmds.polyExtrudeFacet(box_name[0] +  '.f[' + str(3) + ':' +  str(5)+ ']', kft=False, ltz=thickness)
    cmds.polyExtrudeFacet(box_name[0] +  '.f[' + str(0) + ':' +  str(1)+ ']', kft=True, ltz=thickness)
    
    corner_inst_a = cmds.polyCube(n='cornerA', w = thickness, h = hieght, d = thickness)
    cmds.move(width/2.0 + thickness/2.0, hieght/2.0, depth/2.0 + thickness/2.0,  corner_inst_a[0])
    
    corner_inst_b = cmds.polyCube(n='cornerB', w = thickness, h = hieght, d = thickness)
    cmds.move(width/2.0 + thickness/2.0, hieght/2.0, -depth/2.0 - thickness/2.0,  corner_inst_b[0])
    
    corner_inst_c = cmds.polyCube(n='cornerC', w = thickness, h = hieght, d = thickness)
    cmds.move(-width/2.0 - thickness/2.0, hieght/2.0, depth/2.0 + thickness/2.0,  corner_inst_c[0])
    
    corner_inst_d = cmds.polyCube(n='cornerD', w = thickness, h = hieght, d = thickness)
    cmds.move(-width/2.0 - thickness/2.0, hieght/2.0, -depth/2.0 - thickness/2.0,  corner_inst_d[0])
   
    
    #lid
    if lid_or_slabs == 'lid':
        lid_inst_1 = cmds.duplicate( box_inst )
        lid_inst_2 = cmds.duplicate( corner_inst_a )
        lid_inst_3 = cmds.duplicate( corner_inst_b )
        lid_inst_4 = cmds.duplicate( corner_inst_c )
        lid_inst_5 = cmds.duplicate( corner_inst_d )
        lid_inst = cmds.group(empty = True, name ="lid#")
        cmds.parent(lid_inst_1, lid_inst)
        cmds.parent(lid_inst_2, lid_inst)
        cmds.parent(lid_inst_3, lid_inst)
        cmds.parent(lid_inst_4, lid_inst)
        cmds.parent(lid_inst_5, lid_inst)
        lid_name = cmds.ls(lid_inst)
        cmds.scale( 1.1, 0.1, 1.1, lid_name[0])
        cmds.rotate(0, 0, str(180) + 'deg', lid_name[0], r=True)
        cmds.move(0, hieght, 0,  lid_name[0])
        cmds.parent(lid_inst, Box_inst)
    
    width = width + 2*thickness
    
    #slabs
    if lid_or_slabs == 'slabs':
        slab_inst_a = cmds.polyPlane(n='slabA', w = width, h = depth/2.0)
        slab_a_name = cmds.ls(slab_inst_a[0])
        cmds.polyExtrudeFacet( ltz=thickness)
        cmds.move(0, hieght - thickness, (depth/2.0)*1.5,  slab_inst_a[0])
        cmds.xform(r=True, rp=(0, 0, -(depth/4.0)))
        if up_or_down == 'up':
            cmds.rotate(str(-angle) + 'deg', 0, 0, slab_a_name, r=True)
        else:
            cmds.rotate(str(angle) + 'deg', 0, 0, slab_a_name, r=True)
        cmds.parent(slab_inst_a, Box_inst)
        
        slab_inst_b = cmds.polyPlane(n='slabB', w = width, h = depth/2.0)
        slab_b_name = cmds.ls(slab_inst_b[0])
        cmds.polyExtrudeFacet( ltz=thickness)
        cmds.move(0, hieght - thickness, -(depth/2.0)*1.5,  slab_inst_b[0])
        cmds.xform(r=True, rp=(0, 0, (depth/4.0)))
        if up_or_down == 'up':
            cmds.rotate(str(angle) + 'deg', 0, 0, slab_b_name, r=True)
        else:
            cmds.rotate(str(-angle) + 'deg', 0, 0, slab_b_name, r=True)
        cmds.parent(slab_inst_b, Box_inst) 
        
        slab_inst_c = cmds.polyPlane(n='slabC', w = depth, h = width/2.0)
        slab_c_name = cmds.ls(slab_inst_c[0])
        cmds.polyExtrudeFacet( ltz=thickness)
        cmds.rotate(0, '90deg', 0, slab_c_name, r=True)
        cmds.move((width/2.0)*1.5, hieght - thickness, 0,  slab_inst_c[0])
        cmds.xform(r=True, rp=(0, 0, -(width/4.0)))
        if up_or_down == 'up':
            cmds.rotate(0, 0, str(angle) + 'deg', slab_c_name, r=True)
        else:
            cmds.rotate(0, 0, str(-angle) + 'deg', slab_c_name, r=True)
        cmds.parent(slab_inst_c, Box_inst)
        
        slab_inst_d = cmds.polyPlane(n='slabD', w = depth, h = width/2.0)
        slab_d_name = cmds.ls(slab_inst_d[0])
        cmds.polyExtrudeFacet( ltz=thickness)
        cmds.rotate(0, '90deg', 0, slab_d_name, r=True)
        cmds.move(-(width/2.0)*1.5, hieght - thickness, 0,  slab_inst_d[0])
        cmds.xform(r=True, rp=(0, 0, (width/4.0)))
        if up_or_down == 'up':
            cmds.rotate(0, 0, str(-angle) + 'deg', slab_d_name, r=True)
        else:
            cmds.rotate(0, 0, str(angle) + 'deg', slab_d_name, r=True)
        cmds.parent(slab_inst_d, Box_inst)
        
    cmds.parent(box_inst, box_main_inst)
    cmds.parent(corner_inst_a, box_main_inst)
    cmds.parent(corner_inst_b, box_main_inst)
    cmds.parent(corner_inst_c, box_main_inst)
    cmds.parent(corner_inst_d, box_main_inst)
    cmds.parent(box_main_inst, Box_inst)

UI('Box Input', makeBox)
       
