###===============================================================
###              Import OS Module to Set Directory              ==
###===============================================================
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

###===============================================================
###   Provide Windows With A Different Application Identifier   ==
###===============================================================
try:
    import ctypes # Only exists on Windows.
    myappid = u'Enviva.fORCYS.Integration.version5' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
  pass

###===============================================================
###           Prevent another Instance of the Program           ==
###===============================================================
import win32event
import win32api
import sys
from winerror import ERROR_ALREADY_EXISTS
mutex = win32event.CreateMutex(None, False, 'forcysApp.pyw')
last_error = win32api.GetLastError()
if last_error == ERROR_ALREADY_EXISTS:
    sys.exit(0)

##===============================================================
##                  Check If VPN Is Connected                  ==
##===============================================================
from _utilities_ import WindowsNotify
from _cpu_ import vpn_connection_status, quickKill
if vpn_connection_status() == 'Disconnected':
    WindowsNotify()
    quickKill(processName=["pyw.exe", "pythonw.exe", "python.exe", ".py"], filePath='Skantitrikeristroklou60763')
    quickKill(processName=["pyw.exe", "pythonw.exe", "python.exe", ".py"], filePath='Vryonisyrnaoutsopoula94080')
    sys.exit()  

###================================================================
###                Import All Modules for Program                ==
###================================================================
import _SQL_
import os.path, pathlib
import shutil, subprocess, psutil
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter.filedialog import asksaveasfile
from pandastable import Table, TableModel, config
from PIL import ImageTk, Image
from tkcalendar import Calendar, DateEntry
import re, random, string
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import tempfile
import time
from win32api import *
from win32gui import *
import win32con
import struct
from itertools import count, cycle
import sqlite3
from sqlite3 import Error, IntegrityError
from _directory_ import findPath, full_path, remove_gen_pyPath
from _utilities_ import flatten_list, PhotoImage_GIF
from _cpu_ import startProcess, process_runningByPartialName
import _regex_

###===============================================================
###                         Image Lists                         ==
###===============================================================
List_LoginPageImages = []
List_HomePageImages=[]
List_DirectoryWatcherImages=[]
List_DataManagementImages=[]
List_ETLImages=[]


###===============================================================
###                     Home Page Functions                     ==
###===============================================================
##.............................................................
##  Home Page: Loading Screen Function for Directory Watcher   
##............................................................
def voyage_waiting():
    global root_voyageTracker_loading
    root_voyageTracker_loading = Toplevel()
    window_width = 480
    window_height = 100
    screen_width = root_voyageTracker_loading.winfo_screenwidth()
    screen_height = root_voyageTracker_loading.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2) - 200
    position_right = int(screen_width / 2 - window_width / 2) + 200
    root_voyageTracker_loading.geometry(
        f"{window_width}x{window_height}+{position_right}+{position_top}"
    )
    root_voyageTracker_loading.configure(background="#FFFFFF")
    root_voyageTracker_loading.resizable(False, False)
    root_voyageTracker_loading.overrideredirect(True)
    root_voyageTracker_loading.wait_visibility()
    root_voyageTracker_loading.grab_set()
    # Text
    waitLabel1 = Label(
        root_voyageTracker_loading,
        text="Please Wait",
        fg="#206DB4",
        bg="#FFFFFF",
        font=("Cascadia Code", 12),
        borderwidth=3,
        relief="raised",
    )
    waitLabel1.place(x=20, y=20)
    root_voyageTracker_loading.update_idletasks()
    root_voyageTracker_loading.update()
    # Function
    VoyageTrackerSwitch()
    # Kill Window
    root_voyageTracker_loading.destroy()
    
##.............................................................
##  Home Page: Loading Screen Function for Directory Watcher   
##............................................................
def shipping_waiting():
    global root_shippingPlan_loading
    root_shippingPlan_loading = Toplevel()
    window_width = 480
    window_height = 100
    screen_width = root_shippingPlan_loading.winfo_screenwidth()
    screen_height = root_shippingPlan_loading.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2) - 200
    position_right = int(screen_width / 2 - window_width / 2) + 200
    root_shippingPlan_loading.geometry(
        f"{window_width}x{window_height}+{position_right}+{position_top}"
    )
    root_shippingPlan_loading.configure(background="#FFFFFF")
    root_shippingPlan_loading.resizable(False, False)
    root_shippingPlan_loading.overrideredirect(True)
    root_shippingPlan_loading.wait_visibility()
    root_shippingPlan_loading.grab_set()
    # root_shippingPlan_loading.attributes('-topmost', 1)
    # Text
    waitLabel1 = Label(
        root_shippingPlan_loading,
        text="Please Wait",
        fg="#206DB4",
        bg="#FFFFFF",
        font=("Cascadia Code", 12),
        borderwidth=3,
        relief="raised",
    )
    waitLabel1.place(x=10, y=50)
    root_shippingPlan_loading.update_idletasks()
    root_shippingPlan_loading.update()
    # Function
    ShippingPlanSwitch()
    # Kill Window
    root_shippingPlan_loading.destroy()

##..............................................................
##  Home Page: Get Status of Directory Function   
##..............................................................
def directory_watch_switch_status(proc):
    """ Vryonisyrnaoutsopoula94080 or Skantitrikeristroklou60763 """

    if len(process_runningByPartialName(processName=['pyw.exe',
           'pythonw.exe', 'python.exe', '.py'], partial_name=proc)) \
        == 0:
        res = 'off'
    elif len(process_runningByPartialName(processName=['pyw.exe',
             'pythonw.exe', 'python.exe', '.py'], partial_name=proc)) \
        > 0:

        res = 'on'
    return res

##........................................................
##  Home Page: Status of Directory Switch   
##........................................................
dir_switch_status = {"on":True, "off":False}

##...............................................................................
##  Home Page: Is Task Currently Running and Is Widget Switch On   
##...............................................................................
is_voyage_tracker_switch_on = dir_switch_status[directory_watch_switch_status(proc = 'Vryonisyrnaoutsopoula94080')]
is_shipping_plan_switch_on = dir_switch_status[directory_watch_switch_status(proc = 'Skantitrikeristroklou60763')]


##...........................................
##  Home Page: View Financial Results Function   
##...........................................
def Compare_voyage_tracker_financials():
    check_cols = \
        list(pd.read_csv(findPath(base_path='R:/Depts/Sales-Marketing/SystemsNavigator_ShipNavApplication/VoyageTracker/bin'
             , isdir=False, name='_fin_cols_changes_.txt',
             listdir=False), header=None).iloc[:, 0])

  # Load Most Recent File

    new_file_name = endingFinancialText.get()
    NewFile = pd.read_excel([f for f in financial_reports_path
                            if new_file_name in f][0])[check_cols]

  # Add ID Column

    NewFile['ID'] = NewFile['General__Ship ID'].map(str) \
        + NewFile['General__Ship code'].map(str)

  # Load Previous File

    old_file_name = startingFinancialText.get()
    OldFile = pd.read_excel([f for f in financial_reports_path
                            if old_file_name in f][0])[check_cols]

  # Add ID Column

    OldFile['ID'] = OldFile['General__Ship ID'].map(str) \
        + OldFile['General__Ship code'].map(str)

  # Reorganize column names and bring ID to front

    col_names = NewFile.columns.tolist()[-1:] \
        + NewFile.columns.tolist()[:-1]

  # Assign re-organized columns to both datasets

    NewFile = NewFile[col_names]
    OldFile = OldFile[col_names]
    OldFile = OldFile[OldFile['ID'] != 'nannan']

  # Sort ID's

    NewFile = NewFile.sort_values('ID').reset_index(drop=True)
    OldFile = OldFile.sort_values('ID').reset_index(drop=True)

  # Identify duplicate IDs and add count

    check1 = NewFile['ID'].duplicated(keep=False)
    NewFile.loc[check1, 'ID'] += NewFile.groupby('ID'
            ).cumcount().add(1).astype(str)
    check2 = OldFile['ID'].duplicated(keep=False)
    OldFile.loc[check2, 'ID'] += OldFile.groupby('ID'
            ).cumcount().add(1).astype(str)

  # Get Column Change

    col_changes = [
        'ID',
        'General__Ship ID',
        'General__Name',
        'Demurrage load owner__Demurrage rate ($)',
        'Demurrage load owner__Demurrage or Despatch ($)',
        'Demurrage disch owner__Demurrage rate ($)',
        'Demurrage disch owner__Demurrage or Despatch ($)',
        'Demurrage load supplier__Demurrage rate ($)',
        'Demurrage load supplier__Demurrage or Despatch ($)',
        'Demurrage disch supplier__Demurrage rate ($)',
        'Demurrage disch supplier__Demurrage or Despatch ($)',
        'Demurrage disch customer__Demurrage rate ($)',
        'Demurrage disch customer__Demurrage or Despatch ($)',
        'Load DA owner__Balance ($)',
        'Disch DA owner__Balance ($)',
        'Load DA supplier__Balance ($)',
        'Disch DA supplier__Balance ($)',
        'Disch DA customer__Balance ($)',
        'DA total__DA loadport pickup ($/t)',
        'DA total__DA disport pickup ($/t)',
        'Bunker sea cargo__HFO or VLSFO consumed',
        'Bunker sea cargo__LSMGO consumed',
        'Freight invoice__Freight rate',
        'Freight invoice__Stowage',
        'Freight invoice__Bunker adj',
        'Freight invoice__Shipping adj',
        'Panama canal owner__Balance ($)',
        'Panama canal customer__Balance ($)',
        'Panama canal__ECT demurrage ($)',
        ]

  # Define DFs

    df1 = OldFile[col_changes]
    df2 = NewFile[col_changes]

  # Sort By Ship Code then delete column

    df1 = df1.sort_values(by='General__Ship ID')
Traceback (most recent call last):
  File "/usr/bin/pythontidy", line 9, in <module>
    load_entry_point('PythonTidy==1.21', 'console_scripts', 'pythontidy')()
  File "build/bdist.linux-x86_64/egg/runner.py", line 31, in main
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 4813, in tidy_up
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 3876, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 4343, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 3225, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 4343, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 2319, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 2563, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 3643, in put
AttributeError: Set instance has no attribute 'put'

##...........................................
##  Home Page: View Itinerary Results Function   .
##...........................................
def Compare_voyage_tracker_itinerary():

  # Gather Column Names to Check

    check_cols = \
        list(pd.read_csv(findPath(base_path='R:/Depts/Sales-Marketing/SystemsNavigator_ShipNavApplication/VoyageTracker/bin'
             , isdir=False, name='_itin_cols_.txt', listdir=False),
             header=None).iloc[:, 0])

  # Load Most Recent File

    new_file_name = endingItineraryText.get()
    newFile = pd.read_excel([f for f in itinerary_reports_path
                            if new_file_name in f][0])[check_cols]

  # Add ID Column

    newFile['ID'] = newFile['General__Ship ID'].map(str) \
        + newFile['General__Ship code'].map(str)

  # Load Previous File

    old_file_name = startingItineraryText.get()
    OldFile = pd.read_excel([f for f in itinerary_reports_path
                            if old_file_name in f][0])[check_cols]

  # Add ID Column

    OldFile['ID'] = OldFile['General__Ship ID'].map(str) \
        + OldFile['General__Ship code'].map(str)

  # Reorganize column names and bring ID to front

    col_names = newFile.columns.tolist()[-1:] \
        + newFile.columns.tolist()[:-1]

  # Assign re-organized columns to both datasets

    newFile = newFile[col_names]
    OldFile = OldFile[col_names]
    OldFile = OldFile[OldFile['ID'] != 'nannan']

  # Sort ID's

    newFile = newFile.sort_values('ID').reset_index(drop=True)
    OldFile = OldFile.sort_values('ID').reset_index(drop=True)

  # Identify duplicate IDs and add count

    check1 = newFile['ID'].duplicated(keep=False)
    newFile.loc[check1, 'ID'] += newFile.groupby('ID'
            ).cumcount().add(1).astype(str)
    check2 = OldFile['ID'].duplicated(keep=False)
    OldFile.loc[check2, 'ID'] += OldFile.groupby('ID'
            ).cumcount().add(1).astype(str)

  # Get Column Change

    df1 = OldFile[[
        'ID',
        'General__Ship ID',
        'General__Name',
        'General__Status',
        'General__Load port',
        'General__Discharge port',
        'General__Customer',
        'Itinerary__Within laycan',
        'Itinerary__Within arrival',
        'General__Start arrival window',
        'General__End arrival window',
        ]]
    df2 = newFile[[
        'ID',
        'General__Ship ID',
        'General__Name',
        'General__Status',
        'General__Load port',
        'General__Discharge port',
        'General__Customer',
        'Itinerary__Within laycan',
        'Itinerary__Within arrival',
        'General__Start arrival window',
        'General__End arrival window',
        ]]

  # Sort By Ship Code then delete column

    df1 = df1.sort_values(by='General__Ship ID')
Traceback (most recent call last):
  File "/usr/bin/pythontidy", line 9, in <module>
    load_entry_point('PythonTidy==1.21', 'console_scripts', 'pythontidy')()
  File "build/bdist.linux-x86_64/egg/runner.py", line 31, in main
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 4813, in tidy_up
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 3876, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 4343, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 3225, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 4343, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 2319, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 2563, in put
  File "build/bdist.linux-x86_64/egg/PythonTidy.py", line 3643, in put
AttributeError: Set instance has no attribute 'put'

##...........................................
##  Home Page: Export Results Function   .
##...........................................
def exportResults(selection):
    if selection == 'Financial':
        if startingFinancialText.get() == '' \
            or endingFinancialText.get() == '':
            error_message(msg='Values Cannot be Blank!')
        elif datetime.strptime(startingFinancialText.get().replace('.',
                               '-'), '%Y-%m-%d').date() \
            > datetime.strptime(endingFinancialText.get().replace('.',
                                '-'), '%Y-%m-%d').date():
            error_message(msg='Starting file date cannot be greater than ending file date!'
                          )
            startingFinancialText.set('')
            endingFinancialText.set('')
        elif datetime.strptime(startingFinancialText.get().replace('.',
                               '-'), '%Y-%m-%d').date() \
            == datetime.strptime(endingFinancialText.get().replace('.',
                                 '-'), '%Y-%m-%d').date():
            error_message(msg='Please choose files that are unique!')
            startingFinancialText.set('')
            endingFinancialText.set('')
        else:
            exportFile = Compare_voyage_tracker_financials()
            try:

        # with block automatically closes file

                with filedialog.asksaveasfile(mode='w',
                        defaultextension='.xlsx') as file:
                    exportFile.to_excel(file.name, index=False)
            except AttributeError:
                print 'The user cancelled save'
    elif selection == 'Itinerary':

        if startingItineraryText.get() == '' \
            or endingItineraryText.get() == '':
            error_message(msg='Values Cannot be Blank!')
        elif datetime.strptime(startingItineraryText.get().replace('.',
                               '-'), '%Y-%m-%d').date() \
            > datetime.strptime(endingItineraryText.get().replace('.',
                                '-'), '%Y-%m-%d').date():
            error_message(msg='Starting file date cannot be greater than ending file date!'
                          )
            startingItineraryText.set('')
            endingItineraryText.set('')
        elif datetime.strptime(startingItineraryText.get().replace('.',
                               '-'), '%Y-%m-%d').date() \
            == datetime.strptime(endingItineraryText.get().replace('.',
                                 '-'), '%Y-%m-%d').date():
            error_message(msg='Please choose files that are unique!')
            startingItineraryText.set('')
            endingItineraryText.set('')
        else:
            exportFile = Compare_voyage_tracker_itinerary()
            try:

        # with block automatically closes file

                with filedialog.asksaveasfile(mode='w',
                        defaultextension='.xlsx') as file:
                    exportFile.to_excel(file.name, index=False)
            except AttributeError:
                print 'The user cancelled save'

    


##...........................................
##  Home Page: View Results Function   .
##...........................................
def viewResults(selection):
    global root_comparison_results_view
    if selection == 'Financial':
        if startingFinancialText.get() == '' \
            or endingFinancialText.get() == '':
            error_message(msg='Values Cannot be Blank!')
        elif datetime.strptime(startingFinancialText.get().replace('.',
                               '-'), '%Y-%m-%d').date() \
            > datetime.strptime(endingFinancialText.get().replace('.',
                                '-'), '%Y-%m-%d').date():
            error_message(msg='Starting file date cannot be greater than ending file date!'
                          )
            startingFinancialText.set('')
            endingFinancialText.set('')
        elif datetime.strptime(startingFinancialText.get().replace('.',
                               '-'), '%Y-%m-%d').date() \
            == datetime.strptime(endingFinancialText.get().replace('.',
                                 '-'), '%Y-%m-%d').date():
            error_message(msg='Please choose files that are unique!')
            startingFinancialText.set('')
            endingFinancialText.set('')
        else:
            root_comparison_results_view = Toplevel()
            width = 1000
            height = 550
            screen_width = \
                root_comparison_results_view.winfo_screenwidth()
            screen_height = \
                root_comparison_results_view.winfo_screenheight()
            x = screen_width / 2 - width / 2
            y = screen_height / 2 - height / 2
            root_comparison_results_view.geometry('%dx%d+%d+%d'
                    % (width, height, x, y))
            root_comparison_results_view.configure(background='#FFFFFF')
            root_comparison_results_view.iconbitmap(findPath(base_path=pathlib.Path().resolve(),
                    isdir=False, name='logo3.ico', listdir=False))
            root_comparison_results_view.wait_visibility()
            root_comparison_results_view.grab_set()
            frame = Frame(root_comparison_results_view)
            frame.pack(fill='both', expand=True)
            root_comparison_results_view.title('Financial Comparison Results'
                    )
            pt = Table(parent=frame,
                       dataframe=Compare_voyage_tracker_financials(),
                       showtoolbar=False, showstatusbar=True,
                       editable=False)
            pt.show()
    elif selection == 'Itinerary':

        if startingItineraryText.get() == '' \
            or endingItineraryText.get() == '':
            error_message(msg='Values Cannot be Blank!')
        elif datetime.strptime(startingItineraryText.get().replace('.',
                               '-'), '%Y-%m-%d').date() \
            > datetime.strptime(endingItineraryText.get().replace('.',
                                '-'), '%Y-%m-%d').date():
            error_message(msg='Starting file date cannot be greater than ending file date!'
                          )
            startingItineraryText.set('')
            endingItineraryText.set('')
        elif datetime.strptime(startingItineraryText.get().replace('.',
                               '-'), '%Y-%m-%d').date() \
            == datetime.strptime(endingItineraryText.get().replace('.',
                                 '-'), '%Y-%m-%d').date():
            error_message(msg='Please choose files that are unique!')
            startingItineraryText.set('')
            endingItineraryText.set('')
        else:
            root_comparison_results_view = Toplevel()
            width = 1000
            height = 550
            screen_width = \
                root_comparison_results_view.winfo_screenwidth()
            screen_height = \
                root_comparison_results_view.winfo_screenheight()
            x = screen_width / 2 - width / 2
            y = screen_height / 2 - height / 2
            root_comparison_results_view.geometry('%dx%d+%d+%d'
                    % (width, height, x, y))
            root_comparison_results_view.configure(background='#FFFFFF')
            root_comparison_results_view.iconbitmap(findPath(base_path=pathlib.Path().resolve(),
                    isdir=False, name='logo3.ico', listdir=False))
            root_comparison_results_view.wait_visibility()
            root_comparison_results_view.grab_set()
            frame = Frame(root_comparison_results_view)
            frame.pack(fill='both', expand=True)
            root_comparison_results_view.title('Itinerary Comparison Results'
                    )
            pt = Table(parent=frame,
                       dataframe=Compare_voyage_tracker_itinerary(),
                       showtoolbar=False, showstatusbar=True,
                       editable=False)
            pt.show()

##....................................................................
##  Home Page: Retrieve Baltic Exhange Data from Database Function   .
##....................................................................
def sql_query_baltic_exchange_database():
  global BalticExhangeDataFrame
  try:
    if os.path.exists(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="shipping_index.db", listdir=False)) == True:
      df = _SQL_.SELECT(database="shipping_index.db", tableName="baltic_price", query= 'SELECT * FROM baltic_price WHERE symbol IN (SELECT symbol FROM baltic_exchange_indexes WHERE shipnav_active = "YES")').drop(labels={'ID'}, axis=1)
      df = df.replace(0, np.nan)
      df["date"] = pd.to_datetime(df['date']).apply(lambda x: x.date()) 
      df = df.pivot_table(index=["date"],  columns='symbol', values='price').reset_index(drop=False).rename_axis(None, axis=1)
      dateFrame = pd.DataFrame(pd.date_range(min(df["date"]), max(df["date"]))).rename(columns={0:"date"})
      dateFrame = pd.to_datetime(dateFrame['date']).apply(lambda x: x.date())
      df2 = pd.merge(dateFrame, df, on="date", how="left")
      DF = df2.fillna(method="ffill")
      DF = DF.rename(columns={"HS3_38":"BHSI HS3",	"HS4_38":"BHSI HS4",	"HS7TC":"BHSI 7TC",	"S10TC":"BSI 10TC",	"S1C_58":"BSI S1C",	"S2_58":"BSI S2",	"S4A_58":"BSI S4A"})
      BalticExhangeDataFrame = DF[["date","BHSI", "BHSI HS4", "BHSI HS3", "BHSI 7TC", "BSI", "BSI S4A", "BSI S1C", "BSI 10TC", "BSI S2"]]
    else:
      load_database(database = "Shipping_Indexes", database_name = "shipping_index.db")
      df = _SQL_.SELECT(database="shipping_index.db", tableName="baltic_price", query= 'SELECT * FROM baltic_price WHERE symbol IN (SELECT symbol FROM baltic_exchange_indexes WHERE shipnav_active = "YES")').drop(labels={'ID'}, axis=1)
      df = df.replace(0, np.nan)
      df["date"] = pd.to_datetime(df['date']).apply(lambda x: x.date()) 
      df = df.pivot_table(index=["date"],  columns='symbol', values='price').reset_index(drop=False).rename_axis(None, axis=1)
      dateFrame = pd.DataFrame(pd.date_range(min(df["date"]), max(df["date"]))).rename(columns={0:"date"})
      dateFrame = pd.to_datetime(dateFrame['date']).apply(lambda x: x.date())
      df2 = pd.merge(dateFrame, df, on="date", how="left")
      DF = df2.fillna(method="ffill")
      DF = DF.rename(columns={"HS3_38":"BHSI HS3",	"HS4_38":"BHSI HS4",	"HS7TC":"BHSI 7TC",	"S10TC":"BSI 10TC",	"S1C_58":"BSI S1C",	"S2_58":"BSI S2",	"S4A_58":"BSI S4A"})
      BalticExhangeDataFrame = DF[["date","BHSI", "BHSI HS4", "BHSI HS3", "BHSI 7TC", "BSI", "BSI S4A", "BSI S1C", "BSI 10TC", "BSI S2"]]
  except:
    load_database(database = "Shipping_Indexes", database_name = "shipping_index.db")
    df = _SQL_.SELECT(database="shipping_index.db", tableName="baltic_price", query= 'SELECT * FROM baltic_price WHERE symbol IN (SELECT symbol FROM baltic_exchange_indexes WHERE shipnav_active = "YES")').drop(labels={'ID'}, axis=1)
    df = df.replace(0, np.nan)
    df["date"] = pd.to_datetime(df['date']).apply(lambda x: x.date()) 
    df = df.pivot_table(index=["date"],  columns='symbol', values='price').reset_index(drop=False).rename_axis(None, axis=1)
    dateFrame = pd.DataFrame(pd.date_range(min(df["date"]), max(df["date"]))).rename(columns={0:"date"})
    dateFrame = pd.to_datetime(dateFrame['date']).apply(lambda x: x.date())
    df2 = pd.merge(dateFrame, df, on="date", how="left")
    DF = df2.fillna(method="ffill")
    DF = DF.rename(columns={"HS3_38":"BHSI HS3",	"HS4_38":"BHSI HS4",	"HS7TC":"BHSI 7TC",	"S10TC":"BSI 10TC",	"S1C_58":"BSI S1C",	"S2_58":"BSI S2",	"S4A_58":"BSI S4A"})
    BalticExhangeDataFrame = DF[["date","BHSI", "BHSI HS4", "BHSI HS3", "BHSI 7TC", "BSI", "BSI S4A", "BSI S1C", "BSI 10TC", "BSI S2"]]
  return BalticExhangeDataFrame

def Baltic_exportToExcel():
  try:
    # with block automatically closes file
    with filedialog.asksaveasfile(mode='w', defaultextension=".xlsx") as file:
      BalticExhangeDataFrame.to_excel(file.name, index=False)
  except AttributeError:
    # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
    print("The user cancelled save")
  root_baltic_download.destroy()

def baltic_download_waiting():
  global root_baltic_download
  root_baltic_download = Toplevel()
  window_width = 480
  window_height = 100
  screen_width = root_baltic_download.winfo_screenwidth()
  screen_height = root_baltic_download.winfo_screenheight()
  position_top = int(screen_height / 2 - window_height / 2)-200
  position_right = int(screen_width / 2 - window_width / 2)+200
  root_baltic_download.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
  root_baltic_download.configure(background='#FFFFFF')
  root_baltic_download.resizable(False, False)
  root_baltic_download.overrideredirect(True)
  root_baltic_download.wait_visibility()
  root_baltic_download.grab_set()
  # root_baltic_download.attributes('-topmost', 1)
  # Text 
  waitLabel1 = Label(root_baltic_download, text='Downloading Baltic Report', fg="#206DB4", bg="#FFFFFF", font=("Cascadia Code", 12), borderwidth=3, relief="raised") 
  waitLabel1.place(x=20, y=20)
  root_baltic_download.update_idletasks()
  root_baltic_download.update()
  # Function
  sql_query_baltic_exchange_database()
  # Kill Window 
  root_baltic_download.after(0000, lambda: Baltic_exportToExcel())


  
##.................................
##  Home Page: Log Out Function   .
##.................................
def home_logging_out():
  global root_logout
  root_logout = Toplevel()
  window_width = 480
  window_height = 100
  screen_width = root_logout.winfo_screenwidth()
  screen_height = root_logout.winfo_screenheight()
  position_top = int(screen_height / 2 - window_height / 2) -200
  position_right = int(screen_width / 2 - window_width / 2) + 200
  root_logout.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
  root_logout.configure(background='#FFFFFF')
  root_logout.resizable(False, False)
  root_logout.overrideredirect(True)
  root_logout.wait_visibility()
  root_logout.grab_set()
  log_outLabel1 = Label(root_logout, text='You Have Been Successfully Logged Out!', fg="#206DB4", bg='#FFFFFF', font=("Cascadia Code", 15), borderwidth=3, relief="raised") 
  log_outLabel1.place(x=10, y=50)
  root_logout.after(1500, Login_Screen)



###===============================================================
###                   Database Page Functions                   ==
###===============================================================
##..................................................
##  Database Page: Error Message Window Function   .
##..................................................
def error_message(msg):
  global root_error
  root_error = Toplevel()
  window_width = 350 + (len(msg)*3)
  window_height = 150
  screen_width = root_error.winfo_screenwidth()
  screen_height = root_error.winfo_screenheight()
  position_top = int(screen_height / 4 - window_height / 4)
  position_right = int(screen_width / 2 - window_width / 2)
  root_error.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
  root_error.title('Error!')
  root_error.iconbitmap(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logo3.ico", listdir=False))
  root_error.configure(background='red')
  root_error.resizable(False, False)
  root_error.wait_visibility()
  root_error.grab_set()
  label = Label(root_error, text=msg, fg="#FFFFFF", bg='red', font=("Cascadia Code", 10, 'bold'))
  label.place(x=10, y=50)
  #root_error.after(2000, lambda: root_error.destroy())


##...............................................................................
##  Database Page: Adding New Values - Clear All Entries After Database Insert  .
##...............................................................................
def clear_all_entries(function):
    if function == 'AddValues':
        AddValues_port_name_entry.config(state='normal')
        AddValues_port_name_text.set('')
        port_approve_button.config(state='normal')

        AddValues_plant_name_text.set('')
        AddValues_plant_name_entry.config(state='disabled')
        plant_approve_button.config(state='disabled')

        AddValues_date_text.set('')
        AddValues_date_entry.config(state='disabled')
        date_approve_button.config(state='disabled')

        AddValues_arrivals_text.set('')
        AddValues_arrivals_entry.config(state='disabled')
        arrivals_approve_button.config(state='disabled')
    elif function == 'AddPort':

        AddPort_port_name_entry.config(state='normal')
        AddPort_port_name_text.set('')
        new_port_approve_button.config(state='normal')
    elif function == 'AddPlant':

        AddPlant_port_name_entry.config(state='normal')
        AddPlant_port_name_text.set('')
        choose_port_approve_button.config(state='normal')

        AddPlant_plant_name_text.set('')
        AddPlant_plant_name_entry.config(state='disabled')
        new_plant_approve_button.config(state='disabled')
    else:
        pass

##.......................................................
##  Database Page: Step 1 When Page Button Is Clicked   .
##.......................................................
def CreateSQLTableValues(function):
    global inventory_table_insert_values
    global ports_table_insert_values
    global plants_table_insert_values
    if function is None:
        pass
    elif function == 'AddValues':
        inventory_table_insert_values = pd.DataFrame()
        inventory_table_insert_values = pd.DataFrame(columns=[
            'ID',
            'date',
            'port',
            'plant',
            'arrivals_into_port',
            'barge_load',
            'shrinkage_overage',
            'inventory_adj',
            'waste_adj',
            ])
    elif function == 'AddPort':
        ports_table_insert_values = pd.DataFrame()
        ports_table_insert_values = pd.DataFrame(columns=['port'])
    elif function == 'AddPlant':
        plants_table_insert_values = pd.DataFrame()
        plants_table_insert_values = pd.DataFrame(columns=['port',
                'plant'])
    else:
        pass



##................................................................
##  Database Page: Step 2 Collect Data When Insert Is Pressed  .
##................................................................
def databaseDataCollect(function):
    global inventory_table_insert_values
    global ports_table_insert_values
    global plants_table_insert_values

    if function == 'AddValues':
        if '' in inventory_table_insert_values['ID'].values.tolist() \
            or '' in inventory_table_insert_values['date'
                ].values.tolist() or '' \
            in inventory_table_insert_values['port'].values.tolist() \
            or '' in inventory_table_insert_values['plant'
                ].values.tolist() or '' \
            in inventory_table_insert_values['arrivals_into_port'
                ].values.tolist():
            error_message(msg='Values Missing!')
            clear_all_entries(function='AddValues')
        elif AddValues_date_entry['state'] == 'normal' \
            or AddValues_arrivals_entry['state'] == 'normal' \
            or AddValues_plant_name_entry['state'] == 'normal' \
            or AddValues_port_name_entry['state'] == 'normal':
            error_message(msg='All Entries Must Be Approved!')
            clear_all_entries(function='AddValues')
        elif AddValues_date_text.get() == '' \
            or AddValues_port_name_text.get() == '' \
            or AddValues_plant_name_text.get() == '' \
            or AddValues_arrivals_text.get() == '':
            error_message(msg='All Entries Must Have A Value and Must Be Approved!'
                          )
            clear_all_entries(function='AddValues')
        elif datetime.strptime(AddValues_date_text.get().strip(),
                               '%Y-%m-%d').strftime('%Y%m%d') \
            + AddValues_port_name_text.get() \
            + AddValues_plant_name_text.get() \
            in _SQL_.SELECT_ALL(database=findPath(base_path=pathlib.Path().resolve(),
                                isdir=False, name='inventory.db',
                                listdir=False), tableName='inventory'
                                )['ID'].values.tolist():
            error_message(msg='Value for ID Already Exists!')
            clear_all_entries(function='AddValues')
        elif len([f for f in inventory_table_insert_values['ID'
                 ].values.tolist() if f
                 in _SQL_.SELECT_ALL(database=findPath(base_path=pathlib.Path().resolve(),
                 isdir=False, name='inventory.db', listdir=False),
                 tableName='inventory')['ID'].values.tolist()]) > 0:
            error_message(msg='Value for ID Already Exists!')
            clear_all_entries(function='AddValues')
        elif datetime.strptime(AddValues_date_text.get().strip(),
                               '%Y-%m-%d').strftime('%Y%m%d') \
            + AddValues_port_name_text.get() \
            + AddValues_plant_name_text.get() \
            in inventory_table_insert_values['ID'].values.tolist():
            error_message(msg='You Have Already Entered a Value for This ID!'
                          )
            clear_all_entries(function='AddValues')
        else:
            insert1 = {
                'ID': datetime.strptime(AddValues_date_text.get().strip(),
                        '%Y-%m-%d').strftime('%Y%m%d') \
                    + AddValues_port_name_text.get() \
                    + AddValues_plant_name_text.get(),
                'date': datetime.strptime(AddValues_date_text.get().strip(),
                        '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S'),
                'port': AddValues_port_name_text.get(),
                'plant': AddValues_plant_name_text.get(),
                'arrivals_into_port': float(AddValues_arrivals_text.get().strip().replace(','
                        , '')),
                'barge_load': None,
                'shrinkage_overage': None,
                'inventory_adj': None,
                'waste_adj': None,
                }
            inventory_table_insert_values = \
                inventory_table_insert_values.append(insert1,
                    ignore_index=True)
            clear_all_entries(function='AddValues')
            databaseAdd_Values_SaveChanges_Button.place(x=530, y=380)
    elif function == 'AddPort':

        if AddPort_port_name_text.get() == '':
            error_message(msg='No Values to Insert!')
            clear_all_entries(function='AddPort')
        elif AddPort_port_name_text.get() \
            in flatten_list(_SQL_.SELECT_ALL(database=findPath(base_path=pathlib.Path().resolve(),
                            isdir=False, name='inventory.db',
                            listdir=False), tableName='ports'
                            ).values.tolist()) == True:
            error_message(msg='Port Already Exists!')
            clear_all_entries(function='AddPort')
        elif AddPort_port_name_entry['state'] == 'normal':
            error_message(msg='All Entries Must Be Approved!')
            clear_all_entries(function='AddPort')
        else:
            insert2 = {'port': AddPort_port_name_text.get()}
            ports_table_insert_values = \
                ports_table_insert_values.append(insert2,
                    ignore_index=True)
            clear_all_entries(function='AddPort')
            databaseAdd_Port_SaveChanges_Button.place(x=530, y=380)
    elif function == 'AddPlant':

        if AddPlant_plant_name_text.get() == '' \
            or AddPlant_port_name_text.get() == '':
            error_message(msg='No Values to Insert!')
            clear_all_entries(function='AddPlant')
        elif [AddPlant_plant_name_text.get(),
              AddPlant_port_name_text.get()] \
            in _SQL_.SELECT_ALL(database=findPath(base_path=pathlib.Path().resolve(),
                                isdir=False, name='inventory.db',
                                listdir=False), tableName='plants'
                                ).values.tolist() == True:
            error_message(msg='Plant Already Exists!')
            clear_all_entries(function='AddPlant')
        elif [AddPlant_plant_name_text.get(),
              AddPlant_port_name_text.get()] \
            in plants_table_insert_values.values.tolist() == True:

            error_message(msg='You Have Already Entered this Combination!'
                          )
            clear_all_entries(function='AddPlant')
        elif AddPlant_plant_name_entry['state'] == 'normal' \
            or AddPlant_port_name_entry['state'] == 'normal':

            error_message(msg='All Entries Must Be Approved!')
            clear_all_entries(function='AddPlant')
        else:
            insert3 = {'port': AddPlant_port_name_text.get(),
                       'plant': AddPlant_plant_name_text.get()}
            plants_table_insert_values = \
                plants_table_insert_values.append(insert3,
                    ignore_index=True)
            clear_all_entries(function='AddPlant')
            databaseAdd_Plant_SaveChanges_Button.place(x=530, y=380)

      

##.......................................................
##  Database Page: Load Database Function   .
##.......................................................
def database_loading(db_location_folder, db_name):
    global root_database_loading
    global database_last_modified
    root_database_loading = Toplevel()
    window_width = 350
    window_height = 100
    screen_width = root_database_loading.winfo_screenwidth()
    screen_height = root_database_loading.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root_database_loading.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    root_database_loading.configure(background='black')
    root_database_loading.resizable(False, False)
    root_database_loading.overrideredirect(True)
    root_database_loading.wait_visibility()
    root_database_loading.grab_set()

  # Text

    waitLabel1 = Label(
        root_database_loading,
        text='Please Wait',
        fg='#FFFFFF',
        bg='red',
        font=('Cascadia Code', 10),
        borderwidth=3,
        relief='raised',
        )
    waitLabel1.place(x=20, y=50)
    root_database_loading.update_idletasks()
    root_database_loading.update()

  # Function

    try:
        if os.path.exists(findPath(base_path=pathlib.Path().resolve(),
                          isdir=False, name=db_name, listdir=False)) \
            == True:
            database_last_modified = \
                time.ctime(os.path.getmtime(findPath(base_path=pathlib.Path().resolve(),
                           isdir=False, name=db_name, listdir=False)))
        else:
            load_database(database=db_location_folder,
                          database_name=db_name)
            database_last_modified = \
                time.ctime(os.path.getmtime(findPath(base_path=pathlib.Path().resolve(),
                           isdir=False, name=db_name, listdir=False)))
    except:
        load_database(database=db_location_folder,
                      database_name=db_name)
        database_last_modified = \
            time.ctime(os.path.getmtime(findPath(base_path=pathlib.Path().resolve(),
                       isdir=False, name=db_name, listdir=False)))

  # Bring Database View

    Database_Screen()

##....................................................
##  Database Page: Successful Admin Login Function   .
##....................................................
# If Login Successful


def data_management_login_status():
    if os.getlogin().lower() == 'cedric.moore':

    # If Login Successful

        database_loading(db_location_folder='Inventory',
                         db_name='inventory.db')
    else:
        root_admin.destroy()


##............................................
##  Database Page: Log Out Window Function   .
##............................................

def database_logging_out():
    global root_database_logout
    root_database_logout = Toplevel()
    window_width = 480
    window_height = 100
    screen_width = root_database_logout.winfo_screenwidth()
    screen_height = root_database_logout.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2) - 100
    position_right = int(screen_width / 2 - window_width / 2) + 30
    root_database_logout.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    root_database_logout.configure(background='#FFFFFF')
    root_database_logout.resizable(False, False)
    root_database_logout.overrideredirect(True)
    root_database_logout.wait_visibility()
    root_database_logout.grab_set()
    log_outLabel1 = Label(
        root_database_logout,
        text='You Have Been Successfully Logged Out!',
        fg='#206DB4',
        bg='#FFFFFF',
        font=('Cascadia Code', 15),
        borderwidth=3,
        relief='raised',
        )
    log_outLabel1.place(x=10, y=50)
    root_database_logout.after(1500, Login_Screen)

##................................................................................
##  Database Page: Adding New Values - Change Menu Options for Plants Function   .
##................................................................................
def change_plant_list(dropdown, var):
  selected_port_df = _SQL_.SELECT_ALL(database=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="inventory.db", listdir=False), tableName="plants")
  plants = tuple(selected_port_df[selected_port_df["port_name"] == AddValues_port_name_text.get()].iloc[:, 0])
  menu = dropdown['menu']
  menu.delete(0, 'end')
  for plant in plants:
    # Add menu items.
    menu.add_command(label=plant, command=lambda plant=plant: var.set(plant))
  var.set("")


##.........................................................................
##  Database Page: View Database - Window that Shows Selected Database    .
##.........................................................................
def Database_View(databaseName, table_Name):
  try:
    root_database_loading.destroy()
  except:
    pass
  global root_database_view
  root_database_view = Toplevel()
  width = 1000 
  height = 550 
  screen_width = root_database_view.winfo_screenwidth()  
  screen_height = root_database_view.winfo_screenheight() 
  x = (screen_width/2) - (width/2)
  y = (screen_height/2) - (height/2)
  root_database_view.geometry('%dx%d+%d+%d' % (width, height, x, y))
  root_database_view.title(databaseName.split(".")[0].capitalize() + " Database")
  root_database_view.configure(background='#FFFFFF')
  root_database_view.iconbitmap(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logo3.ico", listdir=False))
  root_database_view.wait_visibility()
  root_database_view.grab_set()
  frame = Frame(root_database_view)
  frame.pack(fill='both', expand=True)
  df = _SQL_.SELECT_ALL(database=findPath(base_path=pathlib.Path().resolve(), isdir=False, name=databaseName, listdir=False), tableName=table_Name)
  df['date'] = pd.to_datetime(df['date']).apply(lambda x: x.date())
  pt = Table(parent=frame, dataframe=df, showtoolbar=False, showstatusbar=True, editable=False)
  pt.show()

##...............................................................................
##  Database Page: Approve Database Entry Button Function   .
##...............................................................................
def approve_entry(which, function): # When Approve Button is Pressed
  if function == "AddValues":
    if which == "Port":
      if AddValues_port_name_text.get() == "":
        return error_message(msg="Please Select a Port Before Continuing")
      else:
        change_plant_list(dropdown = AddValues_plant_name_entry, var = AddValues_plant_name_text)
        AddValues_port_name_entry.config(state="disabled")
        port_approve_button.config(state= "disabled")
        AddValues_plant_name_entry.config(state="normal")
        plant_approve_button.config(state= "normal")
        AddValues_date_entry.config(state="disabled")
        AddValues_arrivals_entry.config(state="disabled")
    elif which == "Plant":
      if AddValues_plant_name_text.get() == "":
        return error_message(msg="Please Select a Plant Before Continuing")
      else:
        AddValues_plant_name_entry.config(state="disabled")
        plant_approve_button.config(state= "disabled")
        AddValues_date_entry.config(state="normal")
        date_approve_button.config(state= "normal")
    elif which == "Date":
      if AddValues_date_text.get().strip() == "":
        return error_message(msg="Please Select a Date Before Continuing")
      elif re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", re.IGNORECASE).match(AddValues_date_text.get().strip()) is None:
        return error_message(msg="Date Should Be in YYYY-MM-DD Format")
        AddValues_date_text.set("")
      else:
        AddValues_date_entry.config(state="disabled")
        date_approve_button.config(state= "disabled")
        AddValues_arrivals_entry.config(state="normal")
        arrivals_approve_button.config(state= "normal")
    elif which == "Arrivals":
      if AddValues_arrivals_text.get().replace(",", "") == "":
        return error_message(msg="Please Enter a Value Before Continuing")
        AddValues_arrivals_text.set("")
      elif _regex_.containsAnyAlpha(AddValues_arrivals_text.get().strip().replace(",", "")) == True:
        return error_message(msg="Port Arrival Values Cannot Contain Letters")
        AddValues_arrivals_text.set("")
      else:
        AddValues_arrivals_entry.config(state="disabled")
        arrivals_approve_button.config(state= "disabled")
    else:
      pass
    
  elif (function == "AddPort") and (which is None):
    if AddPort_port_name_text.get() == "":
      return error_message(msg="Please Enter a Port Name Before Continuing")
    else:
      AddPort_port_name_entry.config(state="disabled")
      new_port_approve_button.config(state= "disabled")
      
  elif function == "AddPlant":
    if which == "Port":
      if AddPlant_port_name_text.get() == "":
        return error_message(msg="Please Select a Port Before Continuing")
      else:
        AddPlant_port_name_entry.config(state="disabled")
        choose_port_approve_button.config(state= "disabled")
        AddPlant_plant_name_entry.config(state="normal")
        new_plant_approve_button.config(state= "normal")

    elif which == "Plant":
      if AddPlant_plant_name_text.get() == "":
        return error_message(msg="Please Enter a Plant Name Before Continuing")
      else:
        AddPlant_plant_name_entry.config(state="disabled")
        new_plant_approve_button.config(state= "disabled")
    else:
      pass
  else:
    pass


##.......................................................
##  Database Page: Inventory Table Insert  .
##.......................................................
def INSERT_INTO_INVENTORY_ALL():
  global inventory_table_insert_values
  global root_inventory_insert
  root_inventory_insert = Toplevel()
  window_width = 480
  window_height = 100
  screen_width = root_inventory_insert.winfo_screenwidth()
  screen_height = root_inventory_insert.winfo_screenheight()
  position_top = int(screen_height / 2 - window_height / 2)-100
  position_right = int(screen_width / 2 - window_width / 2)+30
  root_inventory_insert.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
  root_inventory_insert.configure(background='#FFFFFF')
  root_inventory_insert.resizable(False, False)
  root_inventory_insert.overrideredirect(True)
  root_inventory_insert.wait_visibility()
  root_inventory_insert.grab_set()
  # Text 
  waitLabel1 = Label(root_inventory_insert, text='Please Wait', fg="#206DB4", bg='#FFFFFF', font=("Cascadia Code", 15), borderwidth=3, relief="raised")
  waitLabel1.place(x=10, y=50)
  root_inventory_insert.update_idletasks()
  root_inventory_insert.update()
  # Function
  if not inventory_table_insert_values.empty:
    _SQL_.INSERT(
      database = findPath(base_path=pathlib.Path().resolve(), isdir=False, name="inventory.db", listdir=False), 
      sqlTable="inventory", 
      sqlColumns=inventory_table_insert_values.columns.values.tolist(), 
      values=inventory_table_insert_values
      )
    CreateSQLTableValues(function="AddValues")
  else:
    error_message(msg="No Values to Insert!")
  # Kill Window
  root_inventory_insert.destroy()
  

##.......................................................
##  Database Page: Port Table Insert  .
##.......................................................
def INSERT_INTO_PORT():
  global ports_table_insert_values
  global root_port_insert
  root_port_insert = Toplevel()
  window_width = 480
  window_height = 100
  screen_width = root_port_insert.winfo_screenwidth()
  screen_height = root_port_insert.winfo_screenheight()
  position_top = int(screen_height / 2 - window_height / 2)-100
  position_right = int(screen_width / 2 - window_width / 2)+30
  root_port_insert.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
  root_port_insert.configure(background='#FFFFFF')
  root_port_insert.resizable(False, False)
  root_port_insert.overrideredirect(True)
  root_port_insert.wait_visibility()
  root_port_insert.grab_set()
  # Text 
  waitLabel1 = Label(root_port_insert, text='Please Wait', fg="#206DB4", bg='#FFFFFF', font=("Cascadia Code", 15), borderwidth=3, relief="raised")
  waitLabel1.place(x=10, y=50)
  root_port_insert.update_idletasks()
  root_port_insert.update()
  # Function
  if not ports_table_insert_values.empty:
    _SQL_.INSERT(
      database = findPath(base_path=pathlib.Path().resolve(), isdir=False, name="inventory.db", listdir=False), 
      sqlTable="ports", 
      sqlColumns=ports_table_insert_values.columns.values.tolist(), 
      values=ports_table_insert_values
      )
    CreateSQLTableValues(function="AddPort")
  else:
    error_message(msg="No Values to Insert!")
  # Kill Window
  root_port_insert.destroy()
    

##.......................................................
##  Database Page: Plant Table Insert  .
##.......................................................
def INSERT_INTO_PLANT():
  global ports_table_insert_values
  global root_plant_insert
  root_plant_insert = Toplevel()
  window_width = 480
  window_height = 100
  screen_width = root_plant_insert.winfo_screenwidth()
  screen_height = root_plant_insert.winfo_screenheight()
  position_top = int(screen_height / 2 - window_height / 2)-100
  position_right = int(screen_width / 2 - window_width / 2)+30
  root_plant_insert.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
  root_plant_insert.configure(background='#FFFFFF')
  root_plant_insert.resizable(False, False)
  root_plant_insert.overrideredirect(True)
  root_plant_insert.wait_visibility()
  root_plant_insert.grab_set()
  # Text 
  waitLabel1 = Label(root_plant_insert, text='Please Wait', fg="#206DB4", bg='#FFFFFF', font=("Cascadia Code", 15), borderwidth=3, relief="raised")
  waitLabel1.place(x=10, y=50)
  root_plant_insert.update_idletasks()
  root_plant_insert.update()
  # Function
  if not plants_table_insert_values.empty:
    _SQL_.INSERT(
      database = findPath(base_path=pathlib.Path().resolve(), isdir=False, name="inventory.db", listdir=False), 
      sqlTable="plants", 
      sqlColumns=plants_table_insert_values.columns.values.tolist(), 
      values=plants_table_insert_values
      )
    CreateSQLTableValues(function="AddPlant")
  else:
    error_message(msg="No Values to Insert!")
  # Kill Window
  root_plant_insert.destroy()
















###===============================================================
###                    Login Page Functions                     ==
###===============================================================

##.........................................................
##  Login Page: Send Email for Requesting Access Function .
##.........................................................
def Send_Outlook(reason, recipients, root):
  if _regex_.isEnviva(email_string = emailEntry_Text.get()) == False:
    AttnLabel = Label(root_request_access, text='Please Enter A Valid Enviva Email Address!', fg="red", bg='#272A37', font=("Cascadia Code", 10, 'bold'))
    AttnLabel.place(x=25, y=25)
    AttnLabel.after(3000, lambda: AttnLabel.destroy())
    
  if len(businessReasonEntry_Text.get()) < 4:
    AttnLabel2 = Label(root_request_access, text='Please Enter A Valid Business Reason!', fg="red", bg='#272A37', font=("Cascadia Code", 10, 'bold'))
    AttnLabel2.place(x=25, y=130)
    AttnLabel2.after(3000, lambda: AttnLabel2.destroy())
    
  if (_regex_.isEnviva(email_string = emailEntry_Text.get()) == True) and (len(businessReasonEntry_Text.get()) > 4):
    import win32com.client as win32
    subject = "fORCYS App Request"
    body = reason
    #Create and send email
    olMailItem = 0x0
    obj = win32.gencache.EnsureDispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = subject
    newMail.HTMLBody = body 
    newMail.To = recipients
    newMail.Send()
    del win32
    time.sleep(1)
    remove_gen_pyPath()
    root.destroy()


##.........................................................
##  Login Page: Invalid Password Window                  .
##.........................................................
def invalid_password(root):
    validateUsername = ['no_username']
    validatePassword = ['worryKnuckleBandit']
    if password.get() != validatePassword:
        AttnLabel = Label(root, text='Invalid login ID or password!', fg="red", bg="#FFFFFF", font=("Cascadia Code", 10, 'bold'))
        AttnLabel.place(x=600, y=230)
        AttnLabel.after(3000, lambda: AttnLabel.destroy())
        Login_password_entry.delete(0, END)
        Login_username_entry.delete(0, END)
 
##.........................................................
##  Login Page: Forgot Password                  .
##.........................................................
def password_forgot():
  global root_password_forgot
  root_password_forgot = Toplevel()
  window_width = 600
  window_height = 350
  screen_width = root_password_forgot.winfo_screenwidth()
  screen_height = root_password_forgot.winfo_screenheight()
  position_top = int(screen_height / 4 - window_height / 4)
  position_right = int(screen_width / 2 - window_width / 2)
  root_password_forgot.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
  root_password_forgot.title('Forgot Password')
  root_password_forgot.iconbitmap(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logo3.ico", listdir=False))
  root_password_forgot.configure(background="#FFFFFF")
  root_password_forgot.resizable(False, False)
  root_password_forgot.wait_visibility()
  root_password_forgot.grab_set()
  # Email
  global requestPW_Text
  requestPW_Text = StringVar()
  forgot_Password_border = Frame(root_password_forgot, highlightbackground="#206DB4", highlightthickness=2, background="#FFFFFF")
  forgot_Password_border.place(x=40, y=80, width=465, height=45)

  def photoImage_8314():
    forgot_Password_icon = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="user_icon.png", listdir=False))
    forgot_Password_icon_Label = Label(root_password_forgot, image = forgot_Password_icon, background="#FFFFFF")
    forgot_Password_icon_Label.place(x=48, y=89)
    List_LoginPageImages.append(forgot_Password_icon)
    return forgot_Password_icon
  forgot_Password_icon = photoImage_8314()

  global forgot_Password_entry
  forgot_Password_entry = Entry(root_password_forgot, bd = 0, font = ("Cascadia Code SemiBold", 12), textvariable = requestPW_Text)
  forgot_Password_entry.place(x=88, y=87, width=400, height=30)
  forgotPasswordHeader = Label(root_password_forgot, text = "Enter Username", fg = "#272a42", font = ("Cascadia Code Bold", 15), bg = "#FFFFFF", bd = 0, height=0) 
  forgotPasswordHeader.place(x=200, y=47)
  # Update password Button
  getPasswordButton = Button(root_password_forgot, fg='#f8f8f8', text='Reset', bg='#1D90F5', font=("Cascadia Code", 12, "bold"), command = lambda: print(), cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5") 
  getPasswordButton.place(x=162, y=200, width=256, height=45)





###========================================================================
###========================================================================
###                                                                     ===
###                 DATABASE PAGE 2: INVENTORY DATABASE                 ===
###                                                                     ===
###========================================================================
###========================================================================
def Database_Screen():
  try:
    root_admin.destroy()
  except:
    pass
  try:
    root_login.destroy()
  except:
    pass
  try:
    root_database_loading.destroy()
  except:
    pass
  
  global root_database_main
  root_database_main = Tk()
  databaseHome_width = 1149
  databaseHome_height = 718
  databaseHome_screen_width = root_database_main.winfo_screenwidth()  
  databaseHome_screen_height = root_database_main.winfo_screenheight() 
  databaseHome_x = (databaseHome_screen_width/2) - (databaseHome_width/2)
  databaseHome_y = (databaseHome_screen_height/2) - (databaseHome_height/2)
  root_database_main.geometry('%dx%d+%d+%d' % (databaseHome_width, databaseHome_height, databaseHome_x, databaseHome_y))
  # root_database_main.overrideredirect(True) 
  root_database_main.resizable(False, False)
  root_database_main.title('Database Management')
  root_database_main.iconbitmap(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logo3.ico", listdir=False))
  root_database_main.configure(background="#FFFFFF")
  
  ## Set Global Variables
  global AddPlant_port_name_entry
  global AddPlant_plant_name_entry
  global AddValues_port_name_entry
  global AddValues_plant_name_entry
  global AddValues_date_entry
  global AddValues_arrivals_entry
  global AddPort_port_name_entry 
  global AddValues_port_name_text
  global AddValues_plant_name_text
  global AddValues_date_text
  global AddValues_arrivals_text
  global AddPort_port_name_text
  global AddPlant_port_name_text
  global AddPlant_plant_name_text
  global port_approve_button
  global plant_approve_button
  global date_approve_button
  global arrivals_approve_button
  global new_port_approve_button
  global choose_port_approve_button
  global new_plant_approve_button
  global databaseAdd_Values_SaveChanges_Button
  global databaseAdd_Port_SaveChanges_Button
  global databaseAdd_Plant_SaveChanges_Button
  global databaseAdd_Port_ConfirmButton_Button
  global databaseAdd_Values_ConfirmButton_Button
  global databaseAdd_Plant_ConfirmButton_Button
  
  
  ## Set Variables
  AddValues_port_name_text = StringVar()
  AddValues_plant_name_text = StringVar()
  AddValues_date_text = StringVar()
  AddValues_arrivals_text = StringVar()
  AddPort_port_name_text = StringVar()
  AddPlant_port_name_text = StringVar()
  AddPlant_plant_name_text = StringVar()
  port_list_selection = flatten_list(_SQL_.SELECT_ALL(database=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="inventory.db", listdir=False), tableName="ports").values.tolist())
  plant_list_selection = np.unique(np.array(_SQL_.SELECT_ALL(database=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="inventory.db", listdir=False), tableName="plants")["plant_name"].values.tolist())).tolist()
  
  
  ## Background
  databaseHome_image = Image.open(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="database_background.png", listdir=False))
  databaseHome_img = ImageTk.PhotoImage(databaseHome_image)
  databaseHome_label = Label(root_database_main, image=databaseHome_img, borderwidth=0)
  databaseHome_label.image = databaseHome_img
  databaseHome_label.pack()
  # View Database Button
  viewDatabase_Button = Button(root_database_main, text = "View Database", fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised", command = lambda: Database_View_CurrentInventory()) 
  viewDatabase_Button.place(x=10, y=150)
  # Add New Pellet Production Amount
  newValueEntry_Button = Button(root_database_main, text = "New Production Entry", fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised", command = lambda: Database_Add_Values()) 
  newValueEntry_Button.place(x=10, y=200)
  # New Port Entry
  newPortEntry_Button = Button(root_database_main, text = "New Port Entry", fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised", command = lambda: Database_Add_Port()) 
  newPortEntry_Button.place(x=10, y=250)
  # New Plant Entry
  newPlantEntry_Button = Button(root_database_main, text = "New Plant Entry", fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised", command = lambda: Database_Add_Plant()) 
  newPlantEntry_Button.place(x=10, y=300)
  # New Plant Entry
  modifyValueEntry_Button = Button(root_database_main, text = "Edit Production Entry", fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised", command = lambda: print()) 
  modifyValueEntry_Button.place(x=10, y=350)
  
  # Logo
  def databasePage_Home_photoImage_6943():
    logo_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logo_header.png", listdir=False))
    logo_imageLoginLabel = Label(root_database_main, image=logo_buttonImage, borderwidth=0, background="#FFFFFF")
    logo_imageLoginLabel.place(x=50, y=40)
    List_DataManagementImages.append(logo_buttonImage)
    return logo_buttonImage
  logo_buttonImage = databasePage_Home_photoImage_6943()
  
  # Exit
  def databasePage_Home_photoImage_12354():
    exitApp_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="exit_button.png", listdir=False))
    # exit_imageLoginButton = Button(root_database_main, image=exitApp_buttonImage, borderwidth=0, highlightthickness=0, command=lambda: root_database_main.destroy(), relief="flat", activebackground="#FFFFFF", cursor="hand2")
    exit_imageLoginButton = Button(root_database_main, image=exitApp_buttonImage, borderwidth=0, highlightthickness=0, command=lambda: sys.exit(), relief="flat", activebackground="#FFFFFF", cursor="hand2")
    exit_imageLoginButton.place(x=20, y=680)
    List_DataManagementImages.append(exitApp_buttonImage)
    return exitApp_buttonImage
  exitApp_buttonImage = databasePage_Home_photoImage_12354()
  
  # Log Out
  LogOutButton = Button(root_database_main, text = "Logout", fg = "#206DB4", font = ("Cascadia Code", 10), bg = "#FFFFFF", bd = 0, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#FFFFFF", command = lambda: database_logging_out()) 
  LogOutButton.place(x=52, y=640)

  def databasePage_Home_photoImage_131439457():
    database_log_out_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logout.png", listdir=False))
    database_log_out_Label = Button(root_database_main, image=database_log_out_buttonImage, borderwidth=0, background="#FFFFFF", bd = 0, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#FFFFFF", command = lambda: database_logging_out())
    database_log_out_Label.place(x=23, y=640)
    List_DataManagementImages.append(database_log_out_buttonImage)
    return database_log_out_buttonImage
  database_log_out_buttonImage = databasePage_Home_photoImage_131439457()
  
  
  ##  Create Buttons and Labels   .
  ##...................................................
  
  # View Database -------------
  def Button_688816():
    button = Button(root_database_main, text = "Load Database for Viewing", cursor = "hand2", font = ("Cascadia Code Bold", 11), command = lambda: Database_View(databaseName="inventory.db", table_Name="inventory"))
    return button
  view_button = Button_688816()
  
  
  
  # Add Values -------------
  def Label_367708():
    label = Label(root_database_main, text = "Select Port:", fg = "#206DB4", font = ("Cascadia Code Bold", 10), bg = "#FFFFFF")
    return label
  selectPort = Label_367708()
  
  def Label_652006():
    label = Label(root_database_main, text = "Select Plant:", fg = "#206DB4", font = ("Cascadia Code Bold", 10), bg = "#FFFFFF")
    return label
  selectPlant = Label_652006()
  
  def Label_101074():
    label = Label(root_database_main, text = "Select Date:", fg = "#206DB4", font = ("Cascadia Code Bold", 10), bg = "#FFFFFF")
    return label
  selectDate = Label_101074()
  
  def Label_203314():
    label = Label(root_database_main, text = "Enter Value:", fg = "#206DB4", font = ("Cascadia Code Bold", 10), bg = "#FFFFFF")
    return label
  selectArrivals = Label_203314()
  
  def Entry_205451():
    entry = OptionMenu(root_database_main, AddValues_port_name_text,  *port_list_selection)
    entry.config(highlightbackground="#206DB4", highlightcolor="#206DB4", width = 15, cursor="hand2")
    return entry
  AddValues_port_name_entry = Entry_205451()
  
  def Entry_153720():
    entry = OptionMenu(root_database_main, AddValues_plant_name_text,  *plant_list_selection)
    entry.config(highlightbackground="#206DB4", highlightcolor="#206DB4", width = 15, cursor="hand2")
    return entry
  AddValues_plant_name_entry = Entry_153720()
  
  def Entry_1949647():
    entry = DateEntry(root_database_main, background= "#206DB4", textvariable=AddValues_date_text, date_pattern='yyyy-mm-dd')
    entry.config(width = 18)
    entry.delete(0, END)
    return entry
  AddValues_date_entry = Entry_1949647()
  
  def Entry_114838():
    entry = Entry(root_database_main, font = ("Cascadia Code", 10), textvariable = AddValues_arrivals_text)
    entry.config(width = 16, relief="sunken")
    return entry
  AddValues_arrivals_entry = Entry_114838()
  
  def Button_123252():
    button = Button(root_database_main, text = "Approve", command = lambda: approve_entry(which = "Port", function = "AddValues"))
    return button
  port_approve_button = Button_123252()
  
  def Button_105495():
    button = Button(root_database_main, text = "Approve", command = lambda: approve_entry(which = "Plant", function = "AddValues"))
    return button
  plant_approve_button = Button_105495()
  
  def Button_308011():
    button = Button(root_database_main, text = "Approve", command = lambda: approve_entry(which = "Date", function = "AddValues"))
    return button
  date_approve_button = Button_308011()
  
  def Button_359441():
    button = Button(root_database_main, text = "Approve", command = lambda: approve_entry(which = "Arrivals", function = "AddValues"))
    return button
  arrivals_approve_button = Button_359441()
  
  def Button_136679():
    button = Button(root_database_main, text = "Insert", fg = "#FFFFFF", font = ("Cascadia Code", 13), bg = "#206DB4", bd = 3, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#272A37", relief="raised", command = lambda: databaseDataCollect(function="AddValues"))
    return button
  databaseAdd_Values_ConfirmButton_Button = Button_136679()

  def Button_68164():
    button = Button(root_database_main, text = "Refresh", fg = "#FFFFFF", font = ("Cascadia Code", 13), bg = "grey", bd = 3, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "grey", relief="raised", command = lambda: clear_all_entries(function="AddValues"))
    return button
  Add_Values_Refresh_Button = Button_68164()

  def Button_56106():
    button = Button(root_database_main, text = "Save Changes", fg = "#FFFFFF", font = ("Cascadia Code", 13), bg = "red", bd = 3, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "red", relief="raised", command = lambda: INSERT_INTO_INVENTORY_ALL())
    return button
  databaseAdd_Values_SaveChanges_Button = Button_56106()




  # Ports -------------
  def Entry_330886():
    entry = Entry(root_database_main, font = ("Cascadia Code", 10), textvariable = AddPort_port_name_text)
    entry.config(width = 16, relief="sunken")
    return entry
  AddPort_port_name_entry = Entry_330886()
  
  def Label_111699():
    label = Label(root_database_main, text = "Enter Port Name:", fg = "#206DB4", font = ("Cascadia Code Bold", 10), bg = "#FFFFFF")
    return label
  EnterPort = Label_111699()

  def Button_109634():
    button = Button(root_database_main, text = "Approve", command = lambda: approve_entry(which=None, function="AddPort"))
    return button
  new_port_approve_button = Button_109634()
  
  def Button_654891():
    button = Button(root_database_main, text = "Insert", fg = "#FFFFFF", font = ("Cascadia Code", 13), bg = "#206DB4", bd = 3, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#272A37", relief="raised", command = lambda: databaseDataCollect(function="AddPort"))
    return button
  databaseAdd_Port_ConfirmButton_Button = Button_654891()
  
  def Button_18075():
    button = Button(root_database_main, text = "Refresh", fg = "#FFFFFF", font = ("Cascadia Code", 13), bg = "grey", bd = 3, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "grey", relief="raised", command = lambda: clear_all_entries(function="AddPort"))
    return button
  Add_Port_Refresh_Button = Button_18075()
  
  def Button_30624():
    button = Button(root_database_main, text = "Save Changes", fg = "#FFFFFF", font = ("Cascadia Code", 13), bg = "red", bd = 3, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "red", relief="raised", command = lambda: INSERT_INTO_PORT())
    return button
  databaseAdd_Port_SaveChanges_Button = Button_30624()
  


  # Plants -------------
  def Label_11595100():
    label = Label(root_database_main, text = "Choose A Port:", fg = "#206DB4", font = ("Cascadia Code Bold", 10), bg = "#FFFFFF")
    return label
  ChoosePort = Label_11595100()

  def Label_10095996():
    label = Label(root_database_main, text = "Enter Plant Name:", fg = "#206DB4", font = ("Cascadia Code Bold", 10), bg = "#FFFFFF")
    return label
  EnterPlant = Label_10095996()

  def Entry_10636162():
    entry = OptionMenu(root_database_main, AddPlant_port_name_text,  *port_list_selection)
    entry.config(highlightbackground="#206DB4", highlightcolor="#206DB4", width = 15, cursor="hand2")
    return entry
  AddPlant_port_name_entry = Entry_10636162()

  def Entry_13106750():
    entry = Entry(root_database_main, font = ("Cascadia Code", 10), textvariable = AddPlant_plant_name_text)
    entry.config(width = 16, relief="sunken")
    return entry
  AddPlant_plant_name_entry = Entry_13106750()
  
  def Button_23296656():
    button = Button(root_database_main, text = "Approve", command = lambda: approve_entry(which="Port", function = "AddPlant"))
    return button
  choose_port_approve_button = Button_23296656()
  
  def Button_12073605():
    button = Button(root_database_main, text = "Approve", command = lambda: approve_entry(which="Plant", function = "AddPlant"))
    return button
  new_plant_approve_button = Button_12073605()

  def Button_21647036():
    button = Button(root_database_main, text = "Insert", fg = "#FFFFFF", font = ("Cascadia Code", 13), bg = "#206DB4", bd = 3, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#272A37", relief="raised", command = lambda: databaseDataCollect(function="AddPlant"))
    return button
  databaseAdd_Plant_ConfirmButton_Button = Button_21647036()
  
  def Button_72258():
    button = Button(root_database_main, text = "Refresh", fg = "#FFFFFF", font = ("Cascadia Code", 13), bg = "grey", bd = 3, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "grey", relief="raised", command = lambda: clear_all_entries(function="AddPlant"))
    return button
  Add_Plant_Refresh_Button = Button_72258()
  
  def Button_95969():
    button = Button(root_database_main, text = "Save Changes", fg = "#FFFFFF", font = ("Cascadia Code", 13), bg = "red", bd = 3, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "red", relief="raised", command = lambda: INSERT_INTO_PLANT())
    return button
  databaseAdd_Plant_SaveChanges_Button = Button_95969()


  ## Configure View Database Button
  ##----------------------------------------------
  def Database_View_CurrentInventory():
    CreateSQLTableValues(function=None)
    clear_all_entries(function="AddValues")
    # Highlight View Database Button
    viewDatabase_Button.configure(fg = "#206DB4", font = ("Cascadia Code Bold", 11), bg = "#FFFFFF", bd = 3,  cursor = "hand2", activebackground = "#206DB4", activeforeground = "#FFFFFF", relief="raised")
    # Unhighlight Other Tabs
    newValueEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised")
    newPortEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    newPlantEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    modifyValueEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    # Remove Unwanted Labels and Entries: Add Port
    EnterPort.place_forget()
    AddPort_port_name_entry.place_forget()
    new_port_approve_button.place_forget()
    databaseAdd_Port_ConfirmButton_Button.place_forget()
    Add_Port_Refresh_Button.place_forget()
    databaseAdd_Port_SaveChanges_Button.place_forget()
    # Remove Unwanted Labels and Entries: Add Values
    selectPort.place_forget()
    selectPlant.place_forget()
    selectDate.place_forget()
    selectArrivals.place_forget()
    AddValues_port_name_entry.place_forget()
    AddValues_plant_name_entry.place_forget()
    AddValues_date_entry.place_forget()
    AddValues_arrivals_entry.place_forget()
    port_approve_button.place_forget()
    plant_approve_button.place_forget()
    date_approve_button.place_forget()
    arrivals_approve_button.place_forget()
    databaseAdd_Values_ConfirmButton_Button.place_forget()
    databaseAdd_Values_SaveChanges_Button.place_forget()
    Add_Values_Refresh_Button.place_forget()
    # Remove Unwanted Labels and Entries: Add Plant
    ChoosePort.place_forget()
    EnterPlant.place_forget()
    AddPlant_port_name_entry .place_forget()
    AddPlant_plant_name_entry.place_forget()
    choose_port_approve_button.place_forget()
    new_plant_approve_button.place_forget()
    databaseAdd_Plant_ConfirmButton_Button.place_forget()
    Add_Plant_Refresh_Button.place_forget()
    databaseAdd_Plant_SaveChanges_Button.place_forget()
    # Add View Database Button
    view_button.place(x=400, y=120)
  
  
  
  ## Configure New Pellet Production Amount Button
  ##----------------------------------------------
  def Database_Add_Values():
    CreateSQLTableValues(function="AddValues")
    clear_all_entries(function="AddPort")
    clear_all_entries(function="AddPlant")
    # Highlight Entry Button
    newValueEntry_Button.configure(fg = "#206DB4", font = ("Cascadia Code Bold", 11), bg = "#FFFFFF", bd = 3,  cursor = "hand2", activebackground = "#206DB4", activeforeground = "#FFFFFF", relief="raised")
    # Unhighlight Other Tabs
    viewDatabase_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised")
    newPortEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    newPlantEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    modifyValueEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    # Remove Unwanted Labels and Entries: View Database
    view_button.place_forget()
    # Remove Unwanted Labels and Entries: Add Port
    EnterPort.place_forget()
    AddPort_port_name_entry.place_forget()
    new_port_approve_button.place_forget()
    databaseAdd_Port_ConfirmButton_Button.place_forget()
    Add_Port_Refresh_Button.place_forget()
    databaseAdd_Port_SaveChanges_Button.place_forget()
    # Remove Unwanted Labels and Entries: Add Plant
    ChoosePort.place_forget()
    EnterPlant.place_forget()
    AddPlant_port_name_entry .place_forget()
    AddPlant_plant_name_entry.place_forget()
    choose_port_approve_button.place_forget()
    new_plant_approve_button.place_forget()
    databaseAdd_Plant_ConfirmButton_Button.place_forget()
    Add_Plant_Refresh_Button.place_forget()
    databaseAdd_Plant_SaveChanges_Button.place_forget()
    ## Set Label Widgets
    selectPort.place(x=330, y=120)
    selectPlant.place(x=330, y=170)
    selectDate.place(x=330, y=220)
    selectArrivals.place(x=330, y=267)
    ## Set Entry Widgets
    AddValues_port_name_entry.place(x=490, y=120)
    AddValues_plant_name_entry.place(x=490, y=170)
    AddValues_date_entry.place(x=490, y=222)
    AddValues_arrivals_entry.place(x=490, y=270)
    AddValues_plant_name_entry.config(state= "disabled")
    AddValues_date_entry.config(state= "disabled")
    AddValues_arrivals_entry.config(state= "disabled")
    ## Set Confirm / Deny Widgets
    port_approve_button.place(x=630, y=120)
    plant_approve_button.place(x=630, y=170)
    plant_approve_button.config(state= "disabled")
    date_approve_button.place(x=630, y=222)
    date_approve_button.config(state= "disabled")
    arrivals_approve_button.place(x=630, y=268)
    arrivals_approve_button.config(state= "disabled")
    # Confirm Button
    databaseAdd_Values_ConfirmButton_Button.place(x=330, y=380)
    Add_Values_Refresh_Button.place(x=430, y=380)
    # databaseAdd_Values_SaveChanges_Button.place(x=530, y=380)
    databaseAdd_Values_SaveChanges_Button.place_forget()

  ## Configure New Port Button
  ##----------------------------------------------
  def Database_Add_Port():
    CreateSQLTableValues(function="AddPort")
    clear_all_entries(function="AddValues")
    clear_all_entries(function="AddPlant")
    # Highlight Entry Button
    newPortEntry_Button.configure(fg = "#206DB4", font = ("Cascadia Code Bold", 11), bg = "#FFFFFF", bd = 3,  cursor = "hand2", activebackground = "#206DB4", activeforeground = "#FFFFFF", relief="raised")
    # Unhighlight Other Tabs
    newValueEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised")
    viewDatabase_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised")
    newPlantEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    modifyValueEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    # Remove Unwanted Labels and Entries: View Database
    view_button.place_forget()
    # Remove Unwanted Labels and Entries: Add Values
    selectPort.place_forget()
    selectPlant.place_forget()
    selectDate.place_forget()
    selectArrivals.place_forget()
    AddValues_port_name_entry.place_forget()
    AddValues_plant_name_entry.place_forget()
    AddValues_date_entry.place_forget()
    AddValues_arrivals_entry.place_forget()
    port_approve_button.place_forget()
    plant_approve_button.place_forget()
    date_approve_button.place_forget()
    arrivals_approve_button.place_forget()
    databaseAdd_Values_ConfirmButton_Button.place_forget()
    databaseAdd_Values_SaveChanges_Button.place_forget()
    Add_Values_Refresh_Button.place_forget()
    # Remove Unwanted Labels and Entries: Add Plant
    ChoosePort.place_forget()
    EnterPlant.place_forget()
    AddPlant_port_name_entry .place_forget()
    AddPlant_plant_name_entry.place_forget()
    choose_port_approve_button.place_forget()
    new_plant_approve_button.place_forget()
    databaseAdd_Plant_ConfirmButton_Button.place_forget()
    Add_Plant_Refresh_Button.place_forget()
    databaseAdd_Plant_SaveChanges_Button.place_forget()
    ## Set Label Widgets
    EnterPort.place(x=330, y=120)
    ## Set Entry Widgets
    AddPort_port_name_entry.place(x=490, y=120)
    ## Set Confirm / Deny Widgets
    new_port_approve_button.place(x=630, y=120)
    # Confirm Button
    databaseAdd_Port_ConfirmButton_Button.place(x=330, y=380)
    Add_Port_Refresh_Button.place(x=430, y=380)
    # databaseAdd_Port_SaveChanges_Button.place(x=530, y=380)
    databaseAdd_Port_SaveChanges_Button.place_forget()


  ## Configure New Plant Button
  ##----------------------------------------------
  def Database_Add_Plant():
    CreateSQLTableValues(function="AddPlant")
    clear_all_entries(function="AddValues")
    clear_all_entries(function="AddPort")
    # Highlight Entry Button
    newPlantEntry_Button.configure(fg = "#206DB4", font = ("Cascadia Code Bold", 11), bg = "#FFFFFF", bd = 3,  cursor = "hand2", activebackground = "#206DB4", activeforeground = "#FFFFFF", relief="raised")
    # Unhighlight Other Tabs
    newValueEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised")
    viewDatabase_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised")
    newPortEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    modifyValueEntry_Button.configure(fg = "#FFFFFF", font = ("Cascadia Code Bold", 11), bg = "#206DB4", bd = 3,  cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#206DB4", relief="raised") 
    # Remove Unwanted Labels and Entries: View Database
    view_button.place_forget()
    # Remove Unwanted Labels and Entries: Add Values
    selectPort.place_forget()
    selectPlant.place_forget()
    selectDate.place_forget()
    selectArrivals.place_forget()
    AddValues_port_name_entry.place_forget()
    AddValues_plant_name_entry.place_forget()
    AddValues_date_entry.place_forget()
    AddValues_arrivals_entry.place_forget()
    Add_Values_Refresh_Button.place_forget()
    port_approve_button.place_forget()
    plant_approve_button.place_forget()
    date_approve_button.place_forget()
    arrivals_approve_button.place_forget()
    databaseAdd_Values_ConfirmButton_Button.place_forget()
    databaseAdd_Values_SaveChanges_Button.place_forget()
    # Remove Unwanted Labels and Entries: Add Port
    EnterPort.place_forget()
    AddPort_port_name_entry.place_forget()
    new_port_approve_button.place_forget()
    databaseAdd_Port_ConfirmButton_Button.place_forget()
    Add_Port_Refresh_Button.place_forget()
    databaseAdd_Port_SaveChanges_Button.place_forget()
    ## Set Label Widgets
    ChoosePort.place(x=330, y=120)
    EnterPlant.place(x=330, y=170)
    ## Set Entry Widgets
    AddPlant_port_name_entry.place(x=490, y=120)
    AddPlant_plant_name_entry.place(x=490, y=170)
    ## Set Confirm / Deny Widgets
    choose_port_approve_button.place(x=630, y=120)
    #choose_port_annul_button.place(x=697, y=120)
    new_plant_approve_button.place(x=630, y=170)
    new_plant_approve_button.config(state= "disabled") 
    # Confirm Button
    databaseAdd_Plant_ConfirmButton_Button.place(x=330, y=380)
    Add_Plant_Refresh_Button.place(x=430, y=380)
    # databaseAdd_Plant_SaveChanges_Button.place(x=530, y=380)
    databaseAdd_Plant_SaveChanges_Button.place_forget()







###========================================================================
###========================================================================
###                                                                     ===
###                 DATABASE PAGE 1: ADMIN LOGIN SCREEN                 ===
###                                                                     ===
###========================================================================
###========================================================================
def data_management_login():
  global root_admin
  root_admin = Toplevel()
  root_admin.geometry("650x250")
  root_admin.configure(background='black')
  root_admin.resizable(False, False)
  root_admin.wait_visibility()
  root_admin.grab_set()
  root_admin.overrideredirect(True)
  #root_admin.attributes('-fullscreen', True)
  root_admin.state("zoomed")
  
  adminlabel = Label(root_admin, text='Enter Admin Username:', fg="#FFFFFF", bg='black', font=("Cascadia Code", 11, 'bold')) 
  adminlabel.pack(padx=10, pady=10)
  
  adminUsername_entry = Entry(root_admin, bg="#3D404B", font=("Cascadia Code semibold", 12), highlightthickness=1, bd=0, fg="#FFFFFF")  
  adminUsername_entry.pack()
  adminUsername_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")

  admin_password_label = Label(root_admin, text='Admin Password:', fg="#FFFFFF", bg='black', font=("Cascadia Code", 11, 'bold'))
  admin_password_label.pack(padx=10, pady=20)
  
  admin_password_entry = Entry(root_admin, bg="#3D404B", font=("Cascadia Code semibold", 12), highlightthickness=1, bd=0, fg="#FFFFFF")  
  admin_password_entry.pack()
  admin_password_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")

  initiateLoginButton = Button(root_admin, fg='#f8f8f8', text='Login', bg='#1D90F5', font=("Cascadia Code", 12, "bold"), command = lambda: data_management_login_status(), cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5") 
  initiateLoginButton.pack(padx=10, pady=10)

  initiateExitButton = Button(root_admin, fg='#f8f8f8', text='Exit', bg='red', font=("Cascadia Code", 12, "bold"), command = lambda: sys.exit(), cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5") 
  initiateExitButton.pack(padx=10, pady=5)






###========================================================================
###========================================================================
###                                                                     ===
###                      HOME PAGE 1: WELCOME BACK                      ===
###                                                                     ===
###========================================================================
###========================================================================
def Welcome_Screen():
    global root_welcome
    root_welcome = Toplevel()
    welcome_width = 1260 
    welcome_height = 720 
    welcome_screen_width = root_welcome.winfo_screenwidth()  
    welcome_screen_height = root_welcome.winfo_screenheight() 
    welcome_x = (welcome_screen_width/2) - (welcome_width/2)
    welcome_y = (welcome_screen_height/2) - (welcome_height/2)
    root_welcome.geometry('%dx%d+%d+%d' % (welcome_width, welcome_height, welcome_x, welcome_y))
    root_welcome.overrideredirect(True) # Hide the title bar
    root_welcome.resizable(False, False)
    root_welcome.wait_visibility()
    root_welcome.grab_set()
    welcome_label = PhotoImage_GIF(root_welcome, borderwidth=0)
    welcome_label.Open(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="welcome_page.gif", listdir=False))
    welcome_label.pack()
    root_welcome.after(1500, Home_Screen)




###========================================================================
###========================================================================
###                                                                     ===
###                          HOME PAGE 2: HOME                          ===
###                                                                     ===
###========================================================================
###========================================================================
def Home_Screen():
  global root_home
  try:
    root_login.destroy()
  except:
    pass
  try:
    root_welcome.destroy()
  except:
    pass

  root_home = Tk()
  HomeScreenHome_width = 1149
  HomeScreenHome_height = 718
  HomeScreenHome_screen_width = root_home.winfo_screenwidth()  
  HomeScreenHome_screen_height = root_home.winfo_screenheight() 
  HomeScreenHome_x = (HomeScreenHome_screen_width/2) - (HomeScreenHome_width/2)
  HomeScreenHome_y = (HomeScreenHome_screen_height/2) - (HomeScreenHome_height/2)
  root_home.geometry('%dx%d+%d+%d' % (HomeScreenHome_width, HomeScreenHome_height, HomeScreenHome_x, HomeScreenHome_y))
  # root_home.overrideredirect(True) 
  root_home.resizable(False, False)
  root_home.title('Home')
  root_home.iconbitmap(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logo3.ico", listdir=False))
  root_home.configure(background="#FFFFFF")

  ## Background
  HomeScreenHome_image = Image.open(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="home_bg.png", listdir=False))
  HomeScreenHome_img = ImageTk.PhotoImage(HomeScreenHome_image)
  HomeScreenHome_label = Label(root_home, image=HomeScreenHome_img, borderwidth=0)
  HomeScreenHome_label.image = HomeScreenHome_img
  HomeScreenHome_label.pack()

  # Logo
  def HomeScreenPage_Home_photoImage_14694718():
    Home_logo_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logo_header.png", listdir=False))
    Homelogo_imageLoginLabel = Label(root_home, image=Home_logo_buttonImage, borderwidth=0, background="#FFFFFF", width=120, height=46)
    Homelogo_imageLoginLabel.place(x=20, y=40)
    List_HomePageImages.append(Home_logo_buttonImage)
    return Home_logo_buttonImage
  Home_Home_logo_buttonImage = HomeScreenPage_Home_photoImage_14694718()
  
  # Directory Watcher Text
  DirectoryWatcherText = Label(root_home, text = "Directory Watchers", fg = "#206DB4", font = ("Cascadia Code Bold", 12), bg = "#FFFFFF", bd = 0) 
  DirectoryWatcherText.place(x=200, y=110)

  # Baltic Text
  BalticText = Label(root_home, text = "Baltic Exchange Report", fg = "#206DB4", font = ("Cascadia Code Bold", 12), bg = "#FFFFFF", bd = 0) 
  BalticText.place(x=200, y=445)

  def HomeScreenPage_Home_photoImage_16099666():
    balticDownloadHome_Image = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="download_button.png", listdir=False))
    balticDownloadHome_Button = Button(root_home, image=balticDownloadHome_Image, borderwidth=0, bg="#FFFFFF",highlightthickness=0, command = lambda: baltic_download_waiting(), relief="flat", activebackground="#FFFFFF", cursor="hand2")
    balticDownloadHome_Button.place(x=270, y=480)
    List_HomePageImages.append(balticDownloadHome_Image)
    return balticDownloadHome_Image
  balticDownloadHome_Image = HomeScreenPage_Home_photoImage_16099666()
  
  # Profile
  def HomeScreenPage_Home_photoImage_39439712():
    profile_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="user_profile_pic.png", listdir=False))
    profile_imageLoginLabel = Label(root_home, image=profile_buttonImage, borderwidth=0, background="#206DB4")
    profile_imageLoginLabel.place(x=998, y=20)
    List_HomePageImages.append(profile_buttonImage)
    return profile_buttonImage
  profile_buttonImage = HomeScreenPage_Home_photoImage_39439712()
  
  # Welcome User Text
  WelcomeUserText = Label(root_home, text = f'Welcome, {os.getlogin().split(".")[0]}', fg = "#FFFFFF", font = ("Cascadia Code Bold", 8), bg = "#206DB4", bd = 0) 
  WelcomeUserText.place(x=1030, y=28)
  
  # Exit
  def HomeScreenPage_Home_photoImage_17119258():
    exitAppHome_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="exit_button.png", listdir=False))
    # exit_imagehomeButton = Button(root_home, image=exitAppHome_buttonImage, borderwidth=0, highlightthickness=0, command=lambda: root_home.destroy(), relief="flat", activebackground="#FFFFFF", cursor="hand2")
    exit_imagehomeButton = Button(root_home, image=exitAppHome_buttonImage, borderwidth=0, highlightthickness=0, command=lambda: sys.exit(), relief="flat", activebackground="#FFFFFF", cursor="hand2")
    exit_imagehomeButton.place(x=20, y=680)
    List_HomePageImages.append(exitAppHome_buttonImage)
    return exitAppHome_buttonImage
  exitAppHome_buttonImage = HomeScreenPage_Home_photoImage_17119258()
  
  # Log Out
  HomeLogOutButton = Button(root_home, text = "Logout", fg = "#206DB4", font = ("Cascadia Code", 10), bg = "#FFFFFF", bd = 0, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#FFFFFF", command = lambda: home_logging_out()) 
  HomeLogOutButton.place(x=52, y=622)

  def HomeScreenPage_Home_photoImage_394318372():
    log_out_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logout.png", listdir=False))
    log_out_imageLoginLabel = Button(root_home, image=log_out_buttonImage, borderwidth=0, background="#FFFFFF", bd = 0, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#FFFFFF", command = lambda: home_logging_out())
    log_out_imageLoginLabel.place(x=23, y=620)
    List_HomePageImages.append(log_out_buttonImage)
    return log_out_buttonImage
  log_out_buttonImage = HomeScreenPage_Home_photoImage_394318372()

 
 
 
  ##========================================================================
  ##    Voyage Tracker                                                       
  ##========================================================================
  ## Create Voyage Tracker Label Text
  if is_voyage_tracker_switch_on == True:
    statusTextLabel_1 = Label(root_home, text="Voyage Directory Watcher On!", fg="#76bc21", font=("Cascadia Code Bold", 9), bg="#FFFFFF") 
    statusTextLabel_1.place(x=192, y=170)
  elif is_voyage_tracker_switch_on == False:
    statusTextLabel_1 = Label(root_home, text="Voyage Directory Watcher Off!", fg="grey", font=("Cascadia Code Bold", 9), bg="#FFFFFF") 
    statusTextLabel_1.place(x=192, y=170)
  
  ### Define Function to Control Switch
  global VoyageTrackerSwitch
  def VoyageTrackerSwitch():
    global is_voyage_tracker_switch_on
    # Determine is on or off
    if is_voyage_tracker_switch_on:
      voyage_tracker_button.config(image = voyage_tracker_offImage)
      statusTextLabel_1.config(text = "Voyage Directory Watcher Is Off!", fg = "grey", font=("Cascadia Code Bold", 9), bg="#FFFFFF") 
      is_voyage_tracker_switch_on = False
      quickKill(processName=["pyw.exe", "pythonw.exe", "python.exe", ".py"], filePath='Vryonisyrnaoutsopoula94080')
      # root_home.attributes('-topmost', 1)
    else:
      voyage_tracker_button.config(image = voyage_tracker_onImage)
      statusTextLabel_1.config(text = "Voyage Directory Watcher Is On!", fg = "#76bc21", font=("Cascadia Code Bold", 9), bg="#FFFFFF")
      is_voyage_tracker_switch_on = True
      startProcess(programParam="python", processName=None, fileParam="Vryonisyrnaoutsopoula94080")
      # root_home.attributes('-topmost', 1)
  
  ## Define Our Images
  ### On Image
  def open_dir_image_1():
    voyage_tracker_onImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="on.png", listdir=False))
    List_HomePageImages.append(voyage_tracker_onImage)
    return voyage_tracker_onImage
  voyage_tracker_onImage = open_dir_image_1()
  
  ### Off Image
  def open_dir_image_2():
    voyage_tracker_offImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="off.png", listdir=False))
    List_HomePageImages.append(voyage_tracker_offImage)
    return voyage_tracker_offImage
  voyage_tracker_offImage = open_dir_image_2()
  
  ### Create A Button to Define which button to start with
  if is_voyage_tracker_switch_on == False:
    voyage_tracker_button = Button(root_home, image = voyage_tracker_offImage, bd = 0, activebackground="#FFFFFF", fg="#FFFFFF", bg="#FFFFFF", command = lambda: voyage_waiting(), cursor="hand2")
    voyage_tracker_button.place(x=192, y=200)
  elif is_voyage_tracker_switch_on == True:
    voyage_tracker_button = Button(root_home, image = voyage_tracker_onImage, bd = 0, activebackground="#FFFFFF", fg="#FFFFFF",bg="#FFFFFF", command = lambda: voyage_waiting(), cursor="hand2")
    voyage_tracker_button.place(x=192, y=200)
  
  
  
  ##========================================================================
  ##    Shipping Plan                                                       
  ##========================================================================
  ## Create Shipping Plan Label Text
  if is_shipping_plan_switch_on == True:
    statusTextLabel_2 = Label(root_home, text="Shipping Directory Watcher Is On!", fg="#76bc21", font=("Cascadia Code Bold", 9), bg="#FFFFFF") 
    statusTextLabel_2.place(x=192, y=270)
  elif is_shipping_plan_switch_on == False:
    statusTextLabel_2 = Label(root_home, text="Shipping Directory Watcher Is Off!", fg="grey", font=("Cascadia Code Bold", 9), bg="#FFFFFF") 
    statusTextLabel_2.place(x=192, y=270)
  
  ### Define Function to Control Switch
  global ShippingPlanSwitch
  def ShippingPlanSwitch():
    global is_shipping_plan_switch_on
    # Determine is on or off
    if is_shipping_plan_switch_on:
      shipping_plan_button.config(image = shipping_plan_offImage)
      statusTextLabel_2.config(text = "Shipping Directory Watcher Is Off!", fg = "grey", font=("Cascadia Code Bold", 9), bg="#FFFFFF") 
      is_shipping_plan_switch_on = False
      quickKill(processName=["pyw.exe", "pythonw.exe", "python.exe", ".py"], filePath='Skantitrikeristroklou60763')
      # root_home.attributes('-topmost', 1)
    else:
      shipping_plan_button.config(image = shipping_plan_onImage)
      statusTextLabel_2.config(text = "Shipping Directory Watcher Is On!", fg = "#76bc21", font=("Cascadia Code Bold", 9), bg="#FFFFFF") 
      is_shipping_plan_switch_on = True
      startProcess(programParam="python", processName=None, fileParam="Skantitrikeristroklou60763")
      # root_home.attributes('-topmost', 1)
  
  ## Define Our Images
  ### On Image
  def open_dir_image_3():
    shipping_plan_onImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="on.png", listdir=False))
    List_HomePageImages.append(shipping_plan_onImage)
    return shipping_plan_onImage
  shipping_plan_onImage = open_dir_image_3()
  
  ### Off Image
  def open_dir_image_4():
    shipping_plan_offImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="off.png", listdir=False))
    List_HomePageImages.append(shipping_plan_offImage)
    return shipping_plan_offImage
  shipping_plan_offImage = open_dir_image_4()
  
  ### Create A Button to Define which button to start with
  if is_shipping_plan_switch_on == False:
    shipping_plan_button = Button(root_home, image = shipping_plan_offImage, bd = 0, activebackground="#FFFFFF", fg="#FFFFFF", bg="#FFFFFF", command = lambda: shipping_waiting(), cursor="hand2")
    shipping_plan_button.place(x=192, y=300)
  elif is_shipping_plan_switch_on == True:
    shipping_plan_button = Button(root_home, image = shipping_plan_onImage, bd = 0, activebackground="#FFFFFF", fg="#FFFFFF",bg="#FFFFFF", command = lambda: shipping_waiting(), cursor="hand2")
    shipping_plan_button.place(x=192, y=300)  

  # Voyage Tracker Report Text
  VoyageTrackerReportText = Label(root_home, text = "Voyage Tracker Reports", fg = "#206DB4", font = ("Cascadia Code Bold", 12), bg = "#FFFFFF", bd = 0)
  VoyageTrackerReportText.place(x=500, y=110)
  
  ##========================================================================
  ##    Financial Section                                                       
  ##========================================================================
  # Set Globals
  global startingFinancialText
  global startingFinancialEntry
  global endingFinancialText
  global endingFinancialEntry
  global financial_reports_path
  financial_reports_path = full_path('R:/Depts/Sales-Marketing/SystemsNavigator_ShipNavApplication/VoyageTracker/output/financial')
  # Set Text Variable
  startingFinancialText = StringVar()
  startingFinancialText.set("")
  endingFinancialText = StringVar()
  endingFinancialText.set("")
  # Financial Tracker Report Text
  FinancialComparisonText = Label(root_home, text = "Compare Financial Reports", fg = "black", font = ("Cascadia Code Bold", 10), bg = "#FFFFFF", bd = 0)
  FinancialComparisonText.place(x=630, y=160)
  
  # Set Label
  startingFinancial_label = Label(root_home, text='Select Starting File:', fg="#206DB4", bg='#FFFFFF', font=("Cascadia Code", 9, 'bold')) 
  startingFinancial_label.place(x=510, y=200)
  
  endingFinancial_label = Label(root_home, text='Select Ending File:', fg="#206DB4", bg='#FFFFFF', font=("Cascadia Code", 9, 'bold')) 
  endingFinancial_label.place(x=750, y=200)

  # Set Option Menu
  startingFinancialEntry = OptionMenu(root_home, startingFinancialText,  *[os.path.basename(f).replace(".xlsm", '') for f in financial_reports_path if "~$" not in os.path.basename(f).replace(".xlsm", '')])
  startingFinancialEntry.place(x=520, y=230)
  startingFinancialEntry.config(highlightbackground="#206DB4", highlightcolor="#206DB4", width = 10, cursor="hand2")
  
  endingFinancialEntry = OptionMenu(root_home, endingFinancialText,  *[os.path.basename(f).replace(".xlsm", '') for f in financial_reports_path if "~$" not in os.path.basename(f).replace(".xlsm", '')])
  endingFinancialEntry.place(x=780, y=230)
  endingFinancialEntry.config(highlightbackground="#206DB4", highlightcolor="#206DB4", width = 10, cursor="hand2")
  

  viewFinancialResultsButton = Button(root_home, fg='#FFFFFF', text='View', bg='#b46720', font=("Cascadia Code", 8, "bold"), command = lambda: viewResults(selection="Financial"), cursor='hand2', relief="raised", bd=3, highlightthickness=0, activebackground="#b46720")
  viewFinancialResultsButton.place(x=900, y=205)

  exportFinancialResultsButton = Button(root_home, fg='#FFFFFF', text='Export', bg='#b46720', font=("Cascadia Code", 8, "bold"), command = lambda: exportResults(selection="Financial"), cursor='hand2', relief="raised", bd=3, highlightthickness=0, activebackground="#b46720")
  exportFinancialResultsButton.place(x=900, y=235)


  ##========================================================================
  ##    Itinerary Section                                                       
  ##========================================================================
  # Set Globals
  global startingItineraryText
  global startingItineraryEntry
  global endingItineraryText
  global endingItineraryEntry
  global itinerary_reports_path
  itinerary_reports_path = full_path('R:/Depts/Sales-Marketing/SystemsNavigator_ShipNavApplication/VoyageTracker/output/itinerary')
  # Set Text Variable
  startingItineraryText = StringVar()
  startingItineraryText.set("")
  endingItineraryText = StringVar()
  endingItineraryText.set("")
  # Itinerary Tracker Report Text
  ItineraryComparisonText = Label(root_home, text = "Compare Itinerary Reports", fg = "black", font = ("Cascadia Code Bold", 10), bg = "#FFFFFF", bd = 0)
  ItineraryComparisonText.place(x=630, y=360)
  
  # Set Label
  startingItinerary_label = Label(root_home, text='Select Starting File:', fg="#206DB4", bg='#FFFFFF', font=("Cascadia Code", 9, 'bold')) 
  startingItinerary_label.place(x=510, y=400)
  
  endingItinerary_label = Label(root_home, text='Select Ending File:', fg="#206DB4", bg='#FFFFFF', font=("Cascadia Code", 9, 'bold')) 
  endingItinerary_label.place(x=750, y=400)

  # Set Option Menu
  startingItineraryEntry = OptionMenu(root_home, startingItineraryText,  *[os.path.basename(f).replace(".xlsm", '') for f in itinerary_reports_path if "~$" not in os.path.basename(f).replace(".xlsm", '')])
  startingItineraryEntry.place(x=520, y=430)
  startingItineraryEntry.config(highlightbackground="#206DB4", highlightcolor="#206DB4", width = 10, cursor="hand2")
  
  endingItineraryEntry = OptionMenu(root_home, endingItineraryText,  *[os.path.basename(f).replace(".xlsm", '') for f in itinerary_reports_path if "~$" not in os.path.basename(f).replace(".xlsm", '')])
  endingItineraryEntry.place(x=780, y=430)
  endingItineraryEntry.config(highlightbackground="#206DB4", highlightcolor="#206DB4", width = 10, cursor="hand2")
  

  viewItineraryResultsButton = Button(root_home, fg='#FFFFFF', text='View', bg='#b46720', font=("Cascadia Code", 8, "bold"), command = lambda: viewResults(selection="Itinerary"), cursor='hand2', relief="raised", bd=3, highlightthickness=0, activebackground="#b46720")
  viewItineraryResultsButton.place(x=900, y=405)

  exportItineraryResultsButton = Button(root_home, fg='#FFFFFF', text='Export', bg='#b46720', font=("Cascadia Code", 8, "bold"), command = lambda: exportResults(selection="Itinerary"), cursor='hand2', relief="raised", bd=3, highlightthickness=0, activebackground="#b46720")
  exportItineraryResultsButton.place(x=900, y=435)




















###========================================================================
###========================================================================
###                                                                     ===
###                          LOGIN PAGE: LOGIN                          ===
###                                                                     ===
###========================================================================
###========================================================================
def Login_Screen():
  try:
    root_logout.destroy()
  except:
    pass
  try:
    root_splash.destroy()
  except:
    pass
  try:
    root_home.destroy()
  except:
    pass
  try:
    root_database_main.destroy()
  except:
    pass

  global root_login
  root_login = Tk()
  login_width = 1149
  login_height = 718
  login_screen_width = root_login.winfo_screenwidth()  
  login_screen_height = root_login.winfo_screenheight() 
  login_x = (login_screen_width/2) - (login_width/2)
  login_y = (login_screen_height/2) - (login_height/2)
  root_login.geometry('%dx%d+%d+%d' % (login_width, login_height, login_x, login_y))
  # root_login.overrideredirect(True) 
  root_login.resizable(False, False)
  root_login.title('Login')
  root_login.iconbitmap(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logo3.ico", listdir=False))
  root_login.configure(background="#FFFFFF")
  login_image = Image.open(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="login_page_image.png", listdir=False))
  login_img = ImageTk.PhotoImage(login_image)
  login_label = Label(root_login, image=login_img, borderwidth=0)
  login_label.image = login_img
  login_label.pack()

  loginAccount_headerMain = Label(root_login, text = "Welcome Back!", fg = "#272a42", font = ("Cascadia Code Bold", 28), bg = "#FFFFFF", bd = 0, height=0) 
  loginAccount_headerMain.place(x=600, y=155)

  loginAccount_header = Label(root_login, text = "Login to continue", fg = "#272a42", font = ("Cascadia Code light", 15), bg = "#FFFFFF", bd = 0, height=0) 
  loginAccount_header.place(x=600, y=200)

  needAccessText = Label(root_login, text = "Need Access?", fg = "#272a42", font = ("Cascadia Code", 12), bg = "#FFFFFF", bd = 0) 
  needAccessText.place(x=835, y=38)

  switchRequestAccess = Button(root_login, text = "Request Access", fg = "#206DB4", font = ("Cascadia Code", 12), bg = "#FFFFFF", bd = 0, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#ffffff", command = lambda: request_access()) 
  switchRequestAccess.place(x=950, y=33)

  
  global username
  username = StringVar()
  Login_username_border = Frame(root_login, highlightbackground="#206DB4", highlightthickness=2, background="#FFFFFF")
  Login_username_border.place(x=600, y=255, width=465, height=45)

  def photoImage_4():
    Login_username_icon = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="user_icon.png", listdir=False))
    Login_username_icon_Label = Label(root_login, image = Login_username_icon, background="#FFFFFF")
    Login_username_icon_Label.place(x=608, y=264)
    List_LoginPageImages.append(Login_username_icon)
    return Login_username_icon
  Login_username_icon = photoImage_4()

  global Login_username_entry
  Login_username_entry = Entry(root_login, bd = 0, font = ("Cascadia Code SemiBold", 12), textvariable = username)
  Login_username_entry.place(x=648, y=262, width=400, height=30)



  global password
  password = StringVar()
  Login_password_border = Frame(root_login, highlightbackground="#206DB4", highlightthickness=2, background="#FFFFFF")
  Login_password_border.place(x=600, y=330, width=465, height=45)

  def photoImage_5():
    Login_password_icon = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="password_icon.png", listdir=False))
    Login_password_icon_Label = Label(root_login, image = Login_password_icon, background="#FFFFFF")
    Login_password_icon_Label.place(x=608, y=343)
    List_LoginPageImages.append(Login_password_icon)
    return Login_password_icon
  Login_password_icon = photoImage_5()
  
  global Login_password_entry
  Login_password_entry = Entry(root_login, bd = 0, font = ("Cascadia Code SemiBold", 12), textvariable = password)
  Login_password_entry.place(x=648, y=337, width=400, height=30)


 
  def photoImage_7():
    MainLogin_button_image = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="login_screen_button.png", listdir=False))
    MainLogin_button = Button(root_login, image = MainLogin_button_image, borderwidth = 0, highlightthickness = 0, command = lambda:invalid_password(root = root_login), relief = "flat", activebackground = "#FFFFFF", cursor = "hand2")
    MainLogin_button.place(x=600, y=420)
    List_LoginPageImages.append(MainLogin_button_image)
    return MainLogin_button_image
  MainLogin_button_image = photoImage_7()


  ForgotPasswordText = Button(root_login, text = "FORGOT PASSWORD?", fg = "#272a42", font = ("Cascadia Code", 11), bg = "#FFFFFF", bd = 0, cursor = "hand2", activebackground = "#FFFFFF", activeforeground = "#ffffff", command = lambda: password_forgot()) 
  ForgotPasswordText.place(x=855, y=441)

  LoginOptionsText = Label(root_login, text = "Login with", fg = "#272a42", font = ("Cascadia Code light", 10), bg = "#FFFFFF", bd = 0) 
  LoginOptionsText.place(x=590, y=630)


  def photoImage_8():
    SSOLogin_button_image = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="single_sign_on_button.png", listdir=False))
    List_LoginPageImages.append(SSOLogin_button_image)
    return SSOLogin_button_image
  SSOLogin_button_image = photoImage_8()

  if len(validate) > 0:
    SSOLogin_Button = Button(root_login, image = SSOLogin_button_image, borderwidth = 0, background = "#FFFFFF", highlightthickness = 0, command = lambda: Welcome_Screen(), relief = "flat", activebackground = "#FFFFFF", cursor = "hand2")
    SSOLogin_Button.place(x=690, y=600)
  else:
    SSOLogin_Button = Button(root_login, image = SSOLogin_button_image, borderwidth = 0, background = "#FFFFFF", highlightthickness = 0, relief = "flat", activebackground = "#FFFFFF", cursor = "hand2")
    SSOLogin_Button.place(x=690, y=600)

  def photoImage_10():
    manageData_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="data_management_button.png", listdir=False))
    manageData_imageLoginButton = Button(root_login, image=manageData_buttonImage, borderwidth=0, highlightthickness=0, command=lambda: data_management_login(), relief="flat", activebackground="#FFFFFF", cursor="hand2")
    manageData_imageLoginButton.place(x=880, y=590)
    List_LoginPageImages.append(manageData_buttonImage)
    return manageData_buttonImage
  manageData_buttonImage = photoImage_10()
  
  def photoImage_472():
    logo_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="logo_header.png", listdir=False))
    logo_imageLoginLabel = Label(root_login, image=logo_buttonImage, borderwidth=0, background="#FFFFFF")
    logo_imageLoginLabel.place(x=50, y=40)
    List_LoginPageImages.append(logo_buttonImage)
    return logo_buttonImage
  logo_buttonImage = photoImage_472()
  
  def photoImage_9():
    exitApp_buttonImage = PhotoImage(file=findPath(base_path=pathlib.Path().resolve(), isdir=False, name="exit_button.png", listdir=False))
    exit_imageLoginButton = Button(root_login, image=exitApp_buttonImage, borderwidth=0, highlightthickness=0, command=lambda: sys.exit(), relief="flat", activebackground="#FFFFFF", cursor="hand2")
    exit_imageLoginButton.place(x=20, y=680)
    List_LoginPageImages.append(exitApp_buttonImage)
    return exitApp_buttonImage
  exitApp_buttonImage = photoImage_9()












###========================================================================
###========================================================================
###                                                                     ===
###                             SPLASH PAGE                             ===
###                                                                     ===
###========================================================================
###========================================================================
root_splash = Tk()
splash_width = 1149 
splash_height = 674
splash_screen_width = root_splash.winfo_screenwidth()  
splash_screen_height = root_splash.winfo_screenheight() 
splash_x = (splash_screen_width/2) - (splash_width/2)
splash_y = (splash_screen_height/2) - (splash_height/2)
root_splash.geometry('%dx%d+%d+%d' % (splash_width, splash_height, splash_x, splash_y))
root_splash.overrideredirect(True) # Hide the title bar
root_splash.resizable(False, False)

# Set Image and Label
##-----------------------------------------------------------------------------
splash_image = Image.open(findPath(base_path=pathlib.Path().resolve(), isdir=False, name="splash.png", listdir=False))
splash_img = ImageTk.PhotoImage(splash_image)
splash_label = Label(root_splash, image=splash_img, borderwidth=0)
splash_label.image = splash_img
splash_label.pack()

# Set Interval
##-----------------------------------------------------------------------------
root_splash.after(3000, Login_Screen)


##---- Launch App
##-----------------------------------------------------------------------------
mainloop()
