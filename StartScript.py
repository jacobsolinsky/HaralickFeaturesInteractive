from ij.measure import ResultsTable
from ij import WindowManager, IJ
from ij.gui import GenericDialog
from ij.process import StackStatistics

def calcMedian(ip):
  hist = StackStatistics(ip).histogram16
  histsum = sum(hist)
  ii = 0
  for jj in range(0, 65536):
    ii += hist[jj]
    if ii > histsum / 2:
      break
  return jj


gd = GenericDialog("Image Information")
gd.addNumericField("Cardiomyocye Stain Channel Number", 1, 0, 10, "")
gd.addNumericField("Nuclear Stain Channel Number", 2, 0, 10, "")
gd.showDialog()
cmChan = int(gd.getNextNumber())
nucChan = int(gd.getNextNumber())
IJ.setProperty("cmChan", cmChan)
IJ.setProperty("nucChan", nucChan)

analyte = WindowManager.getCurrentImage()
title = analyte.getTitle()
IJ.run("Split Channels")
nucTitle = "C{}-{}".format(nucChan, title)
nucIp = WindowManager.getImage(nucTitle)
nucIpMedian = calcMedian(nucIp)
IJ.run(nucIp, "Subtract...", "value=" + str(nucIpMedian) + " stack")
IJ.run("Merge Channels...", "c1=[C1-{}] c2=[C2-{}] create".format(title, title))
cmt = ResultsTable()
cmt.show("Cardiomyocyte Results")
IJ.renameResults("Cardiomyocyte Results")
nuct = ResultsTable()
nuct.show("Nucleus Results")
IJ.renameResults("Nucleus Results")