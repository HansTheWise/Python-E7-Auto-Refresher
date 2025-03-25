import ctypes
from ctypes import wintypes
import time
TARGET_GAME = "Epic Seven"

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_MOVE = 0x0001

TARGET_X_POS = "x_pos" 
TARGET_Y_POS = "y_pos"
TARGET_WIDTH = "width"
TARGET_HEIGHT = "height"

VK_LBUTTON = 0x01  # Linke Maustaste
VK_RBUTTON = 0x02  # Rechte Maustaste

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

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
    

    def __init__(self):
        #open ui
        #setup connections
        self.screen_width = user32.GetSystemMetrics(0)  # Bildschirmbreite
        self.screen_height = user32.GetSystemMetrics(1)  # Bildschirmhöhe
        self.event_counter = 0
        self.wnd_stats = {
            TARGET_X_POS: 0,
            TARGET_Y_POS: 0,
            TARGET_WIDTH: 0,
            TARGET_HEIGHT: 0
        }

    def sync_target_info(self):
            self.hwnd = user32.FindWindowW(None, TARGET_GAME)
            if self.hwnd == 0:
                raise Exception("EPIC SEVEN IST NICHT OFFEN!")
            
            rect = wintypes.RECT()
            user32.GetWindowRect(self.hwnd, ctypes.byref(rect))

            new_values = {
                TARGET_X_POS: rect.left,
                TARGET_Y_POS: rect.top,
                TARGET_WIDTH: rect.right - rect.left,
                TARGET_HEIGHT: rect.bottom - rect.top
            }
            for key, value in new_values.items():
                if self.wnd_stats[key] != value:
                    self.wnd_stats[key] = value

            print(f"Position: ({self.wnd_stats[TARGET_X_POS]}, {self.wnd_stats[TARGET_Y_POS]})")
            print(f"Größe: {self.wnd_stats[TARGET_WIDTH]} x {self.wnd_stats[TARGET_HEIGHT]}")
            print("-" * 40)
            

    def capture_pixels(self):
        hdc = user32.GetDC(self.hwnd)
        if not hdc:
            raise RuntimeError("Failed to acquire DC!")
        
                # Create a compatible DC and bitmap to store pixels
        mem_hdc = gdi32.CreateCompatibleDC(hdc)
        bitmap = gdi32.CreateCompatibleBitmap(hdc, self.wnd_stats[TARGET_WIDTH], self.wnd_stats[TARGET_HEIGHT] )
        gdi32.SelectObject(mem_hdc, bitmap)

        gdi32.BitBlt(mem_hdc, 0, 0, self.wnd_stats[TARGET_WIDTH], self.wnd_stats[TARGET_HEIGHT],
                     hdc, self.wnd_stats[TARGET_X_POS], self.wnd_stats[TARGET_Y_POS], gdi32.SRCCOPY  # source copy kopiermodus für pixelkopie
                     )


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
        active_mouse = self.check_active_mouse()
        if active_mouse == False:
            self.click_event(x, y)
    
    def get_cursor_pos(self):
        pt = wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    def set_cursor_pos(self, x, y):
        user32.SetCursorPos(x, y)
        
    def convert_coordinats(self,x,y):
        abs_x = int(x * 65535 / self.screen_width)
        abs_y = int(y * 65535 / self.screen_height)
        return abs_x, abs_y

    def click_event(self,target_x, target_y):
        """Simuliert einen Mausklick an (x, y) ohne sichtbare Mausbewegung"""
        
        abs_x, abs_y = self.convert_coordinats(target_x, target_y)
        
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

        curr_x, curr_y = self.get_cursor_pos()
        user32.SendInput(3, ctypes.byref(inputs), ctypes.sizeof(INPUT))
        self.set_cursor_pos(curr_x, curr_y)
        
        self.event_counter += 1
        
        time.sleep(0.5)
    
    def match_click_event(self, event):
        match event:
            case "buy":
                #bild anlyse
                
                in_use = self.check_active_mouse()
                if in_use == False:
                    self.sync_target_info()
                    self.click_event()
                    return
            case "refresh":
                in_use = self.check_active_mouse()
                if in_use == False:
                    self.sync_target_info()
                    self.click_event()
                return
            case "confire":
                in_use = self.check_active_mouse()
                if in_use == False:
                    self.sync_target_info()
                    self.click_event()
            case _:
                print("Unknown event type")
                return
    
    def drag_event(self,target_x, target_y, dst_x, dst_y):
        
        abs_tx, abs_ty = self.convert_coordinats(target_x, target_y)
        abs_dx, abs_dy = self.convert_coordinats(dst_x, dst_y)
        inputs = (INPUT * 4)()

        inputs[0].type = 0
        inputs[0].mi = MOUSEINPUT(abs_tx, abs_ty, 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, 0, None)

        inputs[1].type = 0
        inputs[1].mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, None)

        inputs[2].type = 0
        inputs[2].mi = MOUSEINPUT(abs_dx, abs_dy, 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, 0, None)
        
        inputs[3].type = 0
        inputs[3].mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, None)

        curr_x, curr_y = self.get_cursor_pos()
        user32.SendInput(3, ctypes.byref(inputs), ctypes.sizeof(INPUT))
        self.set_cursor_pos(curr_x, curr_y)
        
        self.event_counter += 1
        
        time.sleep(0.5)

if __name__ =="__main__":
    tri = Auto_refresher()
    tri.test_function(100, 100)

    # asdasdas