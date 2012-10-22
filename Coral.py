import vtk

reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName('../Data/1000_KORAALS1/20110617/00006_POLS_0_5_MM')
reader.Update()

imageData = vtk.vtkImageData()
imageData.DeepCopy(reader.GetOutput())

extractor = vtk.vtkExtractVOI()
extractor.SetInput(imageData)
extractor.SetVOI(0,300,0,300,0,300)
extractor.GetVOI()

opacityFunction = vtk.vtkPiecewiseFunction()
opacityFunction.AddPoint(1000, 0.0)
opacityFunction.AddPoint(1400, 0.4)
opacityFunction.AddPoint(1800, 0.0)
opacityFunction.AddPoint(2000, 0.1)
opacityFunction.AddPoint(2400, 0.4)
opacityFunction.AddPoint(2800, 0.0)
colorFunction = vtk.vtkColorTransferFunction()

colorFunction.AddRGBPoint(1400, 0.0, 1.0, 0.0)
colorFunction.AddRGBPoint(2000, 1.0, 0.0, 0.0)
colorFunction.AddRGBPoint(2400, 0.0, 0.0, 1.0)

volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorFunction)
volumeProperty.SetScalarOpacity(opacityFunction)
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.ShadeOff()

volume = vtk.vtkVolume()
volume.SetProperty(volumeProperty)

mapper = vtk.vtkFixedPointVolumeRayCastMapper()
mapper.SetInputConnection(extractor.GetOutputPort())
mapper.SetSampleDistance(1.0)
mapper.SetBlendModeToMaximumIntensity()

volume.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.SetBackground(0, 0.0, 0.0)
renderer.AddVolume(volume)
renderer.ResetCamera()

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.SetSize(800, 600)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(window)

iren.Initialize()
iren.Start()
