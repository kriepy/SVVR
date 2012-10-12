import vtk

file_path = '../Data/1000_KORAALS1/20110617/00006_POLS_0_5_MM'
threshold = [-700, -700]

# Load the data from a folder containing DICOM images
def loadData():
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(file_path)
    reader.Update()
    imageData = vtk.vtkImageData()
    imageData.DeepCopy(reader.GetOutput())
    return reader

def connectivityFilter(polyData):
    connectivityFilter = vtk.vtkConnectivityFilter()
    connectivityFilter.setInputConnection(polyData.GetOutputPort())
    connectivityFilter.SetExtractionModeToAllRegions()
    connectivityFilter.ColorRegionsOn()
    connectivityFilter.Update()

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

def dataCleanup(surface):
    clean_data = vtk.vtkCleanPolyData()
    clean_data.SetInputConnection(surface.GetOutputPort())
    
    return clean_data

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
    #connected = connectivityFilter(isoSurface)
    cleanSurface = dataCleanup(isoSurface)
    triangSurface = triangulateData(cleanSurface)
    actor = createGeometry(triangSurface)

    [volume, surface] = getMassProperties(triangSurface)
    
    print "Volume:", volume
    print "Surface:", surface

    runVisualization(actor)
    
if __name__ == "__main__":
    runMain()
