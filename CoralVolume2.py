import vtk
from Histogram import Histogram
from Volume import Volume

file_path = '/media/Documents/UvA/Scientific Visualization and Virtual Reality/S1_CroppedSamples/S1_482.vti'
threshold = [0, 0]

def loadData():
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_path)
    reader.Update()

    return reader

def createGeometry(reader, threshold = 0):
    isoSurface = vtk.vtkContourFilter()
    isoSurface.SetInputConnection(reader.GetOutputPort())
    isoSurface.SetValue(0, threshold)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(isoSurface.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor

def runVisualization(reader, actor):
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)

    h = Histogram(10, reader)
    h.plotHistogram(renderer)

    renderer.SetBackground(1, 0.25, 0.25)

    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(window)

    window.Render()
    iren.Start()

def runMain():
    reader = loadData()
    actor = createGeometry(reader, -750)
    vol = Volume(reader)

    print "Volume by voxel count: ", vol.getVolumeByVoxelCount(-750)
    print "Volume by histogram integration: ", vol.getVolumeByHistIntegration(-750)
    print "Volume by isosurface: ", vol.getVolumeByIsosurface(-750)

    runVisualization(reader, actor)

if __name__ == "__main__":
    runMain()
