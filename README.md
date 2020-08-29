# GSRProcessingPipelineSPSS
Galvanic Skin Response processing pipeline designed for eventual analysis with SPSS statistics software. 

------------------------------------------------------------------------------------------------------------------------------------------------------

Overview: 

This data analysis pipeline was developed for the UCSF Neuroscape lab. The Pipeline processes raw iMotions Galvanic Skin Response data into metrics about the GSR data. These metrics are formatted and saved into a .csv file that can be directly inputted into IBM's SPSS Statistical Analysis software. This software uses the metrics in the .csv to generate various statistics that can be extrapolated to either support or refute the hypothesis and goal of a research study. 

-------------------------------------------------------------------------------------------------------------------------------------------------------

Pipeline High Level Methodology: 

Note - for in depth explanation of program methodology and features, please read documentation in pipeline itself. This description provides a very basic understanding of what is happening in the program. 

1) organizes raw files to be analyzed in a way that creates a processed file which is compatible with SPSS software. Organization method also pairs pre, post, and follow up data for a participant together so metrics can be analyzed in way that is significant to research study. 
- for duplicate files, feature to only process the correct file 
- feature to automatically filter out files that do not have enough data to process accurate metrics
2) extracts data from raw iMotions file into a new format that allows analysis of data
3) implements mean filter to eliminate tonic GSR signal and drift. Generates phasic GSR signal 
2) implements low-pass filter to eliminate high frequency noise
3) implements peak detection algorithm with amplitude and artifact filters; peaks with miniscule amplitudes and/or arifacts are discarded 
4) optional feature to visualize phasic GSR data before and after filters are implemented to check if data is accurate
5) calculates all metrics described in "what the pipeline does" section below using the peak and phasic GSR signal data
6) optional feature to print metrics for the user before data is saved; purpose is to visually check if data is accurate 
7) saves the chosen metric for all files in a .csv for further analysis with the SPSS software 

--------------------------------------------------------------------------------------------------------------------------------------------------------

What the pipeline does: 

Note - for all the following metrics, all GSR peak values are reported in the microsiemens unit. All timestamp values are reported in milli-seconds.

1. takes in input of a folder containing raw iMotions Galvanic Skin Response data files
2. processes each file, reporting one of the following metrics in a processed file (user of script decides which metric is reported in .csv):
- number of phasic GSR peaks across entire time series in a file 
- number of GSR peaks in every 20 second range for entire time series (excluding first and last four seconds; common practice to exclude data at beginning and end of file for biometric data analysis for scientific studies)
- average phasic GSR value across entire time series in a file 
- average phasic GSR value in every 20 second range for entire time series (excluding first and last four seconds; common practice to exclude data at beginning and end of file for biometric data analysis for scientific studies)
- average value of peak amplitude across entire time series in a file 
3. The processed .csv files can be inputted directly into the SPSS software to generate statistics about the GSR data from pre -> post -> followup for all participants in a research study, which will indicate whether the research study hypothesis is supported or not. 

--------------------------------------------------------------------------------------------------------------------------------------------------------

How to use this pipeline: 

Note - ensure you have python 3.7 or greater installed in your text editor/IDE with the following packages: Matplotlib, Scipy, Csv, Numpy, Os, and Math.

1) Download the .py file and open in appropriate text editor/IDE. Program was created in pyCharm and Jupyter Notebooks; running the script in either of these IDE's would allow for the least errors while setting up.
2) at the top of the script, edit the 'Folder', 'Folder1', and 'NewFilePath' variables to the directory of the following:
- for 'Folder', edit to the directory where experimental group GSR data is stored
- for 'Folder1', edit to the directory where control group GSR data is stored 
- for 'NewFilePath', edit to the directory where you would like the processed GSR metrics to be stored
3) ensure the GSR files are of type .txt; if they are of any other type, convert them to type .txt before using this script
4) Run the preprocessing() function to process all the raw GSR data to the metrics denoted above the divider (-------); processed data for every file will be stored in a new .csv file at the directory you specified through the 'NewFilePath' variable
5) import this .csv file into SPSS to generate statistics on the data, and see whether the hypothesis of your research study is supported or refuted from the GSR data!
