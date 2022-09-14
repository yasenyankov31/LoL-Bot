import win32gui

while True:
    hwnd = win32gui.FindWindow(None, 'League of Legends (TM) Client')
    print(hwnd)