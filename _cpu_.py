import os
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
import time
import psutil
import win32process
import subprocess, re, string, pandas as pd, sys
from io import StringIO
import pathlib
from _directory_ import findPath
from _regex_ import file_extension




def process_runningByPath(processName, path_to_file):
    for proc in psutil.process_iter(['name']):
        if proc.name() in processName:
            for path in proc.cmdline():
              if path_to_file in path:
                  return True
    return False




def process_runningByPartialName(processName, partial_name):
    PIDs = []
    for proc in psutil.process_iter(['name']):
      if proc.name() in processName:
          for sub_proc in proc.cmdline():
              if partial_name in sub_proc:
                  PIDs.append(proc.pid)
    return PIDs




def quickKill(processName, filePath):
    if len(re.findall(pattern=r"\\", string=filePath)) > 0:
        file_Basename = os.path.basename(filePath).replace(file_extension(os.path.basename(filePath)), "")
    else:
        file_Basename = filePath
    for proc in psutil.process_iter(['name']):
      if proc.name() in processName:
          for sub_proc in proc.cmdline():
              if file_Basename in sub_proc:
                  proc.kill()


def startProcess(programParam=None, processName=None, fileParam=None):
    # Path and name of the program you want to start\
    if fileParam != None:
        # Close Any Processes that Are Currently Open
        if processName == None:
            processes = ["pyw.exe", "pythonw.exe", "python.exe", ".py"]
            quickKill(processName = processes, filePath=fileParam)
            time.sleep(1)
        else:
            quickKill(processName = processName, filePath=fileParam)
            time.sleep(1)
            
        # Create a subprocess with the program
        subprocess.Popen([programParam, fileParam], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
  
  

def vpn_connection_status():
    interfaces = psutil.net_if_addrs()
    for interface_name, interface_addresses in interfaces.items():
        if interface_name == "Ethernet 3":
            for address in interface_addresses:
                if address.family == psutil.AF_LINK and not address.address.startswith('127'):
                    return "Connected"
    return "Disconnected"























### Old
##----------------------------------------------------------------
##        Function to Get Running Process by Partial Name       --
##----------------------------------------------------------------
# def process_runningByPartialName(processName, partial_name):
#   PIDs = []
#   process_status = [ proc for proc in psutil.process_iter() if proc.name() in processName ]
#   for current_process in process_status:
#     try:
#       if len([f for f in current_process.cmdline() if partial_name in f]) > 0:
#         PIDs.append(current_process.pid) 
#       else:
#         []
#     except psutil.NoSuchProcess:
#       []
#   return PIDs

##---------------------------------------------------------------
##          Find If VPN Is Connected
##---------------------------------------------------------------
# # -- Version 1
# def vpn_connection_status():
#   import os, subprocess, re, string, pandas as pd
#   # ipconfig /all
#   p = subprocess.Popen(['powershell.exe', "netsh interface show interface"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#   output = list(p.communicate(b"input data that is passed to subprocess' stdin"))
#   mod_output = output[0]
#   line = mod_output.decode()
#   line = line.rstrip()
#   line = line.replace('\r', '')
#   line = line.replace('\n', '')
#   # Remove Start to Ethernet 2
#   mod_str = line[re.search(r'Ethernet 2', line).span()[1]:]
#   # Remove From Ethernet 3 onwards
#   try:
#     new_str = mod_str[:len(mod_str) - re.search(r'Ethernet 3', mod_str).span()[1]]
#     line_str = new_str.split("  ")
#     while('' in line_str):
#       line_str.remove('')
#     df = pd.DataFrame(columns = ['Admin State', 'State', 'Type', 'Interface Name'])
#     df.loc[1]=line_str
#     # Check If Connected
#     return df['State'].values[0]
#   except ValueError:
#     if re.findall(pattern="Connected", string=mod_str, flags=0) == []:
#      ret_string = re.findall(pattern="Disconnected", string=mod_str, flags=0)
#     elif re.findall(pattern="Disconnected", string=mod_str, flags=0) == []:
#       ret_string = re.findall(pattern="Connected", string=mod_str, flags=0)
#     return ret_string[0].strip()

# # -- Version 2
# def vpn_connection_status():
#   process = subprocess.Popen(['powershell.exe', "netsh interface show interface"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#   output = list(process.communicate(b"input data that is passed to subprocess' stdin"))[0].decode()
#   df = pd.read_csv(StringIO(output), sep=";")
#   # colNames = [x.strip() for x in "".join(df.columns.values.tolist()).split("  ") if x != '']
#   for i in df.itertuples():
#     if "Ethernet 3" in df.at[i.Index, df.columns.values[0]]:
#       result = df.at[i.Index, df.columns.values[0]]
#       break
#   try:
#     return [x.strip() for x in result.split(sep="  ") if x != ''][1].strip()
#   except:
#     return "Disconnected"


# def process_runningByPath(processName, path_to_file):
#   process_status = [ proc for proc in psutil.process_iter() if proc.name() == processName ]
#   for current_process in process_status:
#     try:
#       if current_process.cmdline()[-1].strip() == path_to_file:
#         x = True
#       else:
#         x = False
#     except psutil.NoSuchProcess:
#       x = False
#   return x

##----------------------------------------------------------------
##        Function to Kill Process
##----------------------------------------------------------------
# def killSwitch(watching):
#   pidList = process_runningByPartialName(processName=["pyw.exe", "pythonw.exe", "python.exe"], partial_name=watching)
#   if len(pidList) > 0:
#     [os.system(f'taskkill /PID {f} /F') for f in pidList]
#   else:
#     pass
# def killSwitch(watching):
#   pidList = process_runningByPartialName(processName=["pyw.exe", "pythonw.exe", "python.exe", ".py"], partial_name=watching)
#   if len(pidList) > 0:
#     [os.system(f'taskkill /PID {f} /F') for f in pidList]
#   else:
#     pass
# [os.system(f'taskkill /PID {f} /F') for f in _cpu_.process_runningByPartialName(processName=["pyw.exe", "pythonw.exe",  "python.exe"], partial_name="Vryonisyrnaoutsopoula94080")]
