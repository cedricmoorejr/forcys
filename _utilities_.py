import os
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
import numpy as np
from tkinter import Label
from PIL import Image, ImageTk
from itertools import count, cycle
from win32api import *
from win32gui import *
import win32con
import sys
import struct
import time
import ctypes






class PhotoImage_GIF(Label):
    def Open(self, photo_image):
        if isinstance(photo_image, str):
            photo_image = Image.open(photo_image)
        photo_frames = []
        try:
            for num in count(1):
                photo_frames.append(ImageTk.PhotoImage(photo_image.copy()))
                photo_image.seek(num)
        except EOFError:
            pass
        self.photo_frames = cycle(photo_frames)
        try:
            self.delay = photo_image.info["duration"]
        except:
            self.delay = 100
        if len(photo_frames) == 1:
            self.config(image=next(self.photo_frames))
        else:
            self.NextImage()

    def Close(self):
        self.config(image=None)
        self.photo_frames = None

    def NextImage(self):
        if self.photo_frames:
            self.config(image=next(self.photo_frames))
            self.after(self.delay, self.NextImage)





##---------------------------------------------------------------
##            Remove Double Brackets From List         --
##---------------------------------------------------------------
def flatten_list(list1):
  flattened = [] 
  for sublist in list1: 
    for val in sublist: 
      flattened.append(val) 
  return flattened


##----------------------------------------------------------------
##        Find Missing Elements Between Two Lists 			        --
##----------------------------------------------------------------
def missing(List1, List2):
	return [x for x in List1 if x not in List2]


##----------------------------------------------------------------
##        					Force Nan Value			        --
##----------------------------------------------------------------
def nan():
  return list(np.ones(np.array([1, 3, 4, 6, 9])[-1])*np.NaN)[0]





##----------------------------------------------------------------
##        				Create Windows Popup			        --
##----------------------------------------------------------------
def WindowsNotify():
    # Icon styles
    MessageBox_ICON_ERROR = 0x10
    MessageBox_ICON_WARNING = 0x30
    MessageBox_ICON_INFO = 0x40

    # Button styles
    MessageBox_OK = 0x0
    MessageBox_OKCANCEL = 0x1
    MessageBox_YESNO = 0x4
    MessageBox_YESNOCANCEL = 0x03
    MessageBox_HELP = 0x4000
    ctypes.windll.user32.MessageBoxW(
        0,
        "You are disconnected from VPN! \n As a result, the program will not start.",
        "Attention!",
        MessageBox_ICON_WARNING | MessageBox_OK,
    )
