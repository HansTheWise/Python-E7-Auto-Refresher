import ctypes
from ctypes import wintypes
import time
TARGET_GAME = "Epic Seven"

user32 = ctypes.windll.user32

class Auto_refresher():
    
    #def __init__(self):
        #open ui
        #setup connections

    def search_for_target_window(self ,target):
        length = 256
        buffer = ctypes.create_unicode_buffer(length)
        window_title = ""
        n = 1
        while window_title != target:
                hwnd = user32.GetForegroundWindow()
                user32.GetWindowTextW(hwnd, buffer, length)
                window_title = buffer.value
                print(f"try: {n} wrong window: {window_title}")
                self.get_target_informations(hwnd, window_title)
                n+=1
                time.sleep(0.5)
        
    def get_target_informations(hwnd, window_title):
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))

            x, y = rect.left, rect.top
            width = rect.right - rect.left
            height = rect.bottom - rect.top

            print(f"Aktives Fenster: {window_title}")
            print(f"Position: ({x}, {y})")
            print(f"Größe: {width} x {height}")
            print("-" * 40)

if __name__ =="__main__":
    instanz = Auto_refresher()
    instanz.search_for_target_window(TARGET_GAME)