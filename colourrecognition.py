import win32gui
import win32ui
import win32con
import numpy as np
from ctypes import windll, byref, c_int
import time
from event_cases import Scrip_Modules

# Force DPI awareness

"""
testen ob die farbe für book marks nur einmal auftritt 
    vielleicht mit 1-5 wertabweichung um kompremirung zu beachten
    --> benötig keine bilderkennung
als scaling einen sehr großen wert 100000 zu 100000 oder noch größer für genauen ramen
wenn wir nur nach einem value schauen haben wir konstanten aufwand eine line pixel wären ca 1000+ vergleiche
wenn dann noch in 5 abschnitte unterteilt dann maybe 500+- kommt auf festergröße an maybe festlegen?

items haben rahmen, dieser hat glaube immer die selbe farbe, können wir die position des rahmens bestimmen so wissen wir
die position des items innerhalb
"""

windll.user32.SetProcessDPIAware()


def capture_window(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        raise ValueError(f"Window '{window_title}' not found")

    # funktion schon vorhanden
    check = Scrip_Modules.is_window_foreground(hwnd)
    if not check:
        print("fenster nicht gefunden")
        return
    
    # Get client area dimensions
    rect = win32gui.GetClientRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

    # Create device context
    hdc = win32gui.GetWindowDC(hwnd)
    dc = win32ui.CreateDCFromHandle(hdc)
    mem_dc = dc.CreateCompatibleDC()

    # Create bitmap
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(dc, width, height)
    mem_dc.SelectObject(bitmap)

    # Capture using PrintWindow with retries
    for _ in range(3):
        result = windll.user32.PrintWindow(hwnd, mem_dc.GetSafeHdc(), 2)
        if result:
            break
        time.sleep(0.1)

    # Convert to numpy array
    pixel_bytes = bitmap.GetBitmapBits(True)
    pixel_array = np.frombuffer(pixel_bytes, dtype=np.uint8)

    # Cleanup
    dc.DeleteDC()
    mem_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)
    win32gui.DeleteObject(bitmap.GetHandle())

    return pixel_array.reshape((height, width, 4))[:, :, 2::-1]  # BGRA -> RGB


# Usage example
if __name__ == "__main__":
    try:
        pixels = capture_window("Epic Seven")

        # Analyze captured data
        print("Capture stats:")
        print(f"Total pixels: {pixels.size // 3}")
        print(f"Zero pixels: {np.all(pixels == 0, axis=2).sum()}")
        print(f"Non-zero pixels: {np.any(pixels != 0, axis=2).sum()}")
        print("Sample non-zero area:")


        print(pixels[100:105, 100:105])  # Adjust coordinates as needed

    except Exception as e:
        print(f"Error: {e}")