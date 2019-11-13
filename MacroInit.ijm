macro "Initialize Haralick Features Plugin [s]" {
	thisDirectory = getDirectory("imagej") + "jars/HaralickFeaturesInteractive/";
	jythonText = File.openAsString(thisDirectory + "StartScript.py");
	call("ij.plugin.Macro_Runner.runPython", jythonText, "");
}
macro "Analyze Cardiomyocyte [c]" {
	thisDirectory = getDirectory("imagej") + "jars/HaralickFeaturesInteractive/";
	jythonText = File.openAsString(thisDirectory + "AnalyzeCardiomyocyte.py");
	call("ij.plugin.Macro_Runner.runPython", jythonText, "");
}
macro "Analyze Nucleus [n]" {
	thisDirectory = getDirectory("imagej") + "jars/HaralickFeaturesInteractive/";
	jythonText = File.openAsString(thisDirectory + "AnalyzeNucleus.py");
	call("ij.plugin.Macro_Runner.runPython", jythonText, "");
}
macro "Change Estimated Sarcomere Length [r]" {
	thisDirectory = getDirectory("imagej") + "jars/HaralickFeaturesInteractive/";
	jythonText = File.openAsString(thisDirectory + "ChangeSarcomereLength.py");
	call("ij.plugin.Macro_Runner.runPython", jythonText, "");
}
