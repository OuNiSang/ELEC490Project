# NOTE: keep this file under the .ui directory, 
# which can convert .ui into .py

import os
import os.path

#dir of file 
dir_ui = './Scripts/UI_Files'
dir_py = './Scripts/PY_Files'

#list all the .ui file under dir 
def ListUiFile():
    ls = []
    files = os.listdir(dir_ui)
    for filename in files: 
        # print(dir + os.sep + filename)

        if os.path.splitext(filename)[1] == '.ui':
            ls.append(filename)
    print("Detected: ",ls)
    return ls

#turn .ui file into .py file
def Ui2PyFilename(filename):
    return 'UI_'+os.path.splitext(filename)[0] + '.py'

#use concel to turn .ui into .py
def runMain():
    ls = ListUiFile()
    for uiFile in ls:
        pyFile = Ui2PyFilename(uiFile)  
        cmd = 'pyuic5 {dir_ui}/{uiFile} > {dir_py}/{pyFile} '.format(pyFile = pyFile, dir_ui = dir_ui, dir_py = dir_py, uiFile = uiFile)
        print(cmd)
        os.system(cmd)

if __name__ == "__main__":
    runMain()