
import os
import math
import copy
import csv
import matplotlib
# %matplotlib qt ---- import this function for interactivity
# %matplotlib widget or notebook ----  import this funciton for interactivity - better quality but must only review one graph at a time
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

Folder = r'/Users/anshverma/Documents/UCSF Neuroscape Work /UCSF Data Analysis Files/Meditrain 2020 Summer study/MTOA_Files/MIST'  # folder path with MT data

Folder1 = r'/Users/anshverma/Documents/UCSF Neuroscape Work /UCSF Data Analysis Files/Meditrain 2020 Summer study/Baseline Files/Baseline'  # folder path with Baseline data

NewFilePath = r'/Users/anshverma/Documents/UCSF Neuroscape Work /UCSF Data Analysis Files/Meditrain 2020 Summer study/Processed_MTOA'  # where want to store processed GSR data

def split(word):
    """
    splits string into list of individual characters
    """
    return [char for char in word]


def gatheringfiles(file):
    """this function does the following:
    1) creates a list of files and participant ID's (list of characters in a string)
    """
    if (file == ".DS_Store"):
        return ""

    c2 = 0
    ID = split(file)
    counter = 0
    c3 = 0

    # below while loop finds the participant ID within filename
    while (c2 < len(ID) - 1):
        try:
            while (0 <= int(ID[c2 + 1]) < 10 and 0 <= int(ID[c2]) < 10 and c2 > 7):
                counter += 1
                if ((counter == 2 or counter == 3) and (
                        ID[c2 + 2] == '_' or ID[c2 + 2] == '.')):  # and not(int(ID[c2 + 2]))
                    c3 = c2 + 1
                    c2 == len(ID)
                c2 += 1
            c2 += 1
        except ValueError:
            c2 += 1
            continue

    # returns list of filename and participant ID, which is appended to overall list in another function
    return [file, ID[(c3 - counter):(c3 + 1)]]


def organizingfiles(filestoeval, Folder):
    """this function does the following:
    2) converts each participant ID's into an integer, appends to the end of each sublist with file names
    3) creates a separate list of sorted participant ID's in increasing order
    4) sorts the list of filenames and participant ID's in increasing orders
    5) all filenames with the same participant ID, puts them in a sublist within overall list

    Note - script does NOT check for repeats because decision for which file to use must be done by human - however, do add a repeat checker
    """
    interlist = []

    # below loop converts participant ID list to an integer and appends to the end of sublist where participant ID list used to be
    # also appends integer to a new list, which will be a sorted list of participant ID numbers
    for x in range(0, len(filestoeval)):
        string1 = ""
        for g in range(0, len(filestoeval[x][-1])):
            string1 += filestoeval[x][-1][g]
        filestoeval[x][-1] = int(string1)
        interlist.append(int(string1))
    interlist2 = sorted(interlist)

    filestoeval1 = []

    # makes a new list filestoeval1, which is a sorted version of filestoeval; sorted based on participant ID numbers

    for d in range(0, len(interlist2)):  # works
        x = 0
        while (interlist2[d] != filestoeval[x][-1]):
            x += 1
        tempvar9 = filestoeval.pop(x)
        filestoeval1.append(tempvar9)

    filestoeval2 = []
    iterator = 0

    # appends all the filenames with same ID in a sublist within overall list
    while (iterator < len(filestoeval1)):
        filestoeval3 = []
        giter = 1
        try:
            while (filestoeval1[iterator + giter][-1] == filestoeval1[iterator][-1]):
                giter += 1
        except IndexError:
            ansh = 0
        for q in range(iterator, iterator + giter):
            filestoeval3.append(filestoeval1[q][0])
        iterator = iterator + giter
        filestoeval2.append(filestoeval3)

    checklist = interlist2
    # below gets rid of any repeat participant ID numbers
    interlist2 = set(interlist2)
    interlist2 = list(interlist2)
    interlist2 = sorted(interlist2)

    if (Folder == r'/Users/anshverma/Documents/UCSF Neuroscape Work /UCSF Data Analysis Files/Meditrain 2020 Summer study/MTOA_Files/MIST'):
        for x in range(len(filestoeval2)):
            filestoeval2[x].insert(0, interlist2[x])
            filestoeval2[x].insert(0, "MT")
    else:
        for x in range(len(filestoeval2)):
            filestoeval2[x].insert(0, interlist2[x])
            filestoeval2[x].insert(0, "Baseline")
    return filestoeval2



def addFileToList(list3, x, filename, designation, ID):
    """
    if multiple files for same participant and trial, selects the correct file to use
    """
    replacedict = {'Baseline2714': "Dump055_MTOA_2714_POST.txt" , 'MT2714': "Dump118_MTOA2714_POST.txt",
                   'Baseline2790': "Dump128_MTOA2790_POST.txt", 'MT2790': "Dump129_MTOA_2790_POST.txt",
                   'Baseline2971' : "Dump107_MTOA2971_PRE.txt", 'MT2971': "Dump108_MTOA2971_PRE.txt",
                   'MT3005': "Dump094_MTOA3005_POST.txt", 'MT3152': "Dump106_MTOA3152_POST.txt",
                   'MT3177': "Dump001_MTOA3177_POST_3.txt", 'Baseline3400': "Dump082_MTOA3400_PRE.txt",
                'MT3450': "Dump004_MTOA3450_POST.txt", 'MT3457': "Dump005_MTOA3457_POST.txt", 'MT3635': "Dump003_MTOA3635_PRE.txt",
                'MT3661': "Dump033_MTOA3661_PRE.txt", 'MT4263': "Dump003_MTOA4263_POST.txt"
                   } #dict containing all the correct files to use
    bool1 = True
    while (bool1):
        if (list3[x] == ""):
            list3[x] = filename
            bool1 = False
        elif (type(list3[x]) == str):
            try: #replacing current file with correct file to analyze
                identifier = designation + str(ID)
                list3[x] = replacedict[identifier]
                bool1 = False
            except KeyError: #if correct file does not exist in dictionary, add to dictionary and
            #try to replace current file with this correct file
                print("this is the designation, ID, and filename")
                print(designation, ID, filename)
                input1 = input("input the designation and ID to make a dictionary key")
                input2 = input("input the filename to make a dictionary value")
                replacedict[input1] = input2
    return list3


def intoPrintFormat(filename, list3, designation, ID):
    """
    Given type of file (pre, post, or fu), and designation (MT or Baseline), adds file to correct index in a sublist
    within a bigger list that is used to process raw GSR data in the correct order, so that it is saved in the correct
    format
    """

    counter = 0
    c2 = 7
    c3 = 0
    tempfilename = split(filename)
    while (7 <= c2 < len(tempfilename)):
        L = False
        G = False
        Q = False
        if (tempfilename[c2] == "P" or tempfilename[c2] == "p"):
            if (tempfilename[c2 + 1:c2 + 3] == ["r", "e"] or tempfilename[c2 + 1:c2 + 3] == ["R", "E"]):
                L = True
            elif (tempfilename[c2 + 1:c2 + 4] == ["O", "S", "T"] or tempfilename[c2 + 1:c2 + 4] == ["o", "s", "t"]):
                G = True
            else:
                L = False
                G = False

        elif (tempfilename[c2] == "F" or tempfilename[c2] == "f"):
            Q = True
            if (tempfilename[c2 + 1:c2 + 2] == ["U"] or tempfilename[c2 + 1:c2 + 2] == ["u"]):
                ansh = 0
            elif (tempfilename[c2 + 1:c2 + 8] == ["O", "L", "L", "O", "W", "U", "P"] or tempfilename[c2 + 1:c2 + 8] == [
                "o", "l", "l", "o", "w", "u", "p"]):
                ansh = 1
            else:
                Q = False
        if (designation == "MT"):
            if (L):
                list3 = addFileToList(list3, 4, filename, designation, ID)
                break
            elif (G):
                list3 = addFileToList(list3, 5, filename, designation, ID)
                break
            elif (Q):
                list3 = addFileToList(list3, 6, filename, designation, ID)
                break
        else:
            if (L):
                list3 = addFileToList(list3, 1, filename, designation, ID)
                break
            elif (G):
                list3 = addFileToList(list3, 2, filename, designation, ID)
                break
            elif (Q):
                list3 = addFileToList(list3, 3, filename, designation, ID)
                break
        c2 += 1
    return list3

def savingVals(toggle, listval, Folder, Folder1, retval, ampfilter, noisefilter):
    val1 = 0
    val2 = 0
    if(type(listval) == list):
        for g in listval:
            print(g)
        input1 = input("enter which file you would like to analyze") #has to be correct
        val1, val2 = temppeakdetectionpreprocessing(input1, Folder, Folder1, toggle, retval, ampfilter, noisefilter)
    elif(listval != ""): #fix the indexing below, and also make sure it calls from the right folder to process the data [1: (len(realFinalList[x][y])) - 7]
        print(listval)
        val1, val2 = temppeakdetectionpreprocessing(str(listval), Folder, Folder1, toggle, retval, ampfilter, noisefilter) #edit this function heavily so works with new scenario
    else:
        #listval = "" #edit code this function is in because there is no more break statement
        val1 = ""
        val2 = ""
    print(val1, val2, "this is in savingVals")
    return val1, val2

def savingdata(savingwhichdata, NewFilePath, realFinalList):
    """
    saves processed GSR data into a spreadsheet formatted to be processed by SPSS
    """
    list1 = copy.deepcopy(realFinalList)
    list2 = copy.deepcopy(realFinalList)
    for x in range(1, len(realFinalList)):
        toggle = 0
        for y in range(1, len(realFinalList[x])):
            if(y > 3):
                print("togged to 1", realFinalList[x][y], y)
                toggle = 1
            else:
                print("togged to 2", realFinalList[x][y], y)
                toggle = 2
            try:
                list1[x][y], list2[x][y] = savingVals(toggle, realFinalList[x][y], Folder, Folder1, savingwhichdata, 0.005, 0.1) #finish this function (not done), and test out
                print(list1[x][y], list2[x][y])
            except FileNotFoundError:
                continue
    try:
        with open(NewFilePath + "/MaxPeakValuesV2.csv", 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(list1)
            csvFile.close()
            print("saved MaxPeakValuesV2")
        with open(NewFilePath + "/FilteredAvgGsrValV2.csv", 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(list2)
            csvFile.close()
            print("saved FilteredAvgGsrValV2")
    except PermissionError:
        print("there was an error of some sort")

def temppeakdetectionpreprocessing(file, Folder, Folder1, toggle, retval, amplitudethreshold, signaljump):
    """
    function that processes raw GSR data of a single file to return any of the following processed metrics:
    - Number of Phasic GSR Peaks
    - Average Phasic GSR value
    - Average Amplitude of Phasic GSR Peaks
    - Number of Phasic GSR Peaks in every 20 second interval
    - Average Phasic GSR value in every 20 second interval
    """
    def peakdetection(PhasicGSRVals, addFilters):
        """
        Function that detects peaks and saves the following metrics for peaks:
        - Peak onset value and timestamp
        - Peak offset value and timestamp
        - maximum value of peak and timestamp
        - whether peak was evoked by a stimulus marker or not
        :param PhasicGSRVals: List containing Phasic GSR Values
        :param addFilters: bool which decides whether amplitude and artifact filters are implemented when deciding
        what is a peak
        :return: dictionary with all peaks and their metrics, and the addition of all peak amplitudes
        """

        PeakSets = []
        PeakMax = 0
        l = 0
        peakOnsetExists = 0
        NumberPeaks = 0

        while l < len(PhasicGSRVals):

            c = False

            if (PhasicGSRVals[l] > 0.01):
                c = True
                peakOnsetExists += 1
            else:
                l += 1

            if (c):

                d = 0
                minNum = math.pow(10, -10)
                minNum = 5.0 * minNum

                try:
                    while (PhasicGSRVals[d + l] > minNum):  # have to experiment w/minNum value to make sure not skipping over peaks/combining multiple peaks into one
                        d += 1
                except IndexError:
                    l = l + d
                    print("tried to make peak, couldn't reach end value before went through all Phasic GSR Values")
                    continue

                inc = 0
                sub = l
                while (l + inc < l + d):
                    if (PhasicGSRVals[l + inc] > PhasicGSRVals[sub]):
                        sub = l + inc
                    inc += 1

                PeakAmplitude = float(GSRval[Phasicindexs[sub]]) - float(GSRval[Phasicindexs[l]])

                if (addFilters):
                    startBool = False
                    i = 0
                    while (l + i < l + d):
                        if (i > 0 and abs(PhasicGSRVals[l + i] - PhasicGSRVals[l + i - 1]) > signaljump):
                            artifactdetect = abs(PhasicGSRVals[l + i] - PhasicGSRVals[l + i - 1])
                            # print("there was an artifact of " + str(artifactdetect) + " between two consecutive Phasic GSR data points")
                            # print(str(PhasicGSRVals[l + inc - 1]) + "and " + str(PhasicGSRVals[l + inc] + " are the data points."))
                            startBool = True
                            break
                        i += 1
                    if (startBool):
                        # print("no more peak because artifact present in peak")
                        l = l + d
                        continue
                    if (PeakAmplitude >= amplitudethreshold):
                        pass
                    else:
                        # print("'Peak' amplitude is " + str(PeakAmplitude) + ", too low")
                        #print("Therefore, not counting this 'peak' as a peak")
                        l = l + d
                        continue

                NumberPeaks += 1  # counts number of peaks

                Peak = {}.fromkeys(["Peak Onset", "Peak Offset/MinVal", "PeakMax", "TimeStamp Onset", "TimeStamp Offset",
                     "TimeStamp Max", "Stim Peak"], 0);

                Peak["Peak Onset"] = [PhasicGSRVals[l], float(GSRval[Phasicindexs[l]])]
                Peak["Peak Offset/MinVal"] = [PhasicGSRVals[l + d], float(GSRval[Phasicindexs[l + d]])]
                Peak["PeakMax"] = PeakAmplitude
                PeakMax += PeakAmplitude
                Peak["TimeStamp Onset"] = TimeStamp1[l]
                Peak["TimeStamp Offset"] = TimeStamp1[l + d]
                Peak["TimeStamp Max"] = TimeStamp1[sub]
                Peak["Stim Peak"] = False
                PeakSets.append(Peak)

                if (d > 0):
                    l = l + d
                else:
                    l += 1

        # to check # of peaks and peak metrics
        # print(len(PeakSets))
        # for i in range(30,40):
        # print(PeakSets[i])

        print(PeakMax, "PeakMaxBeforeDivision")
        return PeakSets, PeakMax

    def PhasicGSRAvgPerBin(PhasicGSRVals, TimeStamp):
        """
        returns a dictionary with the average Phasic GSR value per 20 second window
        """
        temp = 4.0  # when starts recording
        BinDict = {}
        x = 0
        activatesaving = False

        while (TimeStamp[x] / 1000 < 4.0):
            x += 1
        # print(x, TimeStamp[x]/1000)
        while (x < len(TimeStamp)):
            PhasicGSRAvg = 0
            y = x
            while (x < len(TimeStamp) and temp <= TimeStamp[x] / 1000 <= temp + 2.0):
                PhasicGSRAvg += PhasicGSRVals[x]
                x += 1
                activatesaving = True
            if (activatesaving):
                PhasicGSRAvg = PhasicGSRAvg / (x - y)
                temp += 2.0
                BinDict[temp - 2.0] = [PhasicGSRAvg, temp]
                activatesaving = False
            else:
                temp += 2.0
        return BinDict


    def peaksperbin(PeakSets):
        """
        returns a dictionary with the number of Phasic GSR Peaks per 20 second window
        :param PeakSets: list with all the phasic GSR peaks (each stored as a dictionary)
        :return: a dictionary containing the number of Phasic GSR Peaks per 20 second window
        """
        temp = 4.0  # timestamp in seconds for when Phasic GSR Values start to exist
        #because of common practice, do not include data for first and last four seconds of trial in analysis
        dict2 = {}
        update = 0
        und = 0
        u = 0
        while (u < len(PeakSets)):
            count = 0
            update = u

            while ((update < len(PeakSets)) and PeakSets[update]["TimeStamp Onset"] / 1000 < temp + 2.0):
                count += 1
                update += 1

            if (update > u):
                u = update
                und += 1  # counts # of new peaks created

            dict2.update({temp: [count, temp, temp + 2.0, PeakSets[update - 1]["TimeStamp Onset"] / 1000]})
            temp += 2.0

        return dict2



    def butter_lowpass_filter(data, order):
        """
        function that implements low pass filter on unfiltered Phasic GSR values
        """
        b, a = butter(order, 0.5, btype='low', analog=False)  # 0.5 is a commonly accepted Hz filter value

        y = filtfilt(b, a, data)
        return y

    def meanfilter(g, GSRval):
        """ function that calculates Phasic GSR data from raw Phasic GSR data using the mean filter"""
        GSRMean = 0
        for val in g:
            GSRMean += val
        GSRMean = GSRMean / (len(g))

        return float(GSRval[x]) - GSRMean

    def medianfilter(g, GSRval):
        """ function that calculates Phasic GSR data from raw Phasic GSR data using the median filter"""
        if (type(len(g) / 2) == int):
            c = g[len(g) / 2]
        else:
            try:
                val_1 = int(len(g) / 2)
                val_2 = val_1 + 1
                c = (g[val_1] + g[val_2]) / 2
            except IndexError:
                if (len(g) == 1):
                    c = g[0]
                elif (len(g) == 2):
                    c = (g[0] + g[1]) / 2

        return float(GSRval[x]) - c

    # lists that will be used to iterate through data in file
    EventName = []
    TimeStamp = []
    MediaTime = []
    LiveMarker = []
    MarkerText = []
    GSRval = []
    filename = file + "peakDetectionGSRData.csv"
    PhasicGsrAvgVal = []

    # variables to check edge cases in program
    a = False
    v = 0
    count = 0
    error_GSRVals_UI_difftimestamp = 0
    error_GSR_UI_sametimestamp = 0
    error_GSR = 0
    error_GSR_time = 0
    error_GSR_both = 0

    # opening file
    if (toggle == 1):
        openfile = open(Folder + "/" + file, "r")
    else:
        openfile = open(Folder1 + "/" + file, "r")
    print(openfile) # see file directory

    dd = 0
    cc = 0
    ee = 0
    ff = 0
    gg = 0
    ll = 0
    mm = 0
    nnnn = 0
    bool5 = False
    bool6 = True
    for line in openfile:  # loop through each line in the file
        row = line.split("\t")  # sep each line by tabs, make into a list can iterate through now

        # finding index's of data collumns
        while v <= 46 and len(row) > 20:
            if (bool(row[v] == 'EventSource') == True):
                h = v
                print(h, 'EventSource')
                v += 1
            elif (bool(row[v] == 'Timestamp') == True):
                j = v
                print(j, 'Timestamp')
                v += 1
            elif (bool(row[v] == 'MediaTime') == True):
                q = v
                print(q, 'MediaTime')
                v += 1
            elif (bool(row[v] == 'StimulusName') == True):
                nnnn = v
                print(nnnn, 'StimulusName')
                v += 1
            elif (bool(row[v] == 'GSR CAL (µSiemens)(Shimmer)') == True or bool(row[v] == 'GSR CAL (µSiemens)(Shimmer Sensor)') == True or bool(row[v] == 'GSR CAL (µSiemens) (Shimmer)') == True or bool(row[v] == 'GSR CAL (µSiemens) (Shimmer Sensor)') == True):  # or
                print(v, "GSR")
                d = v
                v += 1
            elif (bool(row[v] == 'LiveMarker') == True):
                z = v
                print(z, 'LiveMarker')
                v += 1
            elif (bool(row[v] == 'MarkerText') == True):
                t = v
                print(t, 'MarkerText')
                v = 47
                a = True
            else:
                v += 1
        countReal = count - 1

        # iterates through file and appends relevant data to lists to be used later
        if (a and ("Shimmer Shimmer" in row[h])):
            dd += 1

            if (count == 0):
                ee += 1
                GSRval.append(row[d])
                EventName.append(row[h])
                TimeStamp.append(row[j])
                MediaTime.append(row[q])  # only for if gsr before media starts - would use this metric to see this
                MarkerText.append(row[t])
                LiveMarker.append(row[z])
                count += 1
            elif (row[j] != TimeStamp[count - 1] and row[d] == GSRval[count - 1]):  # if this is a new timestamp
                # if this happens, have two same GSR val recorded w/a small timestamp diff
                error_GSR += 1
                mm += 1
                GSRval.append(row[d])
                EventName.append(row[h])
                TimeStamp.append(row[j])
                MediaTime.append(row[q])  # only for if gsr before media starts - would use this metric to see this
                MarkerText.append(row[t])
                LiveMarker.append(row[z])
                count += 1
            elif (row[d] == GSRval[count - 1] and row[j] == TimeStamp[count - 1]):  # if timestamp and gsrval are same, override last input
                error_GSR_both += 1
                EventName[countReal] = row[h]  # will override GSR eventname
                MediaTime[countReal] = row[q]  # should be the same
                MarkerText[countReal] = row[t]  # this and below line are new, with marker now
                LiveMarker[countReal] = row[z]
            elif (row[d] != GSRval[count - 1] and row[j] == TimeStamp[count - 1]):  # will rarely happen
                # if happens, choose Marker GSR Val over reg GSR val
                error_GSR_time += 1
                GSRval[countReal] = row[d]
                EventName[countReal] = row[h]
                EventName[countReal] = row[h]  # will override GSR eventname
                MediaTime[countReal] = row[q]  # should be the same
                MarkerText[countReal] = row[t]
                LiveMarker[countReal] = row[z]
            else:
                cc += 1
                GSRval.append(row[d])
                EventName.append(row[h])
                TimeStamp.append(row[j])
                MediaTime.append(row[q])
                MarkerText.append(row[t])
                LiveMarker.append(row[z])
                count += 1

    PhasicGSRVals = []
    Phasicindexs = []
    TimeStamp1 = []
    NumberPeaks = 0
    bool_2 = False

    for x in range(0, len(TimeStamp)):

        if (float(TimeStamp[x]) >= 4000):  # no GSR vals used from first 4 sec of trial, common practice
            bool_2 = True
        if ((bool_2) and (float(TimeStamp[x]) <= float(
                TimeStamp[-1]) - 4000)):  # no GSR vals used from last 4 sec of trial, common practice
            a = x
            q = x
            g = []
            c = 0
            g.append(float(GSRval[x]))
            try:
                while (a - 1 > 0 and float(TimeStamp[a - 1]) > float(TimeStamp[x]) - 4000):  # (a-1) < len(TimeStamp)
                    a = a - 1
                    g.insert(0, float(GSRval[a]))
            except IndexError:
                print(a)
            while (float(TimeStamp[q + 1]) < float(TimeStamp[x]) + 4000 and (q - 1) < len(TimeStamp)):
                q = q + 1
                g.insert(-1, float(GSRval[q]))

            PhasicGSRVals.append(meanfilter(g, GSRval))

            TimeStamp1.append(int(TimeStamp[x]))  # so have corresponding timestamps to full GSR list
            Phasicindexs.append(int(x))  # corresponding indexs to full GSR list

    """ for visualization of Phasic GSR data and debugging
    
    plt.plot(TimeStamp1[40:670], PhasicGSRVals[40:670])
    plt.xlabel("time")
    plt.ylabel("GSR values")
    plt.title("GSR graph for file")
    plt.show()
    """

    """ for visualization of Phasic GSR data and debugging
    
    plt.plot(TimeStamp1[1000:2000], PhasicGSRVals[1000:2000])
    plt.xlabel("time")
    plt.ylabel("Phasic GSR values")
    plt.title("Phasic GSR graph for file")
    plt.show()
    plt.plot(TimeStamp1[0:len(TimeStamp1) - 1], PhasicGSRVals[0:len(PhasicGSRVals) - 1])
    plt.xlabel("time")
    plt.ylabel("Phasic GSR values")
    plt.title("Phasic GSR graph for file")
    plt.show()
    """

    """ for visualization of Phasic GSR data and debugging
    
    plt.plot(TimeStamp1[1000:2000], PhasicGSRVals1[1000:2000])
    plt.xlabel("time")
    plt.ylabel("Phasic GSR values")
    plt.title("Phasic GSR graph for file")
    plt.show()
    plt.plot(TimeStamp1[0:len(TimeStamp1) - 1], PhasicGSRVals1[0:len(PhasicGSRVals1) - 1])
    plt.xlabel("time")
    plt.ylabel("Phasic GSR values")
    plt.title("Phasic GSR graph for file")
    plt.show()
    """

    """
    plt.plot(TimeStamp1[40:100], PhasicGSRVals[40:100])
    plt.xlabel("time")
    plt.ylabel("GSR values")
    plt.title("GSR graph for file")
    plt.show()
    """

    """ To see peak metrics from unfiltered Phasic GSR data for debugging and for sanity check of data
    
    PeakSets, PeakMax = peakdetection(PhasicGSRVals, False)
    print("Number of peaks with no filters implemented is " + str(len(PeakSets)))
    dict3 = peaksperbin(PeakSets)
    print("Number of peaks in every 20 second interval with no filters implemented is " + str(list(dict3.values())))
    """

    """ To see peak metrics from filtered Phasic GSR data (filtered using artifact and peak amplitude thresholds) for debugging and for sanity check of data
     
    PeakSets, PeakMax = peakdetection(PhasicGSRVals, True)
    print("Number of peaks after peak amplitude and signal jump filters were implemented is " + str(len(PeakSets)))
    dict3 = peaksperbin(PeakSets)
    print("Number of peaks in every 20 second interval after peak amplitude and signal jump filters were implemented is " + str(list(dict3.values())))
    """

    # below detects GSR Peaks
    PeakSets, PeakMax = peakdetection(PhasicGSRVals, True)


    filtered_PhasicGSRVals = butter_lowpass_filter(PhasicGSRVals , 2)

    """ for visualization of Filtered Phasic GSR data and debugging
    
    plt.plot(TimeStamp1[1000:2000], filtered_PhasicGSRVals[1000:2000])
    plt.xlabel("Time")
    plt.ylabel("Filtered Phasic GSR values")
    plt.title("Filtered Phasic GSR Graph")
    plt.show()
    plt.plot(TimeStamp1[0:len(TimeStamp1) - 1], filtered_PhasicGSRVals[0:len(PhasicGSRVals) - 1])
    plt.xlabel("time")
    plt.ylabel("Phasic GSR values")
    plt.title("Phasic GSR graph for file")
    plt.show()
    """

    FilteredPeakSets, NewPeakMax = peakdetection(filtered_PhasicGSRVals, True)
    dict4 = peaksperbin(FilteredPeakSets)
    dict5 = PhasicGSRAvgPerBin(filtered_PhasicGSRVals, TimeStamp1)
    templist = list(dict4.keys())

    # print(len(dict4, sorted(templist)[-1]))
    """ To see peak metrics from Filtered Phasic GSR data (filtered using low-pass filter and artifact and peak amplitude thresholds) for debugging and for sanity check of data
    print("Number of peaks after low pass filter implemented is " + str(len(FilteredPeakSets)))
    print("Number of peaks in every 20 second interval after filter is implemented is " + str(list(dict4.values())))
    NewPeakMax = NewPeakMax/len(filtered_PhasicGSRVals)
    print("FilteredPeakMax", NewPeakMax)
    """

    AvgGSRVal = 0
    for val in filtered_PhasicGSRVals:
        AvgGSRVal += val

    NumberOfPeaks = len(FilteredPeakSets)

    try: # feature is to return avg phasic GSR val
        AvgGSRVal = AvgGSRVal / len(filtered_PhasicGSRVals)
    except ZeroDivisionError:
        print("something is wrong, there are no filtered Phasic Values. We are continuing analysis without the values")
        AvgGSRVal = 0

    try:
        NewPeakMax = NewPeakMax / len(FilteredPeakSets)
    except ZeroDivisionError:
        print("something is wrong, there are no filtered Phasic Peaks. We are continuing analysis without the peaks")
        NewPeakMax = 0

    if (retval == 0):
        return NumberOfPeaks
    elif (retval == 1):
        print("number of peaks", NumberOfPeaks)
        print(NewPeakMax, AvgGSRVal, "finalwhatistobesaved")
        return NewPeakMax, AvgGSRVal
    elif (retval == 2):
        return dict4[4.0][0]
    else:
        return [dict5][8.0][0]

def preprocessing():
    # this script is made to process raw GSR data in imotions files

    filestoeval = []
    filestoeval1 = []

    for root, dirs, filenames in os.walk(Folder1):
        for file in filenames:
            if (file == ".DS_Store"):
                continue
            try:
                stats = os.stat(Folder1 + "/" + file)
                if (int(stats.st_size) > 400000):
                    filestoeval.append(gatheringfiles(file))
                else:
                    print(file, stats.st_size)
            except FileNotFoundError:
                continue
    for root, dirs, filenames in os.walk(Folder):
        for file in filenames:
            if (file == ".DS_Store"):
                continue
            try:
                stats = os.stat(Folder + "/" + file)
                if (int(stats.st_size) > 400000):
                    filestoeval1.append(gatheringfiles(file))
                else:
                    print(file, stats.st_size)
            except FileNotFoundError:
                continue
    BaselineFiles = organizingfiles(filestoeval, Folder1)
    MTFiles = organizingfiles(filestoeval1, Folder)

    finallist = []

    x = 0
    y = 0
    while (len(MTFiles) > x and len(BaselineFiles) > y):
        if (MTFiles[x][1] < BaselineFiles[y][1]):
            finallist.append(MTFiles[x])
            x += 1
        elif (MTFiles[x][1] > BaselineFiles[y][1]):
            finallist.append(BaselineFiles[y])
            y += 1
        else:
            finallist.append(BaselineFiles[y])
            finallist.append(MTFiles[x])
            x += 1
            y += 1
    if (y != len(BaselineFiles)):
        for x in range(y, len(BaselineFiles)):
            finallist.append(BaselineFiles[x])
    elif (x != len(MTFiles)):
        for z in range(x, len(MTFiles)):
            finallist.append(MTFiles[z])
    realFinalList = []
    q = 0

    while (q < len(finallist)):
        g = 0
        list3 = [finallist[q][1], "", "", "", "", "", ""]
        while ((q + g < len(finallist)) and finallist[q + g][1] == finallist[q][1]):
            for m in range(2, len(finallist[q + g])):
                list3 = intoPrintFormat(finallist[q + g][m], list3, finallist[q + g][0], finallist[q + g][1])
            g += 1
        q = q + g
        realFinalList.append(list3)
    realFinalList.insert(0, ["ParticipantID", "Group", "Baseline_PRE", "Baseline_Post", "Baseline_FU", "MIST_PRE", "MIST_POST", "MIST_FU"])

    savingdata(1, NewFilePath, realFinalList)
