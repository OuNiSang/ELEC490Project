# NOTE: keep this file under the .ui directory, 
# which can convert .ui into .py

import os
import os.path

#dir of file 
dir = './GUI_Source'

#list all the .ui file under dir 
def ListUiFile():
    ls = []
    files = os.listdir(dir)
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
        pyFile = Ui2PyFilename(uiFile)  #TODO still facing error of finding .ui files 
        cmd = 'pyuic5 {uiFile} > {pyFile} '.format(pyFile = pyFile, uiFile = uiFile)
        print(cmd)
        os.system(cmd)

if __name__ == "__main__":
    runMain()