import vtk

var = raw_input("Enter dataname:")
file_path = '../data/S2-cropped/S2-'+var+'.vti'

th = int(raw_input("Enter threshold:"))

threshold = [th,th]

def loadData():
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_path)
    reader.Update()

    return reader
    
def generateIsosurface(reader):
    isoSurface = vtk.vtkContourFilter()
    isoSurface.SetInputConnection(reader.GetOutputPort())
    isoSurface.GenerateValues(2, threshold)
    
    return isoSurface

def getMassProperties(triangles):
    mass = vtk.vtkMassProperties()
    mass.SetInputConnection(triangles.GetOutputPort())
    
    return mass.GetVolume(), mass.GetSurfaceArea()
    
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
    
def runVisualization(actor):
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1, 0.25, 0.25)
    
    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)
    
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(window)
    
    window.Render()
    iren.Start()

def runMain():
    reader = loadData()
    isoSurface = generateIsosurface(reader)
    cleanSurface = dataCleanup(isoSurface)
    triangSurface = triangulateData(cleanSurface)
    actor = createGeometry(triangSurface)
    
    [volume, surface] = getMassProperties(triangSurface)
    
    print "Volume:", volume
    print "Surface:", surface
    
    runVisualization(actor)
    
if __name__ == "__main__":
    runMain()
