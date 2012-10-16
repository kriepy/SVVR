import vtk

class Histogram:

    def __init__(self, binsCount, reader):
        self.Reader = reader
        self.BinsCount = binsCount
        self.BinStep = 0
        self.ScalarRange = [0, 0]
        self.FreqArray = vtk.vtkDataArray.CreateDataArray(vtk.VTK_INT)
        self.FreqArray.SetNumberOfComponents(1)

        extract = vtk.vtkImageExtractComponents()
        extract.SetInputConnection(self.Reader.GetOutputPort())
        extract.SetComponents(0)
        extract.Update()
        extract.GetOutput().GetScalarRange(self.ScalarRange)

        self.BinStep = (self.ScalarRange[1] - self.ScalarRange[0]) / self.BinsCount

        histo = vtk.vtkImageAccumulate()
        histo.SetInputConnection(extract.GetOutputPort())
        histo.SetComponentExtent(0, self.BinsCount, 0, 0, 0, 0)
        histo.SetComponentOrigin(self.ScalarRange[0], 0, 0)
        histo.SetComponentSpacing(self.BinStep,  0, 0)
        histo.SetIgnoreZero(False)
        histo.Update()

        for j in range(0, self.BinsCount):
            compValue = histo.GetOutput().GetPointData().GetScalars().GetValue(j)
            self.FreqArray.InsertNextTuple1(compValue)

        lastBinValue = self.FreqArray.GetComponent(self.BinsCount - 1, 0)
        binValue = histo.GetOutput().GetPointData().GetScalars().GetValue(self.BinsCount)
        self.FreqArray.SetComponent(self.BinsCount - 1, 0, lastBinValue + binValue)

    def getBinCenter(self, index):
        return self.ScalarRange[0] + self.BinStep / 2 + self.BinStep * index

    def plotHistogram(self, renderer):
        barChart = vtk.vtkBarChartActor()
        dataObject = vtk.vtkDataObject()
        dataObject.GetFieldData().AddArray(self.FreqArray)

        for i in range(0, self.BinsCount):
            barChart.SetBarLabel(i, "{0:.2f}".format(self.getBinCenter(i)))

        barChart.SetInput(dataObject)
        barChart.GetLegendActor().SetNumberOfEntries(dataObject.GetFieldData().GetArray(0).GetNumberOfTuples())
        barChart.LegendVisibilityOff()
        barChart.LabelVisibilityOn()
        barChart.GetProperty().SetColor(1, 1, 1)
        renderer.AddActor(barChart)

    def printBinValues(self):
        for i in range(0, self.BinsCount):
            print "{0}: [{1}]".format(str(i), str(self.FreqArray.GetComponent(i, 0)))

    def printBinCenters(self):
        for i in range(0, self.BinsCount):
            print "{0}: {1}".format(str(i), str(self.getBinCenter(i)))

    def getBinsCount(self):
        return self.BinsCount

    def getScalarRange(self):
        return self.ScalarRange[0], self.ScalarRange[1]

    def getBinValueAtIndex(self, index):
        if index >= self.BinsCount:
            print 'Error: Index must be less than {0}'.format(str(index))
            return -1

        return  self.FreqArray.GetComponent(index, 0)

    def setBinValueAtIndex(self, index, newValue):
        if index >= self.BinsCount:
            print 'Error: Index must be less than {0}'.format(str(index))
            return -1

        self.FreqArray.SetComponent(index, 0, newValue)

    def normalizeHistogram(self, const):
        for i in range(0, self.BinsCount):
            binValue = self.FreqArray.GetComponent(i, 0)
            self.FreqArray.SetComponent(i, 0, binValue / const)
