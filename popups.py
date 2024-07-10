import base64
import io
import tkinter as tk
import cv2
import threading
import time
import numpy as np
import platform
import constants
from camera import VideoLabel
from PIL import Image
from PIL import ImageTk

# ---------------- FOR THE MAIN VIEW ---------------- 
def open_camera(parent):
    if not (parent.temp_popup == None):
        return
    
    parent.temp_popup = tk.Toplevel(
        parent,
        borderwidth = 1,
        relief='solid'
    )
    parent.temp_popup.overrideredirect(1)
    
    # LAYOUT
    parent.temp_popup.rowconfigure(0, weight = 1)
    parent.temp_popup.rowconfigure(1, weight = 1)
    parent.temp_popup.columnconfigure(0, weight = 1)
    parent.temp_popup.columnconfigure(1, weight = 1)
    
    # Video Label
    video_label = VideoLabel(parent.temp_popup)
    video_label.grid(row = 0,
                     column = 0,
                     columnspan = 2)
    
    # Cancel button
    button_cancel = tk.Button(parent.temp_popup, 
                              text = "Cancel",
                              font = constants.button_font,
                              background="CadetBlue",
                              activebackground="CadetBlue",
                              command= lambda: __destroy_popup(parent))
    button_cancel.grid(row = 1,
                     column = 0,
                     columnspan = 1,
                     sticky = "nswe",
                     pady = (0, 10),
                     padx = (10, 5))
    
    # Take Photo button
    button_photo = tk.Button(parent.temp_popup, 
                              text = "Take Photo",
                              font = constants.button_font,
                              background="CadetBlue",
                              activebackground="CadetBlue",
                              command= lambda: __take_photo(parent, video_label))
    
    button_photo.grid(row = 1,
                     column = 1,
                     columnspan = 1,
                     sticky = "nswe",
                     pady = (0, 10),
                     padx = (5, 10))

    video_label.init_camera()
    video_label.start_video_play()
    __center_popup(parent, True)


def show_results(parent, response):
    if not (parent.temp_popup == None):
        return

    json_response = response.json()
    annotated_image = Image.open(
        io.BytesIO(
            base64.decodebytes(
                bytes(json_response["annotated_image"],"utf-8")
            )
        )
    )
    annotated_image = annotated_image.resize((440, 260))
    ph = json_response["ph"]
    overall_maturity = json_response["overall_maturity"]

    parent.temp_popup = tk.Toplevel(
        parent,
        borderwidth = 1,
        relief='solid'
    )
    parent.temp_popup.overrideredirect(1)
    
    # LAYOUT
    parent.temp_popup.rowconfigure(0, weight = 1)
    parent.temp_popup.rowconfigure(1, weight = 1)
    parent.temp_popup.columnconfigure(0, weight = 1)
    parent.temp_popup.columnconfigure(1, weight = 1)

    # results label
    results_label = tk.Label(parent.temp_popup,
                             font = constants.data_label_font_mini,
                             text = f"PH:\n{ph}\n" +
                             f"Overall Maturity:\n{overall_maturity}\n"
    )
    results_label.grid(row = 0,
                       column = 0,
                       columnspan = 1
    )
    
    # Image Label
    img = ImageTk.PhotoImage(image = annotated_image)
    parent.temp_annotated_img = img
    image_label = tk.Label(parent.temp_popup,
                           image = parent.temp_annotated_img)
    image_label.grid(row = 0,
                     column = 1,
                     columnspan = 1,
                     sticky = "nswe",
                     padx = (10, 10),
                     pady = (10, 5))
    
    # Ok button
    button_ok = tk.Button(parent.temp_popup, 
                              text = "Ok",
                              font = constants.button_font,
                              background="CadetBlue",
                              activebackground="CadetBlue",
                              command= lambda: __destroy_popup(parent))
    button_ok.grid(row = 1,
                     column = 1,
                     columnspan = 1,
                     sticky = "nswe",
                     pady = (0, 10),
                     padx = (10, 10))
    
    parent.submit_button.config(state = tk.DISABLED)
    __center_popup(parent, True)


def show_err_popup(parent, message):
    if not (parent.temp_popup == None):
        return

    parent.temp_popup = tk.Toplevel(
        parent,
        borderwidth = 1,
        relief='solid'
    )
    parent.temp_popup.overrideredirect(1)
    
    # LAYOUT
    parent.temp_popup.rowconfigure(0, weight = 1)
    parent.temp_popup.rowconfigure(1, weight = 1)
    parent.temp_popup.columnconfigure(0, weight = 1)
    parent.temp_popup.columnconfigure(1, weight = 1)

    # Error image label
    error_image_label = tk.Label(
        parent.temp_popup,
        image = parent.error_icon_17p
    )
    error_image_label.grid(
        row = 0,
        column = 0,
        columnspan = 1,
        sticky = "nswe",
        pady = (10, 0),
        padx = (10, 10)
    )

    # Message label
    error_message_label = tk.Label(
        parent.temp_popup,
        text = message
    )
    error_message_label.grid(
        row = 0,
        column = 1,
        columnspan = 1,
        sticky = "nswe",
        pady = (10, 0),
        padx = (0, 10)
    )

    # Ok button
    button_ok = tk.Button(
        parent.temp_popup, 
        text = "Ok",
        font = constants.button_font,
        background="CadetBlue",
        activebackground="CadetBlue",
        command= lambda: __destroy_popup(parent)
    )
    button_ok.grid(
        row = 1,
        column = 1,
        columnspan = 1,
        sticky = "nswe",
        pady = (0, 10),
        padx = (10, 10)
    )
    __center_popup(parent)


def show_conf_dialog(parent, message, function):
    if not (parent.temp_popup == None):
        return

    parent.temp_popup = tk.Toplevel(
        parent,
        borderwidth = 1,
        relief='solid'
    )
    parent.temp_popup.overrideredirect(1)
    
    # LAYOUT
    parent.temp_popup.rowconfigure(0, weight = 1)
    parent.temp_popup.rowconfigure(1, weight = 1)
    parent.temp_popup.columnconfigure(0, weight = 1)
    parent.temp_popup.columnconfigure(1, weight = 1)

    # Error image label
    warning_image_label = tk.Label(
        parent.temp_popup,
        image = parent.warning_icon_17p
    )
    warning_image_label.grid(
        row = 0,
        column = 0,
        columnspan = 1,
        sticky = "nswe",
        pady = (10, 0),
        padx = (10, 10)
    )

    # Message label
    warning_message_label = tk.Label(
        parent.temp_popup,
        text = message,
        font = constants.data_label_font_mini
    )
    warning_message_label.grid(
        row = 0,
        column = 1,
        columnspan = 1,
        sticky = "nswe",
        pady = (10, 0),
        padx = (0, 10)
    )

    # Cancel button
    button_cancel = tk.Button(
        parent.temp_popup, 
        text = "Cancel",
        font = constants.button_font,
        background="CadetBlue",
        activebackground="CadetBlue",
        command= lambda: __destroy_popup(parent)
    )
    button_cancel.grid(
        row = 1,
        column = 0,
        columnspan = 1,
        sticky = "nswe",
        pady = (0, 10),
        padx = (10, 5)
    )

    # Ok button
    button_ok = tk.Button(
        parent.temp_popup, 
        text = "Ok",
        font = constants.button_font,
        background="CadetBlue",
        activebackground="CadetBlue",
        command= lambda: __call_and_destroy(parent, function)
    )
    button_ok.grid(
        row = 1,
        column = 1,
        columnspan = 1,
        sticky = "nswe",
        pady = (0, 10),
        padx = (5, 10)
    )
    __center_popup(parent)


def __call_and_destroy(parent, function):
    function()
    __destroy_popup(parent)


def __center_popup(parent, is_video_label = False):
    if is_video_label:
        parent.temp_popup.wait_visibility()
        parent.temp_popup.geometry(f"640x480")
    else:
        parent.temp_popup.wait_visibility()
        x = 320 - parent.temp_popup.winfo_width()//2
        y = 240 - parent.temp_popup.winfo_height()//2
        parent.temp_popup.geometry(f"640x480+{x}+{y}")


def __destroy_popup(parent):
    if (parent.temp_popup == None):
        return
    parent.temp_popup.destroy()
    parent.temp_popup = None
    try:
        parent.toggle_disable_submit()
    except:
        pass


def __take_photo(parent, video_label):
    parent.photo_arr = video_label.get_frame()
    parent.photo_arr_resized = cv2.resize(parent.photo_arr, (225, 141))
    im = Image.fromarray(parent.photo_arr_resized)
    img = ImageTk.PhotoImage(image = im)
    parent.photo_label.config(
        image = img,
        background = "#D9D9D9"
    )
    parent.photo_label.image = img
    __destroy_popup(parent)