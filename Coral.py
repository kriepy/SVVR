import vtk

reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName('/home/mihai/Desktop/1000_KORAALS1/20110617/00006_POLS_0_5_MM')
reader.Update()

imageData = vtk.vtkImageData()
imageData.DeepCopy(reader.GetOutput())

opacityFunction = vtk.vtkPiecewiseFunction()
opacityFunction.AddPoint(0, 0.25)
opacityFunction.AddPoint(1000, 0.75)
colorFunction = vtk.vtkColorTransferFunction()

volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorFunction)
volumeProperty.SetScalarOpacity(opacityFunction)
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.ShadeOff()

volume = vtk.vtkVolume()
volume.SetProperty(volumeProperty)

mapper = vtk.vtkFixedPointVolumeRayCastMapper()
mapper.SetInput(imageData)
mapper.SetSampleDistance(1.0)
mapper.SetBlendModeToMaximumIntensity()

volume.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.SetBackground(1, 0.25, 0.5)
renderer.AddVolume(volume)
renderer.ResetCamera()

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.SetSize(800, 600)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(window)

iren.Initialize()
iren.Start()