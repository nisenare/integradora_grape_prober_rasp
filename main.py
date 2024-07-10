#!/usr/bin/python
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import main_view
import connection_view
import power_view
import constants

global window


def main():
    global window
    window = tk.Tk()
    window.attributes("-fullscreen", True)
    style = ttk.Style()
    style.configure("TNotebook", tabposition="wn")

    box = ttk.Notebook(window)

    home_tab = main_view.MainView(window)
    home_icon = ImageTk.PhotoImage(
        Image.open(constants.absolute_path + "/resource/icon/home_icon_google.png")
    )

    conn_tab = connection_view.ConnectionView(window)
    conn_icon = ImageTk.PhotoImage(
        Image.open(constants.absolute_path + "/resource/icon/wifi_icon_google.png")
    )

    power_tab = power_view.PowerView(window)
    power_icon = ImageTk.PhotoImage(
        Image.open(constants.absolute_path + "/resource/icon/power_icon_google.png")
    )

    box.add(home_tab, image=home_icon)
    box.add(conn_tab, image=conn_icon)
    box.add(power_tab, image=power_icon)

    box.pack(expand=True, fill="both")
    window.mainloop()

    return 0


if __name__ == "__main__":
    exit(main())
