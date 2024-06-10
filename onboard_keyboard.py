import subprocess
import os
import signal

def show_keyboard():
    subprocess.Popen(['onboard'])

def hide_keyboard():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if b'onboard' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)