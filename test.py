import ctypes
from ctypes import wintypes
import time
TARGET_GAME = "Epic Seven"

user32 = ctypes.windll.user32
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_MOVE = 0x0001

VK_LBUTTON = 0x01  # Linke Maustaste
VK_RBUTTON = 0x02  # Rechte Maustaste

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long), #absolute ziel koordinaten für die maus
        ("dy", ctypes.c_long), #absolute ziel koordinaten für die maus
        ("mouseData", ctypes.c_ulong), #mausrad brauchen wir nicht
        ("dwFlags", ctypes.c_ulong), #was wir machen möchte zbsp click, bewegung etc
        ("time", ctypes.c_ulong), #kann für zeitstempel genutzt werden brauchen wir nicht?
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)) #auch nicht benötigt
    ]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("mi", MOUSEINPUT)] #type gibt art des inputs an [0] ist INPUT_MOUSE

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
                self.get_target_informations(hwnd)
                n+=1
                time.sleep(0.5)
        
    def get_target_informations(self, hwnd):
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))

            x, y = rect.left, rect.top
            width = rect.right - rect.left
            height = rect.bottom - rect.top

            print(f"Position: ({x}, {y})")
            print(f"Größe: {width} x {height}")
            print("-" * 40)
            
    def check_active_mouse(self):
            in_use = False
            # Überprüfen, ob die linke Maustaste gedrückt ist
            if user32.GetAsyncKeyState(VK_LBUTTON) & 0x8000:
                in_use = True
                print("Linke Maustaste gedrückt!")
            # Überprüfen, ob die rechte Maustaste gedrückt ist
            if user32.GetAsyncKeyState(VK_RBUTTON) & 0x8000:
                in_use = True
                print("Rechte Maustaste gedrückt!")
            return in_use

    def check_content(self):
        i = 0
        
    def input_test(self):
        i = 0

    def target_window_visible():
        fill_out = None
        
    def test_function(self, x, y):
        self.screen_width = user32.GetSystemMetrics(0)  # Bildschirmbreite
        self.screen_height = user32.GetSystemMetrics(1)  # Bildschirmhöhe
        active_mouse = self.check_active_mouse()
        if active_mouse == False:
            self.click_event(x, y)

    def click_event(self,x, y):
        """Simuliert einen Mausklick an (x, y) ohne sichtbare Mausbewegung"""
        def get_cursor_pos():
            pt = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(pt))
            return pt.x, pt.y

        def set_cursor_pos(x, y):
            user32.SetCursorPos(x, y)
    
        abs_x = int(x * 65535 / self.screen_width)
        abs_y = int(y * 65535 / self.screen_height)
        
        #wir erstellen 3 inputs
        inputs = (INPUT * 3)() #die klammer dahintert sorgt dafür das wir das array erstelle und nicht nur definieren

        # Unsichtbare Bewegung zur Position (x, y)
        inputs[0].type = 0  # INPUT_MOUSE
        inputs[0].mi = MOUSEINPUT(abs_x, abs_y, 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, 0, None) #wir übergeben die daten für das field

        # Linksklick drücken
        inputs[1].type = 0
        inputs[1].mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, None)

        # Linksklick loslassen
        inputs[2].type = 0
        inputs[2].mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, None)

        c_x, c_y = get_cursor_pos()
        user32.SendInput(3, ctypes.byref(inputs), ctypes.sizeof(INPUT))
        set_cursor_pos(c_x, c_y)
        time.sleep(0.5)

if __name__ =="__main__":
    tri = Auto_refresher()
    tri.test_function(100, 100)