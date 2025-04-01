from event_cases import Scrip_Modules
import colourrecognition 
import ctypes
import os
from ctypes import wintypes
import time
from PyQt6 import QtWidgets, uic
from PyQt6 import QtCore
import re

UI_NAME = "e7_refresher.ui"

class Auto_Script(Scrip_Modules, colourrecognition):

    
    
    def __init__(self):
        super().__init__()
        self.skystone_amount = 0
        self.create_session()

    def create_session(self):
        self.load_ui()
        self.connect_buttons()
        self.set_styles()
        
        def load_ui(self):
            position = os.path.abspath(__file__) 
            script_dir = os.path.dirname(position) 
            ui_path = os.path.join(script_dir, UI_NAME)
            uic.loadUi(ui_path, self)
            
        def connect_buttons(self):
            self.start_button.clicked.connect(lambda: self.start_session())
            self.pause_button.clicked.connect(lambda: self.pause_session())
            self.stop_button.clicked.connect(lambda: self.stop_session())
        
        def set_styles(self):
            uwu = "shit"   
    
    
    def start_session(self):
        
        def verify_sky_amount(skystone_input):
            skystone_pattern = r'^\d[2,7]$'
            if not re.match(skystone_pattern, skystone_input):
                return 0 ,False
            return int(skystone_input), True
        
        skystone_input = self.skystone_input.text()
        self.skystone_amount, check = verify_sky_amount(skystone_input)
        if check == False:
            self.skystone_input.setText("wrong input!")
        
    def pause_session(self):
        None
    def stop_session(self):
        None
    def update_log(self):
        None
    def update_loot_per_sky(self):
        None
    
if __name__ == "__main__":
    test = Auto_Script()
    