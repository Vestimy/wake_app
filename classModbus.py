import minimalmodbus, classConfig


class classModbus(minimalmodbus.Instrument):
    def __init__(self, portname, slaveaddress):
        self.config = classConfig.Config()
        self.modbusval = True
        try:
            minimalmodbus.Instrument.__init__(self, portname, slaveaddress, mode='rtu')
        except IOError as e:
            self.modbusval = False
            print("Error __init__ Modbus")
            print(e)
        else:
            self.serial.baudrate = self.config.getModbusSpeed()

    def speed(self):

        self.serial.baudrate = self.config.getModbusSpeed()

    def get_pv_loop1(self):
        """Return the process value (PV) for loop1."""
        return self.read_register(289, 1)

    def setStart(self):
        try:
            self.write_register(8192, 2)
            # print(self.serial.baudrate)
        except IOError as e:
            print("Failed to write from instrument")
            print(e)
            print(self.serial.baudrate)
        except Exception:
            return "ошибка"

    def setHome(self):
        try:
            self.write_register(8192, 3)
        except IOError:
            print("Failed to write from instrument")
        except Exception as e:
            print("ошибка SetHome")
            print(e)

    def setForward(self):
        try:
            self.write_register(8192, 4)
        except IOError as e:
            print("Failed to write from instrument")

            print(e)
        except Exception:
            return "ошибка"

    def setBackward(self):
        try:
            self.write_register(8192, 8)
        except IOError:
            print("Failed to write from instrument")
        except Exception as e:
            print("Ошибка")

            print(e)

    def setStop(self):
        try:
            self.write_register(8192, 1)
        except IOError as e:
            print("Failed to write from instrument")
            print(e)
        except Exception as e:
            print("Ошибка")
            print(e)

    def setRevers(self):
        try:
            self.write_register(8192, 12)
        except IOError:
            print("Failed to read from instrument")
        except Exception:
            print("Ошибка")

    def setComand(self, reg, val):
        if val is None:
            try:
                reg = int(reg)
                return str(self.read_register(reg))
            except IOError:
                print("Failed to read from instrument")
            except Exception:
                print("Ошибка чтения")
        else:
            reg = int(reg)
            val = int(val)
            try:
                self.write_register(reg, val)
            except IOError:
                print("Failed to read from instrument")
            except Exception:
                print("Ошибка записи")

    def setSpeed(self, val):

        val = self.speedConvert(val)
        # val = self.mymap(val, 1, 30, 30, 450)
        try:
            self.write_register(8193, val)
        except IOError:
            print("Failed to read from instrument")
        except Exception:
            print("Ошибка")

    def mymap(self, x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def speedConvert(self, value):
        x = float(value) * 16.6667
        x = x / (2 * 3.14 * 0.1)
        val = self.mymap(x, 1, 1485, 1, 500)
        return int(val)
        # '''
        # V = 2 * π * R * n, где
        # V - линейная скорость;
        # R - радиус окружности;
        # n - угловая скорость.
        # D = 2 * R
        # '''

    def getUpdateAll(self):
        lbSetFrequency = str(self.read_register(1))
        lbOutputFrequency = str(self.read_register(2))
        lbRotationalSpeed = str(self.read_register(3))
        lbOperatingHoursCounter = str(self.read_register(4))
        lbFeedbackPidMode = str(self.read_register(5))
        lbDCBusVoltage = str(self.read_register(7))
        lbOutputCurrent = str(self.read_register(8))
        lbErrorRecord1 = str(self.read_register(11))
        lbErrorRecord2 = str(self.read_register(12))

        lbErrorRecord3 = str(self.read_register(13))
        lbErrorRecord4 = str(self.read_register(14))
        lbErrorFreq = str(self.read_register(15))
        lbErrorOutFreq = str(self.read_register(16))
        lbErrorCurrent = str(self.read_register(17))
        lbErrorOutVoltage = str(self.read_register(18))
        version = str(self.read_register(50))
        new = [lbSetFrequency, lbOutputFrequency, lbRotationalSpeed, lbOperatingHoursCounter, lbFeedbackPidMode,
               lbDCBusVoltage, lbOutputCurrent, lbErrorRecord1, lbErrorRecord2, lbErrorRecord3, lbErrorRecord4,
               lbErrorFreq, lbErrorOutFreq, lbErrorCurrent, lbErrorOutVoltage]
        return new
