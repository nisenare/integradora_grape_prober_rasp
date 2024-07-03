import threading
import tkinter as tk
from tkinter import DISABLED, END, LEFT, RIGHT, Y, StringVar, Toplevel, ttk
from PIL import Image, ImageTk
from wifi import *
import subprocess
import signal
import os
import constants
import onboard_keyboard
import connection

class ConnectionView(tk.Frame):

    def __init__(self, master: tk.Tk, *args):
        super().__init__(master, args)
        
        #miembros
        self.wifi_list = []
        self.current_wifi = None
        self.wifi_icon_1 = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_1_icon_google.png")
        self.wifi_icon_2 = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_2_icon_google.png")
        self.wifi_icon_3 = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_3_icon_google.png")
        self.wifi_icon_4 = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_4_icon_google.png")
        self.wifi_off_icon = tk.PhotoImage(file = constants.absolute_path + "resource/icon/network_wifi_off_icon_12p.png")

        #layout
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 6)
        self.columnconfigure(0, weight = 1)
        
        # frame superior - red actual
        self.upper_frame = tk.Frame(self)
        self.upper_frame.grid(row = 0,
                              column = 0,
                              columnspan = 1,
                              sticky = "nswe",
                              padx = (10, 10),
                              pady = (10, 5))
        
        self.upper_frame.rowconfigure(0, weight = 1)
        self.upper_frame.columnconfigure(0, weight = 1)
        
        self.current_con_label = tk.Label(
            self.upper_frame,
            compound = LEFT,
            font = constants.data_label_font_mini)
        
        self.current_con_label.grid(row = 0,
                              column = 0,
                              columnspan = 1,
                              sticky = "nwe")

        # frame inferior, lista de redes
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(row = 1,
                               column = 0,
                               columnspan = 1,
                               sticky = "nswe",
                               padx = (10, 10),
                               pady = (5, 10))
        
        self.bottom_frame.rowconfigure(0, weight = 6)
        self.bottom_frame.rowconfigure(1, weight = 1)
        self.bottom_frame.columnconfigure(0, weight = 1)

        self.av_networks_list = ttk.Treeview(self.bottom_frame)
        self.av_networks_list.heading("#0", text="Available networks")

        self.style = ttk.Style(self)
        self.style.configure('Treeview', rowheight = 45, font = constants.data_label_font_mini)
        self.style.configure("Vertical.TScrollbar", arrowsize = 40)

        self.tree_scroll = ttk.Scrollbar(self.bottom_frame, style = "TScrollbar")
        self.tree_scroll.configure(command=self.av_networks_list.yview)

        self.av_networks_list.configure(yscrollcommand=self.tree_scroll.set)

        self.av_networks_list.grid(row = 0,
                                   column = 0,
                                   columnspan = 1,
                                   sticky = "nswe")
        self.tree_scroll.grid(row = 0,
                                column = 1,
                                columnspan = 1,
                                sticky = "nswe")
        self.top = None
        self.av_networks_list.bind("<Double-Button-1>", self.__get_password)
        # thread
        self.__update_conn_status()

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

    def __update_conn_status(self):
        self.wifi_list = []
        self.current_wifi = None

        try:
            self.wifi_list = list(Cell.all('wlan0'))
        except:
            pass

        current_wifi_name = ""
        try:
            current_wifi_name = subprocess.check_output(['sudo', 'iwgetid']).decode().split('"')[1]
        except:
            pass

        self.av_networks_list.delete(*self.av_networks_list.get_children())

        for network in self.wifi_list:
            if (network.ssid == current_wifi_name):
                self.current_wifi = network
            self.av_networks_list.insert("",
                                        tk.END,
                                        text = network.ssid)

        if not (self.current_wifi is None):
            self.current_con_label.config(
                image= self.__get_signal_quality_icon(self.current_wifi.signal),
                text = " Connected to " + self.current_wifi.ssid
            )
        else:
            self.current_con_label.config(
                image = self.wifi_off_icon,
                text = " Please select a network!"
            )
        
        self.__conn_status_timer = threading.Timer(5.0, self.__update_conn_status)
        self.__conn_status_timer.daemon = True
        self.__conn_status_timer.start()


    def __get_password(self, event):

        if not (self.top == None):
            return

        focused = self.av_networks_list.item(self.av_networks_list.focus())
        ssid = focused["text"]
        this_network = None

        for network in self.wifi_list:
            if (network.ssid == ssid):
                this_network = network
                break

        if (this_network is None):
            return
        
        if not (this_network.encrypted):
            self.__connect_to(this_network, "", False)
            return
        
        self.top = Toplevel(self)
        self.top.overrideredirect(1)
        x = self.winfo_width()//2 - self.top.winfo_width()//2
        y = self.winfo_height()//2 - self.top.winfo_height()//2 - 80
        self.top.geometry(f"+{x}+{y}")

        #layout
        self.top.rowconfigure(0, weight = 1)
        self.top.rowconfigure(1, weight = 1)
        self.top.rowconfigure(2, weight = 1)
        self.top.columnconfigure(0, weight = 1)
        self.top.columnconfigure(1, weight = 1)
    
        label_passwd = tk.Label(self.top, text = "Password for " + ssid + ":")
        textbox_passwd = tk.Entry(self.top, show = "*", font = ("Noto Sans Mono", 14))
        button_cancel = tk.Button(self.top, 
                                  text = "Cancel",
                                  font = constants.button_font_mini,
                                  background="CadetBlue",
                                  activebackground="CadetBlue",
                                  command= lambda: self.__destroy_popup())
        button_ok = tk.Button(self.top,
                              text="Ok",
                              font = constants.button_font_mini,
                              background="CadetBlue",
                              activebackground="CadetBlue",
                              command= lambda: self.__connect_to(this_network, textbox_passwd.get(), True))

        label_passwd.grid(row = 0,
                          column = 0,
                          columnspan= 2,
                          pady = (10, 0),
                          padx = (10, 10),
                          sticky = "nswe")
        textbox_passwd.grid(row = 1,
                            column = 0,
                            columnspan = 2,
                            pady = (5, 10),
                            padx = (10, 10),
                            sticky = "nswe")
        button_cancel.grid(row = 2,
                           column = 0,
                           columnspan = 1,
                           padx = (10, 5),
                           pady = (0, 10),
                           sticky = "nswe")
        button_ok.grid(row = 2,
                       column = 1,
                       columnspan = 1,
                       padx= (5, 10),
                       pady = (0, 10),
                       sticky = "nswe")

        textbox_passwd.bind("<FocusIn>", self.__show_keyboard)
        textbox_passwd.bind("<FocusOut>", self.__hide_keyboard)

    def __connect_to(self, network, passwd: str, encrypted = True):
        if not (encrypted):
            finder = connection.Finder(
                server_name = "localhost",
                password = "",
                interface = "wlan0",
            )
            finder.connection_no_password("\"" + network.ssid + "\"")
        else:
            finder = connection.Finder(
                server_name = "localhost",
                password = passwd,
                interface = "wlan0",
            )
            finder.connection("\"" + network.ssid + "\"")
        self.__destroy_popup()

    def __destroy_popup(self):
        self.top.destroy()
        self.top = None
        onboard_keyboard.hide_keyboard()

    def __show_keyboard(self, event):
        onboard_keyboard.show_keyboard()

    def __hide_keyboard(self, event):
        onboard_keyboard.hide_keyboard()