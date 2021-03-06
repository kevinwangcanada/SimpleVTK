import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# ImageResample
#

class ImageResample:
  def __init__(self, parent):
    parent.title = "ImageResample" # TODO make this more human readable by adding spaces
    parent.categories = ["SimpleVTK"]
    parent.dependencies = []
    parent.contributors = ["Kevin Wang (Princess Margaret Cancer Centre))"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is an image resample module in SimpleVTK extension.
    """
    parent.acknowledgementText = """
    This file was originally developed by Kevin Wang, Princess Margaret Cancer Centre. and was funded by Sparkit and OCAIRO.
""" # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['ImageResample'] = self.runTest

  def runTest(self):
    tester = ImageResampleTest()
    tester.runTest()

#
# qImageResampleWidget
#

class ImageResampleWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    #
    # Reload and Test area
    #
    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "ImageResample Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    reloadFormLayout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # reference volume selector
    #
    self.referenceSelector = slicer.qMRMLNodeComboBox()
    self.referenceSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.referenceSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.referenceSelector.selectNodeUponCreation = True
    self.referenceSelector.addEnabled = False
    self.referenceSelector.removeEnabled = False
    self.referenceSelector.noneEnabled = False
    self.referenceSelector.showHidden = False
    self.referenceSelector.showChildNodeTypes = False
    self.referenceSelector.setMRMLScene( slicer.mrmlScene )
    self.referenceSelector.setToolTip( "Pick the reference to the algorithm." )
    
    parametersFormLayout.addRow("Reference Volume: ", self.referenceSelector)

    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # resample transform selector
    #
    self.transformSelector = slicer.qMRMLNodeComboBox()
    self.transformSelector.nodeTypes = ( ("vtkMRMLTransformNode"), "" )
    self.transformSelector.selectNodeUponCreation = True
    self.transformSelector.addEnabled = False
    self.transformSelector.removeEnabled = False
    self.transformSelector.noneEnabled = False
    self.transformSelector.showHidden = False
    self.transformSelector.showChildNodeTypes = False
    self.transformSelector.setMRMLScene( slicer.mrmlScene )
    self.transformSelector.setToolTip( "Pick the resample transform to the algorithm." )
    parametersFormLayout.addRow("Resample Transform: ", self.transformSelector)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.outputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.outputSelector.selectNodeUponCreation = False
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = False
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.referenceSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.transformSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode() and self.referenceSelector.currentNode() and self.transformSelector.currentNode()

  def onApplyButton(self):
    logic = ImageResampleLogic()
    print("Run the algorithm")
    logic.run(self.referenceSelector.currentNode(), self.inputSelector.currentNode(), self.transformSelector.currentNode(), self.outputSelector.currentNode())

  def onReload(self,moduleName="ImageResample"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent().parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)

    # delete the old widget instance
    if hasattr(globals()['slicer'].modules, widgetName):
      getattr(globals()['slicer'].modules, widgetName).cleanup()

    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()
    setattr(globals()['slicer'].modules, widgetName, globals()[widgetName.lower()])

  def onReloadAndTest(self,moduleName="ImageResample"):
    try:
      self.onReload()
      evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
      tester = eval(evalString)
      tester.runTest()
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(), 
          "Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")


#
# ImageResampleLogic
#

class ImageResampleLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that 
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def run(self,referenceNode, inputNode, transformNode, outputNode):
    """
    Run the actual algorithm
    """
    dimensions = [1,1,1]
    referenceNode.GetImageData().GetDimensions(dimensions)
    
    inputIJK2RASMatrix = vtk.vtkMatrix4x4()
    inputNode.GetIJKToRASMatrix(inputIJK2RASMatrix)
    referenceRAS2IJKMatrix = vtk.vtkMatrix4x4()
    referenceNode.GetRASToIJKMatrix(referenceRAS2IJKMatrix)
    inputRAS2RASMatrix = transformNode.GetMatrixTransformToParent()
    
    resampleTransform = vtk.vtkTransform()
    resampleTransform.Identity()
    resampleTransform.PostMultiply()
    resampleTransform.SetMatrix(inputIJK2RASMatrix)
    resampleTransform.Concatenate(inputRAS2RASMatrix) 
    resampleTransform.Concatenate(referenceRAS2IJKMatrix)
    resampleTransform.Inverse()
   
    resampler = vtk.vtkImageReslice()
    resampler.SetInput(inputNode.GetImageData())
    resampler.SetOutputOrigin(0,0,0)
    resampler.SetOutputSpacing(1,1,1)
    resampler.SetOutputExtent(0,dimensions[0],0,dimensions[1],0,dimensions[2])
    resampler.SetResliceTransform(resampleTransform)
    resampler.Update()
    
    outputNode.CopyOrientation(referenceNode)
    outputNode.SetAndObserveImageData(resampler.GetOutput())
     
    return True
