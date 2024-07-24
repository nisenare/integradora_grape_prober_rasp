import serial
import time

try:
    ser = serial.Serial("/dev/ttyS0", 9600, timeout = 1)
    ser.reset_input_buffer()
except:
    pass


def wait_for_response() -> str:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            return line

  
def send_and_wait(message: str) -> str:
    ser.write(message.encode('utf-8'))
    resp = "\n"
    while (resp == "\n" or resp == ""):
        resp = ser.readline().decode('utf-8').rstrip()
    return resp