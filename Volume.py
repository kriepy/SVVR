import vtk
from Histogram import Histogram

class Volume:

    def __init__(self, reader):
        self.Reader = reader
        spacing = self.Reader.GetOutput().GetSpacing()
        self.VoxelVolume = spacing[0] * spacing[1] * spacing[2]

    def getVolumeByHistIntegration(self, threshold = 0):
        voxelCount = 0
        histogram = Histogram(1024, self.Reader)

        for i in range(0, histogram.getBinsCount()):
            binCenter = histogram.getBinCenter(i)
            binValue = histogram.getBinValueAtIndex(i)

            if binCenter > threshold:
                voxelCount = voxelCount + binValue

        return voxelCount * self.VoxelVolume

    def getVolumeByVoxelCount(self, threshold = 0):
        dims = self.Reader.GetOutput().GetDimensions()
        voxelCount = 0

        for i in range(0, dims[0] * dims[1] * dims[2]):
            voxelDensity = self.Reader.GetOutput().GetPointData().GetScalars().GetComponent(i, 0)

            if voxelDensity > threshold:
                voxelCount = voxelCount + 1

        return voxelCount * self.VoxelVolume

    def getVolumeByIsosurface(self, threshold = 0):
        isoSurface = vtk.vtkContourFilter()
        isoSurface.SetInputConnection(self.Reader.GetOutputPort())
        isoSurface.SetValue(0, threshold)

        clean_data = vtk.vtkCleanPolyData()
        clean_data.SetInputConnection(isoSurface.GetOutputPort())

        triangles = vtk.vtkTriangleFilter()
        triangles.SetInputConnection(isoSurface.GetOutputPort())

        mass = vtk.vtkMassProperties()
        mass.SetInputConnection(triangles.GetOutputPort())

        return mass.GetVolume()
