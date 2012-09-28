import vtk

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('/media/Documents/UvA/Scientific Visualization and Virtual Reality/S1_CroppedSamples/S1_479.vti')
reader.Update()

#thresh = vtk.vtkImageThreshold()
#thresh.SetInputConnection(reader.GetOutputPort())
#thresh.ThresholdBetween(-700, 2500)
#thresh.SetInValue(500)
#thresh.Update()

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

mapper = vtk.vtkSmartVolumeMapper()
mapper.SetInputConnection(reader.GetOutputPort())
mapper.SetBlendModeToComposite()

volume.SetMapper(mapper)
#vol_value = volume.GetVolume()

text = vtk.vtkTextActor()
text.GetTextProperty().SetFontSize(20);
text.GetTextProperty().SetColor(1, 1, 1)
text.SetPosition2(10, 40)
text.SetInput("Hello")

renderer = vtk.vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddVolume(volume)
renderer.AddActor2D(text)
renderer.ResetCamera()

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.SetSize(800, 600)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(window)
iren.Initialize()
iren.Start()