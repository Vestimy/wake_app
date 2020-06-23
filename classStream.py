import datetime
from PyQt5 import QtCore
from classBase import *

# from game import *
# Подключение библиотеку для работы с Джойстиком в линукс
if sys.platform.startswith('linux'):
    from evdev import InputDevice, categorize, ecodes
    import evdev


class myTimer(QtCore.QThread):
    timerSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.getTimer = getConfiguration()

    def run(self):
        self.timerMinutes = self.getTimerMinutes()
        # self.timer = datetime.datetime.strptime('00:'+self.timerMinutes+':01', '%H:%M:%S')
        self.timer = datetime.datetime.strptime(self.timerMinutes, '%H:%M:%S')
        self.running = True
        while self.running:
            self.timer = self.timer - datetime.timedelta(seconds=1)
            self.timerSignal.emit("%s" % self.timer)
            self.sleep(1)
            if self.timer == datetime.datetime.strptime('00:00:00', '%H:%M:%S'):
                self.running = False

    def getTimerMinutes(self):
        self.timerMinutes = self.getTimer.getSettingsWake(True, "getSetTime")
        # self.timerMinutes2 = self.getTimer.getSettingsWake(True, "getSetTime2")
        return self.timerMinutes

    def getTimerRest(self):
        self.timer = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
        self.timerSignal.emit("%s" % self.timer)


class myGamepad(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    myerror = QtCore.pyqtSignal(str)
    keyRecord = QtCore.pyqtSignal(str)

    def __init__(self, path):
        QtCore.QThread.__init__(self)
        self.game = evdev.InputDevice(path)
        self.getWakecontrol = getWakeControl()
        self.keyPress = dict()

    def checkrun(self):
        self.start()

    def loadKey(self):
        self.keyForward = self.getWakecontrol.getKeyControl(True, 'recordButtonForward')
        self.keyBackward = self.getWakecontrol.getKeyControl(True, 'recordButtonBackward')
        self.keyStop = self.getWakecontrol.getKeyControl(True, 'recordButtonStop')
        self.keyHome = self.getWakecontrol.getKeyControl(True, 'recordButtonHome')
        self.keyStartTimer = self.getWakecontrol.getKeyControl(True, 'recordButtonStartTimer')
        self.keySpeedUp = self.getWakecontrol.getKeyControl(True, 'recordButtonSpeedUp')
        self.keySpeedDown = self.getWakecontrol.getKeyControl(True, 'recordButtonSpeedDown')
        self.keyRevers = self.getWakecontrol.getKeyControl(True, "recordButtonRevers")
        self.keyStart = self.getWakecontrol.getKeyControl(True, "recordButtonStart")

    def run(self):
        self.running = True
        self.record = True
        self.load = True
        if self.game:
            for event in self.game.read_loop():
                if self.record:
                    if self.load:
                        self.loadKey()
                        self.load = False
                    if event.type == ecodes.EV_KEY:
                        if event.value == 1:
                            if event.code == self.keyForward:
                                self.mysignal.emit("keyForward")
                            elif event.code == self.keyBackward:
                                self.mysignal.emit("keyBackward")
                            elif event.code == self.keyStop:
                                self.mysignal.emit("keyStop")
                            elif event.code == self.keyHome:
                                self.mysignal.emit("keyHome")
                            elif event.code == self.keyStartTimer:
                                self.mysignal.emit("keyStartTimer")
                            elif event.code == self.keySpeedUp:
                                self.mysignal.emit("keySpeedUp")
                            elif event.code == self.keySpeedDown:
                                self.mysignal.emit("keySpeedDown")
                            elif event.code == self.keyRevers:
                                self.mysignal.emit("keyRevers")
                            elif event.code == self.keyStart:
                                self.mysignal.emit("keyStart")
                            else:
                                pass
                        # elif event.value == 0:
                        #     if event.code == xBtn:
                        #         print("X button not pressed")
                        #     elif event.code == bBtn:
                        #         print("B button not pressed")
                        #     elif event.code == aBtn:
                        #         print("A button not pressed")
                        #     elif event.code == yBtn:
                        #         print("Y button not pressed")
                        #     elif event.code == lBtn:
                        #         print("LEFT button not pressed")
                        #     elif event.code == rBtn:
                        #         print("RIGHT button not pressed")
                        #     elif event.code == lsBtn:
                        #         print("LEFT Shift button not pressed")
                        #     elif event.code == rsBtn:
                        #         print("RIGHT Shift button not pressed")
                        #     elif event.code == selBtn:
                        #         print("Select button not pressed")
                        #     elif event.code == staBtn:
                        #         print("Start button not pressed")
                        #     elif event.code == lanalogBtn:
                        #         print("Analog Left BTN button not pressed")
                        #     elif event.code == ranalogBtn:
                        #         print("Analog Right BTN button not pressed")
                    elif event.type == ecodes.EV_ABS:
                        absevent = categorize(event)
                        # print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X":
                            if absevent.event.value < 128:
                                print("Gauche | Left")
                                print(absevent.event.value)
                            elif absevent.event.value > 128:
                                print("Droite | Right")
                                print(absevent.event.value)
                            elif absevent.event.value == 128:
                                print("Left | Center")
                                print(absevent.event.value)
                        elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
                            if absevent.event.value < 128:
                                print("Haut | Up")
                                print(absevent.event.value)
                            elif absevent.event.value > 128:
                                print("Bas | Down")
                                print(absevent.event.value)
                            elif absevent.event.value == 128:
                                print("Left | Center")
                                print(absevent.event.value)
                        elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Z":
                            if absevent.event.value < 128:
                                print("Right | Up")
                            elif absevent.event.value > 128:
                                print("Right | Down")
                            elif absevent.event.value == 128:
                                print("Right | Center")
                        elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_RZ":
                            if absevent.event.value < 128:
                                print("Right | Left")
                            elif absevent.event.value > 128:
                                print("Right | Right")
                            elif absevent.event.value == 128:
                                print("Right | Center")
                        elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0Y":
                            if absevent.event.value == 0:
                                print("Center")
                            elif absevent.event.value == -1:
                                print("Up")
                            elif absevent.event.value == 1:
                                print("Down")
                        elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0X":
                            if absevent.event.value == 0:
                                print("Center")
                            elif absevent.event.value == -1:
                                print("Left")
                            elif absevent.event.value == 1:
                                print("Right")
                else:
                    if not self.load:
                        self.load = True
                    if event.type == ecodes.EV_KEY:
                        if event.value == 1:
                            key = str(event.code)
                            print(key)
                            self.keyRecord.emit(key)
                        elif event.type == ecodes.EV_ABS:
                            absevent = categorize(event)
                            key = str(ecodes.bytype[absevent.event.type][absevent.event.code])
                            self.keyRecord.emit(key)
                            print(key)

        #
        # print(event.code)
        # if event.code == int(self.keyPress["xbtn"]):
