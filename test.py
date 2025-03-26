import ctypes
from ctypes import wintypes
import time

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

class Events:
    BUY = "BUY"
    REFRESH = "REFRESH"
    CONFIRM = "CONFIRM"
    DRAG = "DRAG"
    
class E7_Pos:
    REFRESH_X = 30
    REFRESH_Y = 82
    
    CONFIRM_X = 92
    CONFIRM_Y = 58
    
    DRAG_START_X = None
    DRAG_START_Y = None
    DRAG_DST_X = None
    DRAG_DST_Y = None

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

TARGET_GAME = "Epic Seven"

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

class Scrip_Modules():
    

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
        
    def find_window(self, target):
        
        hwnd = user32.FindWindowW(None, target)
        if hwnd == 0:
            print("EPIC SEVEN IST NICHT OFFEN!")
            return None, False
        return hwnd, True
    
    def _sync_target_info(self):
            
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
        
    def is_window_foreground(self ,target_hwnd):
            # Get the handle of the currently foreground window
            foreground_hwnd = user32.GetForegroundWindow()
            if not target_hwnd == foreground_hwnd:
                self._bring_target_to_foreground()
                return True
            return target_hwnd == foreground_hwnd    

    def _bring_target_to_foreground(self):
        # Make sure self.hwnd is set
        if not self.hwnd:
            raise Exception("Target window handle is invalid.")
            
        # Optionally restore the window if it is minimized:
        SW_RESTORE = 9
        user32.ShowWindow(self.hwnd, SW_RESTORE)
        
        # Bring the window to the foreground
        result = user32.SetForegroundWindow(self.hwnd)
        
        if not result:
            raise Exception("Failed to bring target window to the foreground!") 
            

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

    def test_function(self):
            self.match_event(Events.REFRESH)
            self.match_event(Events.CONFIRM)
    
    def get_cursor_pos(self):
        pt = wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    def set_cursor_pos(self, x, y):
        user32.SetCursorPos(x, y)
        
    def convert_coordinats(self,x,y):
        abs_x = int((x / self.screen_width) * 65535)
        abs_y = int((y / self.screen_height) * 65535)
        return abs_x, abs_y
    
    def control_checks(self):
        self.hwnd, exists = self.find_window(TARGET_GAME)
        if exists == False:
            print("kein fenster")
            return False
        on_screen = self.is_window_foreground(TARGET_GAME)
        in_use = self.check_active_mouse()
        print(f"exists: {exists}, on_screen: {on_screen}, in_use: {in_use}")
        if in_use == False and on_screen == True:
            self._sync_target_info()
            return True
        else: 
            return False
    
    def get_click_position(self, x, y):
        pixel_x = self.wnd_stats[TARGET_X_POS] + int((x/160) * self.wnd_stats[TARGET_WIDTH])
        pixel_y = self.wnd_stats[TARGET_Y_POS] + int((y/90) * self.wnd_stats[TARGET_HEIGHT])
        print(f"target area ({pixel_x},{pixel_y})")
        return pixel_x, pixel_y
    
    def match_event(self, event):
        check = self.control_checks()
        time.sleep(0.5)
        if check == False:
            return
        
        match event:
            case Events.BUY:
                #bild anlyse
                #x, y = david seine funktio
                self.click_event(x, y)
                
            case Events.REFRESH:
                print(f"refreshing")
                x, y = self.get_click_position(E7_Pos.REFRESH_X, E7_Pos.REFRESH_Y)
                self.click_event(x, y)
                    
            case Events.CONFIRM:
                x, y = self.get_click_position(E7_Pos.CONFIRM_X, E7_Pos.CONFIRM_Y)
                self.click_event(x, y)
                
            case Events.DRAG:
                start_x, start_y = self.get_click_position(E7_Pos.DRAG_START_X, E7_Pos.DRAG_START_Y)
                dst_x, dst_y = self.get_click_position(E7_Pos.DRAG_DST_X, E7_Pos.DRAG_START_Y)
                self.drag_event(start_x, start_y, dst_x, dst_y)
                
            case _:
                print("Unknown event type")

    def click_event(self,target_x, target_y):
        """Simuliert einen Mausklick an (x, y) ohne sichtbare Mausbewegung"""
        
        abs_x, abs_y = self.convert_coordinats(target_x, target_y)
        print(f"absolute coords = {abs_x},{abs_y}")
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
        user32.SendInput(3, inputs, ctypes.sizeof(INPUT))
        #if result != 3:
        #    print(f"Fehler bei SendInput. Erwartet: 3, Gesendet: {result}")
        #else:
            #print("Klick erfolgreich ausgeführt.")
        self.set_cursor_pos(curr_x, curr_y) 
   
        time.sleep(0.5)
    
    
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
        user32.SendInput(3, inputs, ctypes.sizeof(INPUT))
        self.set_cursor_pos(curr_x, curr_y)        
        time.sleep(0.5)

if __name__ =="__main__":
    script = Scrip_Modules()
    script.test_function()

    # asdasdas