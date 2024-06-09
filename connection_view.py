import tkinter as tk
from tkinter import DISABLED, LEFT, StringVar, ttk
from PIL import Image, ImageTk
from wifi import *
import subprocess
import constants

class ConnectionView(tk.Frame):

    def __init__(self, master: tk.Tk, *args):
        super().__init__(master, args)
        
        #miembros
        self.wifi_list = []
        self.current_wifi = None

        try:
            self.wifi_list = Cell.all('wlan0')
        except:
            pass

        self.wifi_icon_1 = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_1_icon_google.png")
        self.wifi_icon_2 = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_2_icon_google.png")
        self.wifi_icon_3 = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_3_icon_google.png")
        self.wifi_icon_4 = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_4_icon_google.png")
        self.wifi_off_icon = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_off_icon_12p.png")

        current_wifi_name = ""
        try:
            current_wifi_name = subprocess.check_output(['sudo', 'iwgetid']).decode().split('"')[1]
        except:
            pass
        
        for network in self.wifi_list:
            if (network.ssid == current_wifi_name):
                self.current_wifi = network
                break

        #layout
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 4)
        self.columnconfigure(0, weight = 1)
        
        # frame superior - red actual
        self.upper_frame = tk.Frame(self, bg= "green")
        self.upper_frame.grid(row = 0,
                              column = 0,
                              columnspan = 1,
                              sticky = "nwe",
                              padx = (10, 10),
                              pady = (10, 5))
        
        self.upper_frame.rowconfigure(0, weight = 1)
        self.upper_frame.columnconfigure(0, weight = 1)
        
        if not (self.current_wifi is None):
            self.current_con_label = tk.Label(self.upper_frame,
                                        image = self.__get_signal_quality_icon(self.current_wifi.signal),
                                        compound = LEFT,
                                        text = " Connected to " + self.current_wifi.ssid,
                                        font = constants.data_label_font_mini)
        else:
            self.current_con_label = tk.Label(self.upper_frame,
                                        image = self.wifi_off_icon,
                                        compound = LEFT,
                                        text = " Please select a network!",
                                        font = constants.data_label_font_mini)
        
        self.current_con_label.grid(row = 0,
                              column = 0,
                              columnspan = 1,
                              sticky = "nwe")
    
    def __get_signal_quality_icon(self, dBm: int):
        quality = 0
        if (dBm <= -100):
            quality = 0
        elif (dBm >= -50):
            quality = 100
        else:
            quality = 2 * (dBm + 100)
        
        if (quality < 25):
            return self.wifi_icon_1
        elif (quality < 50):
            return self.wifi_icon_2
        elif (quality < 75):
            return self.wifi_icon_3
        else:
            return self.wifi_icon_4