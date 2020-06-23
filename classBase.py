import sys, configparser, serial, glob

if sys.platform.startswith('linux'):
    import evdev

path = "config/config.ini"
pathWake = "config/wake.ini"
pathModbus = "config/modbus.ini"


class getModBus():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(pathModbus)

    def getParametrs(self, var1, var2, value=None):
        if var1:
            if var2 == "lbSetFrequency":
                return self.config.get("OPTIONS", "lbSetFrequency")
            elif var2 == "lbOutputFrequency":
                return self.config.get("OPTIONS", "lbOutputFrequency")
            elif var2 == "lbRotationalSpeed":
                return self.config.get("OPTIONS", "lbRotationalSpeed")
            elif var2 == "lbOperatingHoursCounter":
                return self.config.get("OPTIONS", "lbOperatingHoursCounter")
            elif var2 == "lbFeedbackPidMode":
                return self.config.get("OPTIONS", "lbFeedbackPidMode")
            elif var2 == "lbDCBusVoltage":
                return self.config.get("OPTIONS", "lbDCBusVoltage")
            elif var2 == "lbOutputCurrent":
                return self.config.get("OPTIONS", "lbOutputCurrent")
            ###################################################
            elif var2 == "lbErrorRecord1":
                return self.config.get("ERRORS", "lbErrorRecord1")
            elif var2 == "lbErrorRecord2":
                return self.config.get("ERRORS", "lbErrorRecord2")
            elif var2 == "lbErrorRecord3":
                return self.config.get("ERRORS", "lbErrorRecord3")
            elif var2 == "lbErrorRecord4":
                return self.config.get("ERRORS", "lbErrorRecord4")
            elif var2 == "lbErrorFreq":
                return self.config.get("ERRORS", "lbErrorFreq")
            elif var2 == "lbErrorOutFreq":
                return self.config.get("ERRORS", "lbErrorOutFreq")
            elif var2 == "lbErrorCurrent":
                return self.config.get("ERRORS", "lbErrorCurrent")
            elif var2 == "lbErrorOutVoltage":
                return self.config.get("ERRORS", "lbErrorOutVoltage")
        else:
            if var2 == "lbSetFrequency":
                self.config.set("OPTIONS", "lbSetFrequency", value)
            elif var2 == "lbOutputFrequency":
                self.config.set("OPTIONS", "lbOutputFrequency", value)
            elif var2 == "lbRotationalSpeed":
                self.config.set("OPTIONS", "lbRotationalSpeed", value)
            elif var2 == "lbOperatingHoursCounter":
                self.config.set("OPTIONS", "lbOperatingHoursCounter", value)
            elif var2 == "lbFeedbackPidMode":
                self.config.set("OPTIONS", "lbFeedbackPidMode", value)
            elif var2 == "lbDCBusVoltage":
                self.config.set("OPTIONS", "lbDCBusVoltage", value)
            elif var2 == "lbOutputCurrent":
                self.config.set("OPTIONS", "lbOutputCurrent", value)
            ###################################################
            elif var2 == "lbErrorRecord1":
                self.config.set("ERRORS", "lbErrorRecord1", value)
            elif var2 == "lbErrorRecord2":
                self.config.set("ERRORS", "lbErrorRecord2", value)
            elif var2 == "lbErrorRecord3":
                self.config.set("ERRORS", "lbErrorRecord3", value)
            elif var2 == "lbErrorRecord4":
                self.config.set("ERRORS", "lbErrorRecord4", value)
            elif var2 == "lbErrorFreq":
                self.config.set("ERRORS", "lbErrorFreq", value)
            elif var2 == "lbErrorOutFreq":
                self.config.set("ERRORS", "lbErrorOutFreq", value)
            elif var2 == "lbErrorCurrent":
                self.config.set("ERRORS", "lbErrorCurrent", value)
            elif var2 == "lbErrorOutVoltage":
                self.config.set("ERRORS", "lbErrorOutVoltage", value)
            elif var2 == "version":
                self.config.set("OPTIONS", "version", value)
            with open(pathModbus, "w") as config_file:
                self.config.write(config_file)


class getConfiguration():
    def getSetings(self, variable1, variable2, variable3=None):
        config = configparser.ConfigParser()
        config.read(path)
        if variable1:
            if variable2 == 'getPassword':
                conf = config.get('DEFAULT', 'password')
                if conf == variable3:
                    return True
                else:
                    return False
            elif variable2 == 'getSpeed':
                return config.getint('DEFAULT', 'speed')
            elif variable2 == 'getComPort':
                return config.get('DEFAULT', 'port')
            elif variable2 == 'getAdress':
                return config.getint('DEFAULT', 'adress')
            elif variable2 == 'ModORSer':
                return config.getboolean('DEFAULT', 'ModORSer')
            elif variable2 == 'checkWindow':
                if config.getboolean('DEFAULT', 'in_win'):
                    return True
                else:
                    return False
        else:
            if variable2 == 'editPassword':
                config.set('DEFAULT', 'password', variable3)
            if variable2 == 'editComPort':
                config.set('DEFAULT', 'port', variable3)
            if variable2 == 'editSpeed':
                config.set('DEFAULT', 'speed', variable3)
            if variable2 == 'editAdress':
                config.set('DEFAULT', 'adress', variable3)
            elif variable2 == 'checkPinc':
                if True == variable3:
                    config.set('DEFAULT', 'in_win', 'True')
                else:
                    config.set('DEFAULT', 'in_win', 'False')
            elif variable2 == 'fModORSer':
                if True == variable3:
                    config.set('DEFAULT', 'modorser', 'True')
                else:
                    config.set('DEFAULT', 'modorser', 'False')
            with open(path, "w") as config_file:
                config.write(config_file)

    def getSettingsWake(self, variable1, variable2, variable3=None):
        config = configparser.ConfigParser()
        config.read(path)
        if variable1:
            if variable2 == 'getSetTime':
                return config.get('WAKE_SETTINGS', 'set_time')
            if variable2 == 'getSetTime2':
                return config.get('WAKE_SETTINGS', 'set_time2')
        else:
            if variable2 == 'saveSetTime':
                config.set('WAKE_SETTINGS', 'set_time', variable3)
            if variable2 == 'saveSetTime2':
                config.set('WAKE_SETTINGS', 'set_time2', variable3)
            with open(path, "w") as config_file:
                config.write(config_file)

    def serial_portss(self):
        """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def wakeControl(self):
        if sys.platform.startswith('linux'):
            controlwake = ["None"]
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                controlwake.append(device.name)
        if sys.platform.startswith('linux'):
            return controlwake


class getWakeControl():
    def getWakeControlSet(Self, Var1, Var2, Var3=None):
        config = configparser.ConfigParser()
        config.read(pathWake)
        if Var1:
            if Var2 == 'getRecord':
                return config.getboolean('WakeRecord', 'record')
        else:
            if Var2 == 'setWakeRecord':
                if True == Var3:
                    config.set('WakeRecord', 'record', 'True')
                else:
                    config.set('WakeRecord', 'record', 'False')
            with open(pathWake, "w") as config_file:
                config.write(config_file)

    def getKeyControl(self, Var1, Var2, Var3=None):
        config = configparser.ConfigParser()
        config.read(pathWake)
        if Var1:
            if Var2 == "recordButtonForward":
                return config.getint('KeyWake', 'keyForward')
            elif Var2 == "recordButtonBackward":
                return config.getint('KeyWake', 'keyBackward')
            elif Var2 == "recordButtonStop":
                return config.getint('KeyWake', 'keyStop')
            elif Var2 == "recordButtonHome":
                return config.getint('KeyWake', 'keyHome')
            elif Var2 == "recordButtonStartTimer":
                return config.getint('KeyWake', 'keyStartTimer')
            elif Var2 == "recordButtonSpeedUp":
                return config.getint('KeyWake', 'keySpeedUp')
            elif Var2 == "recordButtonSpeedDown":
                return config.getint('KeyWake', 'keySpeedDown')
            elif Var2 == "recordButtonRevers":
                return config.getint("KeyWake", "keyRevers")
            elif Var2 == "recordButtonStart":
                return config.getint("KeyWake", "keyStart")
        else:
            if Var2 == "recordButtonForward":
                config.set('KeyWake', 'keyForward', Var3)
            elif Var2 == "recordButtonBackward":
                config.set('KeyWake', 'keyBackward', Var3)
            elif Var2 == "recordButtonStop":
                config.set('KeyWake', 'keyStop', Var3)
            elif Var2 == "recordButtonHome":
                config.set('KeyWake', 'keyHome', Var3)
            elif Var2 == "recordButtonStartTimer":
                config.set('KeyWake', 'keyStartTimer', Var3)
            elif Var2 == "recordButtonSpeedUp":
                config.set('KeyWake', 'keySpeedUp', Var3)
            elif Var2 == "recordButtonSpeedDown":
                config.set('KeyWake', 'keySpeedDown', Var3)
            elif Var2 == "recordButtonRevers":
                config.set("KeyWake", "keyRevers", Var3)
            elif Var2 == "recordButtonStart":
                config.set("KeyWake", "keyStart", Var3)
            with open(pathWake, "w") as config_file:
                config.write(config_file)
