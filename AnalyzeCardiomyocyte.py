def findMaxima(seq):
    maxSeqList = []
    eSeq = enumerate(seq)
    for i, el in eSeq:
        if (i == 0  and el > seq[i + 1] or
        i == len(seq) - 1 and el > seq[i - 1] or
        el > seq[i - 1] and el > seq[i + 1]):
            maxSeqList.append([i])
            continue
        elif i == len(seq) - 1 or (i == 0 and el < seq[i + 1]):
            continue
        elif (i == 0 and el == seq[i+1] or
        el > seq[i - 1] and el == seq[i + 1]):
            maxSeqList.append([i])
            for j, elj in eSeq:
                if j == len(seq) - 1 and elj == seq[j - 1]:
                    maxSeqList[-1].append(j)
                    break
                elif (j == len(seq) - 1):
                    break
                elif elj == seq[j + 1]:
                    maxSeqList[-1].append(j)
                    continue
                elif elj > seq[j + 1]:
                    maxSeqList[-1].append(j)
                    break
                elif elj <  seq[j + 1]:
                    maxSeqList.pop()
                    break
                else:
                    break
    for i, el in enumerate(maxSeqList):
        maxSeqList[i] = round(sum(el) / len(el))
    return maxSeqList


def findMinima(seq):
    maxSeqList = []
    eSeq = enumerate(seq)
    for i, el in eSeq:
        if (i == 0  and el < seq[i + 1] or
        i == len(seq) - 1 and el < seq[i - 1] or
        el < seq[i - 1] and el < seq[i + 1]):
            maxSeqList.append([i])
            continue
        elif i == len(seq) - 1 or (i == 0 and el > seq[i + 1]):
            continue
        elif (i == 0 and el == seq[i+1] or
        el < seq[i - 1] and el == seq[i + 1]):
            maxSeqList.append([i])
            for j, elj in eSeq:
                if j == len(seq) - 1 and elj == seq[j - 1]:
                    maxSeqList[-1].append(j)
                    break
                elif (j == len(seq) - 1):
                    break
                elif elj == seq[j + 1]:
                    maxSeqList[-1].append(j)
                    continue
                elif elj < seq[j + 1]:
                    maxSeqList[-1].append(j)
                    break
                elif elj >  seq[j + 1]:
                    maxSeqList.pop()
                    break
                else:
                    break
    for i, el in enumerate(maxSeqList):
        maxSeqList[i] = round(sum(el) / len(el))
    return maxSeqList


def dilate(seq, radius):
    orseq = seq
    seq = list(orseq)
    for i, _ in enumerate(seq):
        mini = i - radius
        maxi = i + radius
        mini = mini if mini >= 0 else 0
        maxi = maxi if maxi < len(seq) else len(seq) - 1
        seq[i] = max(orseq[mini : maxi + 1])
    return seq

def erode(seq, radius):
    orseq = seq
    seq = list(orseq)
    for i, _ in enumerate(seq):
        mini = i - radius
        maxi = i + radius
        mini = mini if mini >= 0 else 0
        maxi = maxi if maxi < len(seq) else len(seq) - 1
        seq[i] = min(orseq[mini : maxi + 1])
    return seq


def findMaximaSeqs(seqs, radius):
    minValidRadius = radius / 2
    maxValidRadius = radius * 2
    print("minValidRadius", minValidRadius)
    print("maxValidRadius", maxValidRadius)
    inRadius = int(round(radius / 3))
    seqPointList = []
    for seq in seqs:
        forMaxima = erode(dilate(seq, inRadius), inRadius)
        maxima = findMaxima(forMaxima)
        forMinima = dilate(erode(seq, inRadius), inRadius)
        minima = findMinima(forMinima)
        if minima:
            thisMinimum = int(round(minima[0]))
        else:
            thisMinimum = 0
        print('thisMinimum', thisMinimum)
        thisMaximum = 0
        for i in maxima:
            if (i > minValidRadius and i < maxValidRadius):
                print("thisMaximum", int(round(i)))
                thisMaximum = int(round(i))
                break
        minHeight = seq[thisMinimum]
        maxHeight = 0 if thisMaximum == 0 else seq[thisMaximum]
        strength = maxHeight - minHeight
        seqPointList.append((strength, thisMaximum, thisMinimum, minHeight, maxHeight))
    retSeqP = (0,0,0,0,0)
    for seqP in seqPointList:
        print(seqP[-1])
        if (seqP[-1] > retSeqP[-1]) and seqP[2] > 0:
            retSeqP = seqP
    return retSeqP





from ij.measure import ResultsTable
from ij import WindowManager
from ij.gui import NonBlockingGenericDialog
from ij import IJ
import sys
sys.path.append(IJ.getDirectory("imagej") + "/jars/HaralickFeaturesInteractive/")

from Haralick_Features import Haralick_Features as hf


cmChan = int(IJ.getProperty("cmChan"))

analyte = WindowManager.getCurrentImage()
analyte.setC(cmChan)
title = analyte.getTitle()
cmNumber = IJ.getProperty("cmNumber")
if cmNumber is None:
	cmNumber = 1
	IJ.setProperty("cmNumber", cmNumber)
cmNumber += 1
sarcomereLength = IJ.getProperty("sarcomereLength")
if sarcomereLength is None:
	sarcomereLength = 1.5
icalibration = analyte.getCalibration()
pixelDistance = round(icalibration.getRawX(sarcomereLength))
pixelDistance = round(icalibration.getRawX(sarcomereLength))
retval = findMaximaSeqs(
    [list(hfi) for hfi in hf().calculate(analyte, "Sarcomeres", 45, sarcomereLength, 10, 8)], pixelDistance)
print(list(retval))
valplot = WindowManager.getWindow("Angle-Distance Correlation Values").getPlot()
valplot.setColor("black");
valplot.setLineWidth(3);
valplot.add("line",  (icalibration.getX(retval[2] + 1), icalibration.getX(retval[1] + 1)), (retval[3], retval[4]))
valplot.add("line",  (icalibration.getX(retval[2] + 1), icalibration.getX(retval[1] + 1)), (retval[3], retval[3]))
valplot.add("line",  (icalibration.getX(retval[2] + 1), icalibration.getX(retval[1] + 1)), (retval[4], retval[4]))
valplot.add("line",  (icalibration.getX(retval[1] + 1), icalibration.getX(retval[1] + 1)), (retval[3], retval[4]))
valplot.add("line",  (icalibration.getX(retval[2] + 1), icalibration.getX(retval[2] + 1)), (retval[3], retval[4]))
valplot.show();
valplot.update();
proceed = NonBlockingGenericDialog("Accept Or Reject?")
proceed.addCheckbox("Uncheck To Reject", True)
proceed.showDialog()
proceed = proceed.getNextBoolean()
WindowManager.getWindow("Angle-Distance Correlation Values").close()
WindowManager.getImage("pixarr").close()
WindowManager.getImage("DUP_" + title).close()
if proceed:
	roi = analyte.getRoi()
	roiStats = roi.getStatistics()
	ferets = roi.getFeretValues()
	rt = WindowManager.getWindow("Cardiomyocyte Results").getTextPanel().getOrCreateResultsTable()
	a = rt.getCounter()
	rt.setValue("Correlation Score", a,  retval[0])
	rt.setValue("Sarcomere Length", a,  icalibration.getX(retval[1] + 1))
	rt.setValue("Area", a, roiStats.area)
	rt.setValue("MaxFeret", a, ferets[0])
	rt.setValue("MinFeret", a, ferets[2])
	rt.setValue("CmNumber", a, cmNumber)
	IJ.setProperty("cmNumber", cmNumber)
	rt.show("Cardiomyocyte Results")

