import tkinter as tk
import cv2
import threading
import time
import numpy as np
import platform
import constants
from PIL import Image
from PIL import ImageTk

class VideoLabel(tk.Label):


    def __init__(self, master: tk.Tk):
        super().__init__(master,
            borderwidth = 1,
            relief = "solid",
            background = "black")
        self.grid(row = 1,
            column = 0,
            sticky = "nsew",
            padx = 10,
            pady = 10)
        self.__cap = None
        self.__should_resize = False
        self.__resize_height = 0
        self.__delay = int(1000 / 30)
        self.__running = False
        self.bind('<Destroy>', self.__on_destroy)


    def start_video_play(self):
        if not self.__running:
            self.__running = True
            self.__update_frame()


    def set_cam_index_first_time(self, index):
        if not self.__cap is None:
            return
        if platform.system() == "Windows":
            self.__cap = ThreadedVideoCapture(index = index, api_preference = cv2.CAP_DSHOW)
        elif platform.system() == "Linux":
            self.__cap = ThreadedVideoCapture(index = index, api_preference = None, gamma = 3.0)
        self.__cap.start()


    def change_cam_index(self, new_index):
        self.__cap.set_new_src(new_index)


    def toggle_resize(self):
        self.__should_resize = not self.__should_resize


    def set_info_frame(self, info_frame):
        self.__info_frame = info_frame


    def change_scale_factor(self, scale_factor):
        self.__cap.set_scale_factor(scale_factor)


    def __update_frame(self):
        ret, frame = self.__cap.get_frame()
        if ret:
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image = im)
            self.config(image = img)
            self.image = img
        if self.__running:
            self.after(self.__delay, self.__update_frame)


    def get_frame(self):
        return self.__cap.get_frame()[1]


    def __on_destroy(self, event):
        self.__cap.release()


class ThreadedVideoCapture:

    def __init__(self, api_preference, index = 0, gamma = 1.0):
        self.__api_preference = api_preference
        self.__cap = cv2.VideoCapture(index, self.__api_preference)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, 520)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 380)
        self.__thread = threading.Thread(target = self.__process)
        self.__video_stop = threading.Event()
        self.ret = False
        self.frame = None
        self.__height = 0
        self.__width = 0
        self.gamma_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255
		    for i in np.arange(0, 256)]).astype("uint8")


    def set_new_src(self, index):
        self.__video_stop.set()
        self.__thread.join()
        self.__cap.release()
        self.__cap = cv2.VideoCapture(index, self.__api_preference)
        # self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.__video_stop.clear()
        self.__thread = threading.Thread(target = self.__process)
        self.__thread.start()


    def start(self):
        self.__thread.start()


    def get_frame(self):
        return self.ret, self.frame
    

    def get_height(self):
        return self.__height
    

    def get_width(self):
        return self.__width


    def __process(self):
        while not self.__video_stop.is_set():
            ret, frame = self.__cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.ret = ret
            self.frame = cv2.LUT(frame, self.gamma_table)
            time.sleep(1/30)


    def release(self):
        if not self.__video_stop.is_set():
            self.__video_stop.set()
            self.__thread.join()
        if self.__cap.isOpened():
            self.__cap.release()


def open_camera(parent):

    if not (parent.cam_top == None):
        return
    
    parent.cam_top = tk.Toplevel(parent)
    parent.cam_top.overrideredirect(1)
    x = 640//2 - 260
    y = 480//2 - 190
    parent.cam_top.geometry(f"+{x}+{y}")
    
    # LAYOUT
    parent.cam_top.rowconfigure(0, weight = 1)
    parent.cam_top.rowconfigure(1, weight = 1)
    parent.cam_top.columnconfigure(0, weight = 1)
    parent.cam_top.columnconfigure(1, weight = 1)
    
    # Video Label
    video_label = VideoLabel(parent.cam_top)
    video_label.grid(row = 0,
                     column = 0,
                     columnspan = 2)
    
    # Cancel button
    button_cancel = tk.Button(parent.cam_top, 
                              text = "Cancel",
                              font = constants.button_font,
                              background="CadetBlue",
                              activebackground="CadetBlue",
                              command= lambda: __destroy_popup(parent))
    
    button_cancel.grid(row = 1,
                     column = 0,
                     columnspan = 1,
                     sticky = "nswe")
    
    # Take Photo button
    button_photo = tk.Button(parent.cam_top, 
                              text = "Take Photo",
                              font = constants.button_font,
                              background="CadetBlue",
                              activebackground="CadetBlue",
                              command= lambda: __take_photo(parent, video_label))
    
    button_photo.grid(row = 1,
                     column = 1,
                     columnspan = 1,
                     sticky = "nswe")

    video_label.set_cam_index_first_time(0)
    video_label.start_video_play()


def __take_photo(parent, video_label):
    parent.photo_arr = video_label.get_frame()
    parent.photo_arr_resized = cv2.resize(parent.photo_arr, (225, 141))
    im = Image.fromarray(parent.photo_arr_resized)
    img = ImageTk.PhotoImage(image = im)
    parent.photo_label.config(image = img)
    parent.photo_label.image = img
    __destroy_popup(parent)


def __destroy_popup(parent):
    if (parent.cam_top == None):
        return
    parent.cam_top.destroy()
    parent.cam_top = None
    parent.toggle_disable_submit()