import os

class Finder:

    def __init__(self, *args, **kwargs):
        self.server_name = kwargs['server_name']
        self.password = kwargs['password']
        self.interface_name = kwargs['interface']
        self.main_dict = {}


    def run(self):
        command = """iwlist wlan0 scan | grep -ioE 'ssid:"(.*.*)'"""
        result = os.popen(command)
        result = list(result)

        if "Device or resource busy" in result:
                return None
        else:
            ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
            print("Successfully got ssids {}".format(str(ssid_list)))


    def connection(self, name):
        cmd = "nmcli d wifi connect {} password {}".format(name,
            self.password,
            self.interface_name)
        try:
            if os.system(cmd) != 0:
                raise Exception()
        except:
            return False
        else:
            return True


    def connection_no_password(self, name):
        cmd = "nmcli d wifi connect {}".format(
            name,
            self.interface_name)
        try:
            if os.system(cmd) != 0:
                raise Exception()
        except:
            return False
        else:
            return True
