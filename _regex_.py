import os
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
import re, random, string


def last_n_char(String, n):
    length = len(String)
    return String[length - n :]


def file_extension(String):
    if len(String.split(".")) < 2:
        new_string = String.split(".")[0]
    elif len(String.split(".")) == 2:
        new_string = "." + String.split(".")[1]
    elif len(String.split(".")) > 2:
        new_string = String[String.rfind("."):len(String)].strip()
    return new_string


def containsAnyAlpha(str):
    # initializing flag variable
    n = False

    # checking for letter in string
    for string in str:

        # if string has letter
        if string.isalpha():
            n = True
    return n



def containsAnyDigit(str):
    # initializing flag variable
    n = False

    # checking for number in string
    for string in str:

        # if string has letter
        if string.isdigit():
            n = True
    return n



def formatNegative(x):
    if x == "":
        value = ""
    else:
        value = str(round(x, 2))
        if "-" in value:
            value = value.replace("-", "(") + ")"
    return value



