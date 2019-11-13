from ij import IJ
from ij.gui import GenericDialog
gd = GenericDialog("Change Estimated Sarcomere Length")
gd.addNumericField("Estimated Sarcomere Length", 1.5, 0)
gd.showDialog()
ll = gd.getNextNumber()
IJ.setProperty("sarcomereLength", ll)
