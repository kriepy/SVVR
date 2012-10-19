import vtk

file_path = '../Data/1000_KORAALS1/20110617/00006_POLS_0_5_MM'
threshold = [-700, -700]
n_regions = 0

# Load the data from a folder containing DICOM images
def loadData():
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(file_path)
    reader.Update()
    imageData = vtk.vtkImageData()
    imageData.DeepCopy(reader.GetOutput())
    return reader

def select(connected):
    selector = vtk.vtkThresholdPoints()
    selector.SetInput(connected.GetOutput())
    print n_regions
    for i in range(10,11):#change to n_regions
        selector.ThresholdBetween(48,48)
        selector.SetInputArrayToProcess(1, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_CELLS, "RegionId" )
        selector.Update()
        triangles = vtk.vtkTriangleFilter()
        triangles.SetInputConnection(selector.GetOutputPort())
        [V, A] = getMassProperties(triangles)
        print ("The volume is: " + str(V) + "\n")
    return selector

def connectivityFilter(polyData):
    connectivityFilter = vtk.vtkPolyDataConnectivityFilter()
    connectivityFilter.SetInputConnection(polyData.GetOutputPort())
    connectivityFilter.SetExtractionModeToAllRegions()
    connectivityFilter.ColorRegionsOn()
    connectivityFilter.Update()
    global n_regions
    n_regions = connectivityFilter.GetNumberOfExtractedRegions()
    print ("number of regions extracted: " + str(n_regions) + "\n")
    return connectivityFilter

def getMassProperties(triangles):
    mass = vtk.vtkMassProperties()
    mass.SetInputConnection(triangles.GetOutputPort())
    
    return mass.GetVolume(), mass.GetSurfaceArea()

# Generate the Isosurface using pre-specified threshold
def generateIsosurface(reader):
    isoSurface = vtk.vtkContourFilter()
    isoSurface.SetInputConnection(reader.GetOutputPort())
    isoSurface.GenerateValues(1, threshold)
    return isoSurface

def createGeometry(surface):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(surface.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    return actor

def triangulateData(surface):
    triangles = vtk.vtkTriangleFilter()
    triangles.SetInputConnection(surface.GetOutputPort())
    
    return triangles

# Run the visualization
def runVisualization(actor):
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.2, 0.2, 0.2)
    renderer.ResetCamera()
    
    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(800, 600)
    
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(window)
    
    window.Render()
    iren.Start()

# The main pipeline
def runMain():
    reader = loadData()
    isoSurface = generateIsosurface(reader)
    connected = connectivityFilter(isoSurface)
    selected = select(connected)
    triangSurface = triangulateData(selected)
    actor = createGeometry(triangSurface)

    runVisualization(actor)

    
if __name__ == "__main__":
    runMain()
