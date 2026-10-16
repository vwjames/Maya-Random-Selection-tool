import maya.cmds as cmds
import random as random

#Updates

#Update when minimum changes
def minUpdate(self):
    x = cmds.intField(randomMin, query = True, value = True)
    cmds.intField(randomMax, edit = True, min = x)
    cmds.intField(randomCutOff, edit = True, min = x)
    cmds.intSlider(cutOff, edit = True, min = x)

#Update when maximum changes
def maxUpdate(self):
    x = cmds.intField(randomMax, query = True, value = True)
    cmds.intField(randomMin, edit = True, max = x)
    cmds.intField(randomCutOff, edit = True, max = x)
    cmds.intSlider(cutOff, edit = True, max = x)

#Update when cutoff changes
def cutOffUpdate(self):
    x = cmds.intField(randomCutOff, query = True, value = True)
    cmds.intSlider(cutOff, edit = True, value = x)

#Updte when slider changes
def sliderUpdate(self):
    x = cmds.intSlider(cutOff, query = True, value = True)
    cmds.intField(randomCutOff, edit = True, value = x)

#Update when dropdown changes
def dropDownUpdate(self):
    x = cmds.optionMenu(selectionType, query = True, sl = True)
    if x == 1:
        cmds.text(toolTipText, edit = True, label='Select objects in object mode, running script will keep a random selection of selected objects')
    if x == 2:
        cmds.text(toolTipText, edit = True, label='Select objects in object mode, running script will select randomly from faces')
    if x == 3:
        cmds.text(toolTipText, edit = True, label='Select objects in object mode, running script will select randomly from edges')
    if x == 4:
        cmds.text(toolTipText, edit = True, label='Select objects in object mode, running script will select randomly from verticies')


#Create random selection window
windowName = "RandomSelection"
if cmds.window(windowName, exists=True):
    cmds.deleteUI(windowName)
    cmds.windowPref(windowName, removeAll=True)

randomWindow = cmds.window(windowName, title="Random Selection", iconName='Short Name', widthHeight=(250, 250), s= False)
cmds.columnLayout(adjustableColumn=True, cal="center", cw=250, h=250)
#Dropdown of selection types
selectionType = cmds.optionMenu(label = 'Selection Type', changeCommand = dropDownUpdate)
cmds.menuItem(label ='Object')
cmds.menuItem(label = 'Face')
cmds.menuItem(label = 'Edge')
cmds.menuItem(label = 'Vertex')
#Chcekbox to toggle using children as well.
objectChildren = cmds.checkBox(label = "Use children of selected objects as well?")

cmds.columnLayout(h = 5)
cmds.setParent('..')
toolTipText = cmds.text(label= 'Select objects in object mode, running script will keep a random selection of selected objects', align='center', ww = True, width = 250)
cmds.columnLayout(h = 5)
cmds.setParent('..')


cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 35),(2,72.5), (3, 35),(4,72.5), (5, 35)], bgc = (0.2, 0.2, 0.2))
cmds.text( label='Min' )
cmds.columnLayout()
cmds.setParent('..')
cmds.text( label='Cutoff' )
cmds.columnLayout()
cmds.setParent('..')
cmds.text( label='Max' )
cmds.setParent('..')

cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 35),(2,72.5), (3, 35),(4,72.5), (5, 35)], bgc = (0.2, 0.2, 0.2))

#Minimum field
randomMin = cmds.intField(value = 0, max = 10, changeCommand = minUpdate)
cmds.columnLayout()
cmds.setParent('..')
#Cutoff field
randomCutOff = cmds.intField(value = 5, max = 10, min = 0, changeCommand = cutOffUpdate)
cmds.columnLayout()
cmds.setParent('..')
#Maximum field
randomMax = cmds.intField(value = 10, min = 0, changeCommand = maxUpdate)
cmds.setParent('..')
cutOff = cmds.intSlider( min = cmds.intField(randomMin, query = True, value = True), max = cmds.intField(randomMax, query = True, value = True), value=5, step=1, changeCommand = sliderUpdate)

#Button that runs function
cmds.button(label='Select Randomly', command=('randomSelection(cmds.optionMenu(selectionType, query = True, sl = True), cmds.intField(randomMin, query = True, value = True), cmds.intField(randomMax, query = True, value = True), cmds.intSlider(cutOff, query = True, value = True), cmds.checkBox(objectChildren, q=True, value =True))'))

cmds.button(label='Close', command=('cmds.deleteUI(\"' + randomWindow + '\", window=True)'))

cmds.setParent('..')



cmds.window(randomWindow, edit=True, visible=True, widthHeight=(250, 250))


#Random Selection function
def randomSelection(selectionType = 1, lowRange=0, highRange=1, cutOff=0, objectChildren = True):
    #Get currently selected objects
    selected = cmds.ls(selection = True)
    selectedObjects = []
    #For object selection type, find the list of objects to operate on
    if selectionType == 1:
        selectedObjects = selected
        #if select object children is toggled on, find the object children of currently selected object
        if objectChildren:
            for x in selected:
                children = cmds.listRelatives(x, ad=True, typ = "transform")
                if children != None:
                    selectedObjects = selectedObjects + children
        print(selectedObjects)
        cmds.select(clear=True)
    #For all other selection types, find the list of shapes to operate on
    else:
        #if select object children is toggled on, find the shape children of currently selected object and children down the tree
        if objectChildren:
            for x in selected:
                selectedObjects = selectedObjects + cmds.listRelatives(x, ad=True, typ = "shape")
            print(selectedObjects)
        #if select object children is not on, find the shape children of currently selected object and children down the tree
        else:
            for x in selected:
                selectedObjects = selectedObjects + cmds.listRelatives(x, c=True, typ = "shape")
            print(selectedObjects)


    if selectionType == 2:
        selected = []
        #List faces
        for x in selectedObjects:
            selectedComponents = cmds.ls("{}.f[:]".format(x), fl = True)
            selected = selected + selectedComponents
            print(selected)
    if selectionType == 3:
        selected = []
        #List edges
        for x in selectedObjects:
            selectedObject = cmds.ls("{}.e[:]".format(x), fl = True)
            selected = selected + selectedObject
            print(selected)
    if selectionType == 4:
        selected = []
        #List vertexes
        for x in selectedObjects:
            selectedObject = cmds.ls("{}.vtx[:]".format(x), fl = True)
            selected = selected + selectedObject
            print(selected)

    for x in selected:
        #using list generated, randomly remove from list acording to the inputs of the slider & fields
        y = random.randint(lowRange, highRange)
        if y <= cutOff:
            cmds.select(x, add = True)

    #If selection type is objects, set selection mode to object
    if selectionType == 1:
        cmds.selectMode(object=True)

    #If selection type is faces, set selection mode to faces
    if selectionType == 2:
        cmds.selectMode(component=True)
        cmds.selectType(pf = True )
        cmds.selectType(pe = False )
        cmds.selectType(pv = False )
        cmds.selectType(puv = False )

    #If selection type is edges, set selection mode to edges
    if selectionType == 3:
        cmds.selectMode(component=True)
        cmds.selectType(pf = False )
        cmds.selectType(pe = True )
        cmds.selectType(pv = False )
        cmds.selectType(puv = False )

    #If selection type is vertexes, set selection mode to vertexes
    if selectionType == 4:
        cmds.selectMode(component=True)
        cmds.selectType(pf = False )
        cmds.selectType(pe = False )
        cmds.selectType(pv = True )
        cmds.selectType(puv = False )
