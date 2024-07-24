import tkinter as tk
import cv2
import threading
import time
import numpy as np
import platform
import constants
from PIL import Image
from PIL import ImageTk
from picamera2 import Picamera2

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
        self.__delay = int(1000 / 30)
        self.__running = False
        self.bind('<Destroy>', self.__on_destroy)


    def start_video_play(self):
        if not self.__running:
            self.__running = True
            self.__update_frame()


    def init_camera(self):
        if not self.__cap is None:
            return
        self.__cap = ThreadedVideoCapture()
        self.__cap.start()

    
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

    def __init__(self):
        Picamera2.set_logging(Picamera2.ERROR)
        self.__tuning = Picamera2.load_tuning_file("ov5647.json")
        self.__cap = Picamera2(
            tuning = self.__tuning)
        self.__config = self.__cap.create_preview_configuration(
            main={"size": (620, 380)}
        )
        self.__cap.configure(self.__config)
        self.__cap.start()
        self.__thread = threading.Thread(target = self.__process)
        self.__video_stop = threading.Event()
        self.ret = False
        self.frame = None


    def __process(self):
        while not self.__video_stop.is_set():
            self.ret = False
            self.frame = self.__cap.capture_array()
            self.ret = True
            time.sleep(1/30)


    def release(self):
        if not self.__video_stop.is_set():
            self.__video_stop.set()
            self.__thread.join()

        if self.__cap.is_open:
            self.__cap.stop()
            self.__cap.close()


    def start(self):
        self.__thread.start()


    def get_frame(self):
        return self.ret, self.frame
    