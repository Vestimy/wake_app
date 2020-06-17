import PyQt5
import evdev
import threading
from PyQt5 import QtCore
class tControl(PyQt5.QtCore.QThread):
    # mysignal = PyQt5.QtCore.pyqtSignal(str)
    # myerror = PyQt5.QtCore.pyqtSignal(str)
    # keyRecord = PyQt5.QtCore.pyqtSignal(str)
    def __init__(self, path):
        PyQt5.QtCore.QThread.__init__(self)
        self.dev = evdev.InputDevice(path)
        self.path = path
    def run(self):
        self.x = True
        # while x:
        #     print(self.path)
        #     self.sleep(1)
        for event in self.dev.read_loop():
            if self.x:
                if event.type == evdev.ecodes.EV_KEY:
                    print(evdev.categorize(event))
                    print(event)
            else:
                return None


class Control(evdev.InputDevice):
    def __init__(self, path):
        evdev.InputDevice.__init__(self, path)
        my_thread = threading.Thread(target=self.check,  args=())
        my_thread.start()
        # my_thread.join()
        # print(self)
        # print("klnvlbfdnlfdn")
        # self.run()
    def check(self):
        for event in self.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                print(evdev.categorize(event))
                print(event)
            # elif event.type == evdev.ecodes.EV_ABS:
            #     absevent = evdev.categorize(event)
            #     print(absevent)
            #     print(evdev.ecodes.bytype[absevent.event.type][absevent.event.code])