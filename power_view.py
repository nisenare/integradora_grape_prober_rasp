import tkinter as tk
import constants
import popups
from subprocess import call

class PowerView(tk.Frame):

    def __init__(self, master: tk.Tk, *args):
        super().__init__(master, args)

        # miembros
        self.shutdown_icon_17p = tk.PhotoImage(
            file = constants.absolute_path + "resource/icon/power_icon_google_17p.png"
        )
        self.sleep_icon_17p = tk.PhotoImage(
            file = constants.absolute_path + "resource/icon/sleep_icon_google_17p.png"
        )
        self.restart_icon_17p = tk.PhotoImage(
            file = constants.absolute_path + "resource/icon/restart_icon_google_17p.png"
        )
        self.warning_icon_17p = tk.PhotoImage(
            file = constants.absolute_path + "resource/icon/warning_icon_google_17p.png"
        )
        self.return_value = tk.BooleanVar(value = False)
        self.temp_popup = None

        # layout
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)

        # boton apagar
        self.shutdown_button = tk.Button(
            self,
            image = self.shutdown_icon_17p,
            text = "Shutdown",
            compound = tk.LEFT,
            font = constants.button_font,
            background= "CadetBlue",
            activebackground= "CadetBlue",
            command = lambda: self.__shutdown()
        )
        self.shutdown_button.grid(
            row = 0,
            column = 1,
            columnspan = 1,
            sticky = "nsew",
            pady = (10, 5),
            padx = (10, 10)
        )

        # boton sleep
        self.sleep_button = tk.Button(
            self,
            image = self.sleep_icon_17p,
            text = "Sleep",
            compound = tk.LEFT,
            font = constants.button_font,
            background= "CadetBlue",
            activebackground= "CadetBlue",
            command = lambda: self.__sleep()
        )
        self.sleep_button.grid(
            row = 1,
            column = 1,
            columnspan = 1,
            sticky = "nsew",
            pady = (5, 5),
            padx = (10, 10)
        )

        # boton restart
        self.restart_button = tk.Button(
            self,
            image = self.restart_icon_17p,
            text = "Restart",
            compound = tk.LEFT,
            font = constants.button_font,
            background= "CadetBlue",
            activebackground= "CadetBlue",
            command = lambda: self.__restart()
        )
        self.restart_button.grid(
            row = 2,
            column = 1,
            columnspan = 1,
            sticky = "nsew",
            pady = (5, 10),
            padx = (10, 10)
        )


    def __shutdown(self):
        popups.show_conf_dialog(
            self,
            "Shutdown, are you sure?",
            self.__system_shutdown
        )


    def __sleep(self):
        popups.show_conf_dialog(
            self,
            "Sleep, are you sure?",
            self.__system_sleep
        )


    def __restart(self):
        popups.show_conf_dialog(
            self,
            "Restart, are you sure?",
            self.__system_restart
        )


    def __system_shutdown(self):
        call("nohup shutdown -h now", shell = True)


    def __system_sleep(self):
        call("xset dpms force off", shell = True)

    
    def __system_restart(self):
        call("reboot now", shell = True)
