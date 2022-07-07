# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 12:48:05 2022

@author: Dakota
"""

#%% Import dependencies
import sys
import re  #for word processing
import pandas as pd    #for data loading and manipulation
import os #for access folder
import numpy as np   #for calculaiton
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplcursors
import dill
# from openpyxl import load_workbook
from datetime import datetime
from collections import defaultdict
Tree= lambda: defaultdict(Tree)
from PyQt5 import QtCore, QtGui, QtWidgets  #QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from medpc2excel.medpc_read import medpc_read


#%% predefine custom classes


#%% Utilities Class
class explore:
    def __init__ (self, target_dir, *extension, kernalmsg = True):
        self.rootdir = target_dir
        self.ext = tuple(extension)
        self.p = kernalmsg
        self.get_dir_list(display=False)
        
    def get_dir_list (self, date_range = (), display = True):
        #ext = tuple (extension)
        if len(date_range) > 0:
            if len(date_range) == 2:
                start, end = date_range
                if self.p:
                    print ('getting files between %s to %s'%(start, end))
            elif len(date_range) == 1:
                start = date_range[0]
                end = start
                if self.p:
                    print ('getting file on %s'%(start))
        
        else:
            if self.p:
                print ('Scanning all files')
            start = 0
            end = np.inf
        
        allFile_l = []    
        for subdir, dirs, files in os.walk(self.rootdir):
            for file in files:
                #if file is *.txt file
                pat = ".*\.txt"
                if re.match(pat,file):
                    if file.split('.')[0] >= str(start) and file.split('.')[0] <= str(end):
                        allFile_l.append(os.path.join(subdir,file))
                #if file has no extension
                if not re.match(".*\..*", file):
                    if file.split('_')[0] >= str(start) and file.split('_')[0] <= str(end):
                        allFile_l.append(os.path.join(subdir,file))
        
        if display:
            if self.p:
                print ('Found %s %s files'%(len(allFile_l),self.ext))

        self.allFile_l = allFile_l
        return allFile_l
        
    def head(self, n = 5):
        #num_files = len(self.allFile_l)
        count= 0
        for num, f in enumerate (self.allFile_l, 1):
            if self.p:
                print (num,":",re.split('\\\\',f)[-2]+'\\'+re.split('\\\\',f)[-1])
            count += 1
            if count == n:
                break
        return 

#%% manually call medpc_read function without gui


# _, func_out = medpc_read(f, working_var_label, skipold = skipexist, override = replace_file, replace = replace_data, log = func_out) #pass TS_df_tree to an anonymous variable

# 
# datafolder= path to folder containing data files and .mpc files
datafolder = r'C:\Users\Dakota\Desktop\_mpc2excel_test'


# f = path to a specific file for testing
# f= r'C:\Users\Dakota\Desktop\_mpc2excel_test\2019-11-18_11h39m_Subject VP-VTA-FP08.txt'

#working_var_label = ? user input, I leave this blank
working_var_label= '' 

#- set override setting
override= 'Append' #'New'

if override == 'New':
    skipexist = True
    replace_file = True
    replace_data  = True
if override == 'Override':
    skipexist = False
    replace_file = True
    replace_data  = True
elif override == 'Replace':
    skipexist = False
    replace_file = False
    replace_data = True
elif override == 'Append':
    skipexist = False
    replace_file = False
    replace_data = False
   
    
#now can add breakpoint on function call for debugging without gui

#get path for all *. data file
files = explore(datafolder,*[''],kernalmsg=False)
#get a list of data file
datafile_list = files.get_dir_list(display=False)
func_out = ''

for n, f in enumerate(datafile_list):    
    _, func_out = medpc_read(f, working_var_label, skipold = skipexist, override = replace_file, replace = replace_data, log = func_out) #pass TS_df_tree to an anonymous variable
    print(n,f)
    print('log: '+func_out)
