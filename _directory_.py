import os
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
import os.path, random, string, tempfile, shutil



def findPath(base_path, isdir, name, listdir):
    if isdir == True and listdir == True:
        for root, dirs, files in os.walk(base_path):
            if os.path.basename(root) == name:
                i = root
                return full_path(i)
    elif isdir == True and listdir == False:
        for root, dirs, files in os.walk(base_path):
            if os.path.basename(root) == name:
                i = root
                return i
    elif isdir == False and type(listdir) == bool:
        for root, dirs, files in os.walk(base_path):
            for filename in files:
                if filename == name:
                    return os.path.join(root, filename)



def py_temp_dir():
    temp_folder_name = ".Py_Temp_Directory-" + "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
    )
    os.makedirs(os.path.join(tempfile.gettempdir(), temp_folder_name))
    temp_folder_location = os.path.join(tempfile.gettempdir(), temp_folder_name)
    return temp_folder_location
 



def Rpy_temp_dir(removeAll=False, identifier=None):
    if (removeAll == False) and (identifier == None):
        temp_folder_name = ".Rpy_Temp_Directory-" + "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(12)
        )
        os.makedirs(os.path.join(tempfile.gettempdir(), temp_folder_name))
        temp_folder_location = os.path.join(tempfile.gettempdir(), temp_folder_name)
        return temp_folder_location

    elif (removeAll == False) and (identifier != None):
        temp_folder_name = (
            ".Rpy_Temp_Directory-"
            + identifier
            + "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(12)
            )
        )
        os.makedirs(os.path.join(tempfile.gettempdir(), temp_folder_name))
        temp_folder_location = os.path.join(tempfile.gettempdir(), temp_folder_name)
        return temp_folder_location

    elif removeAll == True:
        import shutil

        identifier = None
        temp_path = os.path.join(tempfile.gettempdir())
        files_in_temp_path = os.listdir(temp_path)
        temp_dirs = [
            word for word in files_in_temp_path if ".Rpy_Temp_Directory-" in word
        ]
        for temp in temp_dirs:
            found = os.path.join(tempfile.gettempdir(), temp)
            shutil.rmtree(found)
    else:
        pass


def full_path(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory)]


def remove_gen_pyPath():
    gen_py_file = [f for f in os.listdir(os.getenv("TEMP")) if f == "gen_py"]
    if gen_py_file == []:
        pass
    else:
        shutil.rmtree(
            os.path.join(
                os.getenv("TEMP"),
                "".join([f for f in os.listdir(os.getenv("TEMP")) if f == "gen_py"]),
            )
        )


def remove_TempDir():
    temp_path = os.path.join(tempfile.gettempdir())
    files_in_temp_path = os.listdir(temp_path)
    temp_dirs = [word for word in files_in_temp_path if ".Py_Temp_Directory-" in word]
    for temp in temp_dirs:
        found = os.path.join(tempfile.gettempdir(), temp)
        shutil.rmtree(found)


def remove_R_TempDir():
    temp_path = os.path.join(tempfile.gettempdir())
    files_in_temp_path = os.listdir(temp_path)
    r_dirs = [word for word in files_in_temp_path if ".R_Temp_Directory-" in word]
    for temp in r_dirs:
        found = os.path.join(tempfile.gettempdir(), temp)
        shutil.rmtree(found)

