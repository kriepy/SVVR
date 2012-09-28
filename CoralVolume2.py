import vtk

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('/media/Documents/UvA/Scientific Visualization and Virtual Reality/S1_CroppedSamples/S1_488.vti')
reader.Update()

thresh = vtk.vtkImageThreshold()
thresh.SetInputConnection(reader.GetOutputPort())
thresh.ThresholdBetween(-700, 2900)
thresh.SetInValue(1)
thresh.SetOutValue(0)
thresh.Update()

iso = vtk.vtkImageMarchingCubes()
iso.SetInputConnection(thresh.GetOutputPort())
iso.Update()

mass = vtk.vtkMassProperties()
mass.SetInputConnection(iso.GetOutputPort())
mass.Update()

print "Volume = ", mass.GetVolume() 
print "Surface = ", mass.GetSurfaceArea()
