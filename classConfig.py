import configparser, serial, glob, os, sys

path = "config/config.ini"
pathWake = "config/wake.ini"
pathModbus = "config/modbus.ini"


class Config():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.path = "config/config.ini"
        self.LoadPath()
        # self.config.read(self.path)

    def LoadPath(self):
        if os.path.isfile(self.path):
            self.config.read(self.path)
        else:
            self.createConfig()
            self.LoadPath()

    ############################################################################
    #           Надо СДЕЛАТЬ!!!!!!!!!!!
    #######################################################################
    def createConfig(self):
        self.config.config['DEFAULT'] = {'ServerAliveInterval': '45', 'Compression': 'yes', 'CompressionLevel': '9'}
        self.write()

    def write(self):
        with open(self.path, 'w') as configfile:
            self.config.write(configfile)

    ########################################################################
    #           Управление геймадом
    ########################################################################
    def getControlPath(self):
        return self.config["CONTROL"]["path"]

    def setControlPath(self, value):
        self.config.set("CONTROL", "path", value)
        self.write()

    def getControlName(self):
        return self.config["CONTROL"]["name"]

    def setControlName(self, value):
        self.config.set("CONTROL", "name", value)
        self.write()

    ########################################################################
    #           MODBUS
    #####################################################################
    def setModbusPort(self, value):
        self.config.set("MODBUS", "portname", value)
        self.write()

    def getModbusPort(self):
        return self.config.get("MODBUS", "portname")

    def setModbusSlaveAddress(self, value):
        self.config.set("MODBUS", "slaveaddress", value)
        self.write()

    def getModbusSlaveAddress(self):
        return self.config.getint("MODBUS", "slaveaddress")

    def getModbusSpeed(self):
        return self.config.getint('MODBUS', 'speed')

    def setModbusSpeed(self, value):
        self.config.set("MODBUS", "speed", value)
        self.write()

    def setUpdateAll(self, name, value):
        self.config.set("MODBUS OPTIONS", name, value)
        self.write()

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

    ########################################################################
    #           Конфигурация приложения!!!
    #####################################################################
    def getPassword(self, value):
        passw = self.config.get('DEFAULT', 'password')
        if passw == value:
            return True
        else:
            return False

    def setPassword(self, value):
        self.config.set('DEFAULT', 'password', value)
        self.write()

    def setRequestPassword(self, value):
        self.config.set('DEFAULT', 'requestpass', value)
        self.write()

    def getRequestPassword(self):
        return self.config.getboolean('DEFAULT', 'requestpass')

    def getApiIp(self):
        return self.config.get('API', 'ip')

    def setApiIp(self, value):
        self.config.set('API', 'ip', value)
        self.write()

    def getApiPort(self):
        return self.config.getint('API', 'port')

    def setApiPort(self, value):
        self.config.set('API', "port", value)
        self.write()

    def getApiReq(self):
        return self.config.getboolean('API', "req")

    def setApiReq(self, value):
        self.config.set('API', 'req', value)
        self.write()
