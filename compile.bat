rmdir dist
python -m eel --onefile --clean --uac-admin  main.py front

rename dist\main.exe module_pn6280_control.exe

xcopy cmds  /E dist\cmds\
xcopy data dist\data\
