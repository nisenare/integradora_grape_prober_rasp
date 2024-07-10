import datetime
import tkinter as tk
from tkinter import DISABLED, LEFT, NORMAL, StringVar, ttk
from PIL import Image, ImageTk
import cv2
import requests
import constants
import arduino_com
import camera
import popups

class MainView(tk.Frame):

    def __init__(self, master: tk.Tk, *args):
        super().__init__(master, args)
        
        # miembros
        self.last_ph_val = StringVar(value="0.00")
        self.photo_arr = None
        self.photo_arr_resized = None
        self.temp_popup = None
        self.temp_annotated_img = None
        self.error_icon_17p = tk.PhotoImage(file = constants.absolute_path + "resource/icon/error_icon_google_17p.png")

        #layout
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
    
        #frame de la izq - pH
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row = 0,
                             column = 0,
                             columnspan = 1,
                             sticky = "nswe",
                             padx = (10, 5),
                             pady = (10, 5))
        
        self.left_frame.rowconfigure(0, weight = 6)
        self.left_frame.rowconfigure(1, weight = 1)
        self.left_frame.columnconfigure(0, weight = 1)

        self.drop_icon_17p = tk.PhotoImage(file = constants.absolute_path + "resource/icon/drop_icon_google_17p.png")
        self.ph_label = tk.Label(self.left_frame,
                                 textvariable= self.last_ph_val,
                                 font = constants.data_label_font_bold)
        self.scan_ph_button = tk.Button(self.left_frame,
                                        image = self.drop_icon_17p,
                                        text = "pH Probe ",
                                        compound = LEFT,
                                        font = constants.button_font,
                                        background="CadetBlue",
                                        activebackground="CadetBlue",
                                        command = self.__get_ph_value)

        self.ph_label.grid(row = 0, column = 0, columnspan = 1, sticky = "nsew")
        self.scan_ph_button.grid(row = 1, column = 0, columnspan = 1, sticky = "nsew")

        # frame de la der - Foto
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row = 0,
                              column = 1,
                              columnspan = 1,
                              sticky = "nswe",
                              padx = (5, 10),
                              pady = (10, 5))
        
        self.right_frame.rowconfigure(0, weight = 6)
        self.right_frame.rowconfigure(1, weight = 1)
        self.right_frame.columnconfigure(0, weight = 1)

        self.photo_icon_30p = tk.PhotoImage(file = constants.absolute_path + "resource/icon/photo_icon_google_30p.png")
        self.photo_label = tk.Label(self.right_frame,
                                    image = self.photo_icon_30p,
                                    font = constants.data_label_font_bold,
                                    background="gray74")

        self.camera_icon_17p = tk.PhotoImage(file = constants.absolute_path + "resource/icon/camera_icon_google_17p.png")
        self.photo_button = tk.Button(self.right_frame,
                                        image = self.camera_icon_17p,
                                        text = "Camera ",
                                        compound = LEFT,
                                        font = constants.button_font,
                                        background="CadetBlue",
                                        activebackground="CadetBlue",
                                        command = lambda: popups.open_camera(self))
        
        self.photo_label.grid(row = 0, column = 0, columnspan = 1, sticky = "nsew")
        self.photo_button.grid(row = 1, column = 0, columnspan = 1, sticky = "nsew")

        # frame de abajo
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(row = 1,
                               columnspan = 2,
                               sticky = "s",
                               padx = (10, 10),
                               pady = (5, 10))
        
        self.upload_icon_17p = tk.PhotoImage(file = constants.absolute_path + "resource/icon/upload_icon_google_17p.png")
        self.submit_button = tk.Button(self.bottom_frame,
                                        image = self.upload_icon_17p,
                                        text = "Upload ",
                                        compound = LEFT,
                                        font = constants.button_font,
                                        background="CadetBlue",
                                        activebackground="CadetBlue",
                                        command = self.__submit_data)
        self.submit_button.config(state = DISABLED)
        self.reset_icon_17p = tk.PhotoImage(file = constants.absolute_path + "resource/icon/reset_icon_google_17p.png")
        self.reset_button = tk.Button(self.bottom_frame,
                                        image = self.reset_icon_17p,
                                        text = "Reset ",
                                        compound = LEFT,
                                        font = constants.button_font,
                                        background="CadetBlue",
                                        activebackground="CadetBlue",
                                        command = self.__reset_all_values)
        
        self.reset_button.grid(row = 0, column = 0, sticky = "swe", pady = (0, 10))
        self.submit_button.grid(row = 1, column = 0, sticky = "swe")


    def __reset_all_values(self):
        self.last_ph_val.set("0.00")
        self.photo_arr = None
        self.photo_arr_resized = None
        self.photo_label.config(
            image = self.photo_icon_30p,
            background = "gray74"
        )
        self.toggle_disable_submit()


    def __get_ph_value(self):
        ph_val_str = "..."
        self.last_ph_val.set(ph_val_str)

        try:
            ph_val_str = arduino_com.send_and_wait("PH")
        except:
            ph_val_str = "NO_CON"
            pass

        self.last_ph_val.set(ph_val_str)
        self.toggle_disable_submit()
        

    def toggle_disable_submit(self):
        if (self.last_ph_val.get() == "0.00"
            or self.last_ph_val.get() == "NO_CON"
            or self.photo_arr is None):
            self.submit_button.config(state = DISABLED)
            return

        self.submit_button.config(state = NORMAL)


    def __submit_data(self):
        ret, buffer = cv2.imencode(".jpeg", self.photo_arr)
        
        if not ret:
            return
        
        image_file = { "image": buffer}
        data = {
            "ph": float(self.last_ph_val.get()),
            "date_time": str(datetime.datetime.now()),
        }

        try:
            r = requests.post(constants.backend_url + "/api/sensequery",
                              data = data,
                              files = image_file,
                              timeout = 12)
            popups.show_results(self, r)
        except ConnectionError:
            popups.show_err_popup(self, "Connection Error. Check your network parameters!")
            return
        except TimeoutError:
            popups.show_err_popup(self, "Connection Timeout. Check your network parameters!")
            return

