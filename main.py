import sys, time, datetime, evdev, locale, classBase, classStream
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets, QtCore
from app_main.wake import Ui_Form  # импорт сгенерированного файла из QtDesigner
from app_main.login import Ui_Login_Form  # импорт сгенерированного файла из QtDesigner
from module.classModuleSocket import Server

# Подключение библиотеку для работы с Джойстиком в линукс
path = "config/config.ini"
pathWake = "config/wake.ini"
pathModbus = "config/modbus.ini"
import classModbus, classConfig


# Окно аутентификации
class LoginDialog(QtWidgets.QDialog, Ui_Login_Form, classConfig.Config):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.login = Ui_Login_Form()
        self.login.setupUi(self)
        self.config = classConfig.Config()
        # Вызов функции проверки пароля из my_class
        self.login.login = classBase.getConfiguration()
        # Кнопка аутентификации
        self.login.pushButtonLogin.clicked.connect(self.login_check)

    def login_check(self):
        passw = self.login.lineEdit_Pass.text()
        if passw == "":
            self.login.lcheck.setText("Введите пароль!")
        else:
            if self.config.getPassword(passw):
                self.accept()
            else:
                self.login.lcheck.setText("Пароль Неверный!")
                self.login.lineEdit_Pass.setText('')


# Главное окно
class mywindow(QtWidgets.QWidget):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.config = classConfig.Config()
        # Переменные
        self.controlrun = True
        self.ui.cheacktext = "Нажал кнопку: "
        self.ui.record = True
        self.ui.funcRec = None
        self.ui.buttonName = None
        self.ModbusSpeeds = ['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200']
        self.modbusAdress = [str(i) for i in range(1, 246)]

        self.checkRec = None
        ###############################################################
        #   Соккет сервер
        ###############################################################
        self.sock = Server('')
        self.sock.start()

        ###############################################################
        self.pathverificationcontrol()
        self.ui.getSettingsTimeSet = classBase.getConfiguration()
        self.ui.timetime = self.ui.getSettingsTimeSet.getSettingsWake(True, "getSetTime")
        self.ui.timeEdit.setDateTime(datetime.datetime.strptime(self.ui.timetime, '%H:%M:%S'))

        self.ui.speedWake = self.ui.spinBox.value()

        self.api_ip = self.config.getApiIp()
        self.api_port = self.config.getApiPort()
        self.ui.ipEdit.setText(self.api_ip)
        self.ui.portEdit.setText(str(self.api_port))

        self.sock.socketsignal.connect(self.on_change2, QtCore.Qt.QueuedConnection)

        self.ui.checkApiReq.setChecked(self.config.getApiReq())
        self.ui.checkApiReq.stateChanged.connect(self.requestApi)

        self.ui.horizontalSlider.valueChanged['int'].connect(self.horSlide)
        self.ui.spinBox.valueChanged['int'].connect(self.ui.horizontalSlider.setValue)

        # Окна ввода вывода
        self.ui.spinBox.valueChanged.connect(self.spinboxChanged)
        self.ui.lcdNumber.display(self.ui.spinBox.value())

        # Кнопки
        self.ui.pushButtonStop.clicked.connect(self.funcButtonStop)
        self.ui.pushButtonForward.clicked.connect(self.funcButtonForward)
        self.ui.pushButtonBackward.clicked.connect(self.funcButtonBackward)
        self.ui.pushButtonHome.clicked.connect(self.funcButtonHome)
        self.ui.pushButtonStartTimer.clicked.connect(self.startTimer)
        self.ui.pushButtonSaveSetTime.clicked.connect(self.SaveSetTime)
        self.ui.pushButtonRecord.clicked.connect(self.RecordButton)
        self.ui.pushButtonSavePassword.clicked.connect(self.changePassword)
        self.ui.pushButtonSubmit.clicked.connect(self.modbusSubmit)
        self.ui.pushButtonStart.clicked.connect(self.Start)
        self.ui.pushButtonRevers.clicked.connect(self.Revers)
        self.ui.pushButtonUpdate.clicked.connect(self.test)
        self.ui.restartButton.clicked.connect(self.showDialog)
        self.ui.pushButtonApiSave.clicked.connect(self.ApiSave)
        # self.ui.pushButtonApiStart.clicked.connect(self.ApiStart)
        self.ui.pushButtonApiStop.clicked.connect(self.ApiStop)

        self.ui.recordButtonForward.clicked.connect(self.recordKey)
        self.ui.recordButtonBackward.clicked.connect(self.recordKey)
        self.ui.recordButtonStop.clicked.connect(self.recordKey)
        self.ui.recordButtonHome.clicked.connect(self.recordKey)
        self.ui.recordButtonStartTimer.clicked.connect(self.recordKey)
        self.ui.recordButtonSpeedUp.clicked.connect(self.recordKey)
        self.ui.recordButtonSpeedDown.clicked.connect(self.recordKey)
        self.ui.recordButtonRevers.clicked.connect(self.recordKey)
        self.ui.recordButtonStart.clicked.connect(self.recordKey)
        # Вызов метода проверки из файл
        self.ui.check = classBase.getConfiguration()
        self.ui.modbusOptions = classBase.getModBus()
        self.realTime()
        self.mytimer = classStream.myTimer()
        self.mytimer.timerSignal.connect(self.on_change, QtCore.Qt.QueuedConnection)

        self.path = self.config.getModbusPort()
        self.slaveadress = self.config.getModbusSlaveAddress()
        self.ui.modbus = classModbus.classModbus(self.path, self.slaveadress)

        # Вызывает галочка спрашивать пин код при входе, проверка из файла my_class
        self.ui.requestPassword.setChecked(self.config.getRequestPassword())
        self.ui.requestPassword.stateChanged.connect(self.requestPassword)
        self.ui.Port.addItems(self.config.serial_portss())
        self.ui.Port.activated[str].connect(self.modbusPath)
        self.ui.Speed.addItems(self.ModbusSpeeds)
        self.ui.Speed.setCurrentText(str(self.config.getModbusSpeed()))
        self.ui.Speed.activated[str].connect(self.modbusspeed)
        self.ui.Adress.addItems(self.modbusAdress)
        self.ui.Adress.setCurrentText(str(self.config.getModbusSlaveAddress()))
        self.ui.Adress.activated[str].connect(self.modbusadress)

        # Все связаное с датой
        self.ui.lcdTimer.setNumDigits(8)
        self.ui.lcdTimer.display('00:00:00')

        if sys.platform.startswith('linux'):
            self.ui.comboBoxControl.addItems(self.listControl())
            self.ui.comboBoxControl.activated[str].connect(self.setlistControl)
            self.ui.comboBoxControl.setCurrentText(self.config.getControlName())
        self.ui.getWakecontrol = classBase.getWakeControl()
        self.ui.getWakecontrol.getWakeControlSet(False, "setWakeRecord", True)
        if self.ui.modbus.modbusval:
            self.ui.modbus.serial.baudrate = self.config.getModbusSpeed()

    def sBox(self, value):
        self.ui.horizontalSlider.setValue(value)
        self.ui.modbus.setSpeed(value)

    def runControl(self, value):
        if value is not None:
            if self.controlrun:
                self.ui.buttonGame = classStream.myGamepad(value)
                self.ui.buttonGame.checkrun()
                self.ui.buttonGame.mysignal.connect(self.on_change2, QtCore.Qt.QueuedConnection)
                self.ui.buttonGame.myerror.connect(self.errorSearch, QtCore.Qt.QueuedConnection)
                self.ui.buttonGame.keyRecord.connect(self.keyRecord, QtCore.Qt.QueuedConnection)
                self.controlrun = False

                self.checkRec = True
            else:
                pass

    def pathverificationcontrol(self):
        name = self.config.getControlName()
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if (name in device.name):
                self.runControl(device.path)
                return device.path

    def listControl(self):
        if sys.platform.startswith('linux'):
            listcontrol = ["None"]
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                listcontrol.append(device.name)
        if sys.platform.startswith('linux'):
            return listcontrol

        ############################################################3

    def horSlide(self, value):
        self.ui.spinBox.setValue(value)
        self.ui.speedWake = value
        self.ui.modbus.setSpeed(value)

    def modbusSubmit(self):

        adr = self.ui.editParameterAdress.text()
        value = self.ui.editValue.text()
        if (len(adr) <= 4):
            if adr != "":
                if value == "":
                    value = None
                    self.ui.getParameterAdress.setText(adr)
                    self.ui.getParameterValue.setText(self.ui.modbus.setComand(adr, value))
                else:
                    if len(value) <= 4:
                        self.ui.modbus.setComand(adr, value)
                        self.ui.getParameterAdress.setText(adr)
                        self.ui.getParameterValue.setText(value)
                    else:
                        self.ui.getParameterAdress.setText("Данные не верные")
            else:
                self.ui.getParameterAdress.setText("Неверная команда")
        else:
            self.ui.getParameterAdress.setText("Неверный адрес регистра")

    def modbusHandler(self):
        self.ui.lbSetFrequency.setText(self.ui.modbusOptions.getParametrs(True, "lbSetFrequency"))
        self.ui.lbOutputFrequency.setText(self.ui.modbusOptions.getParametrs(True, "lbOutputFrequency"))
        self.ui.lbRotationalSpeed.setText(self.ui.modbusOptions.getParametrs(True, "lbRotationalSpeed"))
        self.ui.lbOperatingHoursCounter.setText(self.ui.modbusOptions.getParametrs(True, "lbOperatingHoursCounter"))
        self.ui.lbFeedbackPidMode.setText(self.ui.modbusOptions.getParametrs(True, "lbFeedbackPidMode"))
        self.ui.lbDCBusVoltage.setText(self.ui.modbusOptions.getParametrs(True, "lbDCBusVoltage"))
        self.ui.lbOutputCurrent.setText(self.ui.modbusOptions.getParametrs(True, "lbOutputCurrent"))
        self.ui.lbErrorRecord1.setText(self.ui.modbusOptions.getParametrs(True, "lbErrorRecord1"))
        self.ui.lbErrorRecord2.setText(self.ui.modbusOptions.getParametrs(True, "lbErrorRecord2"))
        self.ui.lbErrorRecord3.setText(self.ui.modbusOptions.getParametrs(True, "lbErrorRecord3"))
        self.ui.lbErrorRecord4.setText(self.ui.modbusOptions.getParametrs(True, "lbErrorRecord4"))
        # self.ui.lbErrorFreq.setText(self.ui.modbusOptions.getParametrs(True, "lbErrorFreq"))
        # self.ui.lbErrorOutFreq.setText(self.ui.modbusOptions.getParametrs(True, "lbErrorOutFreq"))
        # self.ui.lbErrorCurrent.setText(self.ui.modbusOptions.getParametrs(True, "lbErrorCurrent"))
        # self.ui.lbErrorOutVoltage.setText(self.ui.modbusOptions.getParametrs(True, "lbErrorOutVoltage"))

    # Функция включения записи
    def RecordButton(self):
        if self.ui.buttonGame.record:
            self.ui.getWakecontrol.getWakeControlSet(False, "setWakeRecord", False)
            self.ui.pushButtonRecord.setText("Выключить редактор")
            self.ui.buttonGame.record = False
            style = "background-color:qlineargradient(spread:reflect, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(83, 197, 0, 255), stop:1 rgba(51, 255, 112, 255))"
            self.ui.pushButtonRecord.setStyleSheet(style)
        else:
            self.ui.getWakecontrol.getWakeControlSet(False, "setWakeRecord", True)
            self.ui.pushButtonRecord.setText("Включить редактор")
            self.ui.buttonGame.record = True
            style = ""
            self.ui.pushButtonRecord.setStyleSheet(style)

    def keyRecord(self, key):
        if self.ui.funcRec != None:
            self.ui.getWakecontrol.getKeyControl(False, self.ui.funcRec, key)
            style = ""
            exec('self.ui.%s.setStyleSheet(style)' % self.ui.funcRec)
            self.ui.funcRec = None

    def recordKey(self):
        self.ui.sender = self.sender()
        if self.checkRec is not None:
            if self.ui.buttonGame.record == False:
                if self.ui.funcRec == None:
                    self.ui.funcRec = self.ui.sender.objectName()
                    self.ui.buttonName = self.ui.sender.text()
                    style = "background-color:qlineargradient(spread:reflect, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(83, 197, 0, 255), stop:1 rgba(51, 255, 112, 255))"
                    exec('self.ui.%s.setStyleSheet(style)' % self.ui.funcRec)
                else:
                    if self.ui.sender.objectName() == self.ui.funcRec:
                        style = ""
                        exec('self.ui.%s.setStyleSheet(style)' % self.ui.funcRec)
                        self.ui.funcRec = None
        else:
            pass

    ##########################################################################
    def on_change2(self, s):
        if s == "keyForward":
            self.funcButtonForward()
        elif s == "keyBackward":
            self.funcButtonBackward()
        elif s == "keyHome":
            self.funcButtonHome()
        elif s == "keyStop":
            self.funcButtonStop()
        elif s == "keySpeedUp":
            if self.ui.speedWake < 56:
                self.ui.speedWake = self.ui.speedWake + 1
                self.ui.lcdNumber.display(self.ui.speedWake)
                self.ui.spinBox.setProperty("value", self.ui.speedWake)
        elif s == "RIGHT":
            pass

        elif s == "keySpeedDown":
            if self.ui.speedWake > 1:
                self.ui.speedWake = self.ui.speedWake - 1
                self.ui.lcdNumber.display(self.ui.speedWake)
                self.ui.spinBox.setProperty("value", self.ui.speedWake)
        elif s == "keyRevers":
            self.Revers()
        elif s == "keyStart":
            self.Start()

        elif s == "keyStartTimer":
            self.startTimer()
        else:
            pass

    def setlistControl(self):
        self.config.setControlName(self.ui.comboBoxControl.currentText())
        if self.ui.comboBoxControl.currentText() != "None":
            self.config.setControlPath(self.pathverificationcontrol())
        else:
            self.config.setControlPath("None")

    def modbusPath(self):
        path = self.ui.Port.currentText()
        self.config.setModbusPort(path)

    def modbusspeed(self):
        modspeed = self.ui.Speed.currentText()
        self.config.setModbusSpeed(modspeed)
        if self.ui.modbus.modbusval:
            self.ui.modbus.serial.baudrate = self.config.getModbusSpeed()

    def modbusadress(self):
        slaveadress = self.ui.Adress.currentText()
        self.config.setModbusSlaveAddress(slaveadress)

    def errorSearch(self, e):
        self.ui.errorLabel.setText(e)

    def startTimer(self):
        if not self.mytimer.isRunning():
            self.mytimer.start()

    def on_change(self, s):
        self.ui.lcdTimer.display(str(s).split()[1])

    def spinboxChanged(self):
        self.ui.lcdNumber.display(self.ui.spinBox.value())

    def realTime(self):
        QTimer().singleShot(1000, self.realTime)
        a = time.strftime("%H:%M:%S", time.localtime())
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        today_date = datetime.date.today().strftime("%A %d.%m.%Y")
        self.ui.currentDateTime.setText("Сегодня: " + str(today_date) + ". Время: " + a)

    def SaveSetTime(self):
        getSettingsTimeSet = classBase.getConfiguration()
        # getSettingsTimeSet.getSettingsWake(False, 'saveSetTime', self.ui.timeSetEdit.text())
        getSettingsTimeSet.getSettingsWake(False, 'saveSetTime', self.ui.timeEdit.text())

    def funcButtonForward(self):
        self.ui.lb.setText(self.ui.cheacktext + "ВПЕРЕД")
        self.ui.pushButtonForward.setDisabled(True)
        self.ui.pushButtonBackward.setDisabled(False)
        self.ui.modbus.setForward()

    def funcButtonBackward(self):
        self.ui.pushButtonForward.setDisabled(False)
        self.ui.pushButtonBackward.setDisabled(True)
        self.ui.lb.setText(self.ui.cheacktext + "НАЗАД")
        self.ui.modbus.setBackward()

    def funcButtonStop(self):
        self.ui.lb.setText(self.ui.cheacktext + "СТОП")
        self.ui.pushButtonForward.setDisabled(False)
        self.ui.pushButtonBackward.setDisabled(False)
        self.ui.modbus.setStop()

    def funcButtonHome(self):
        self.ui.lb.setText(self.ui.cheacktext + "ДОМОЙ")
        self.mytimer.running = False
        self.mytimer.getTimerRest()
        self.ui.modbus.setHome()

    def Start(self):
        self.ui.modbus.setStart()
        self.ui.lb.setText(self.ui.cheacktext + "Start")

    def Revers(self):
        self.ui.modbus.setRevers()
        self.ui.lb.setText(self.ui.cheacktext + "Revers")

    def changePassword(self):
        passw = self.ui.passwordEdit.text()
        if passw != "":
            self.config.setPassword(passw)

    def requestPassword(self, state):
        if state == Qt.Checked:
            self.config.setRequestPassword("True")
        else:
            self.config.setRequestPassword("False")

    def test(self):
        pass
        # value = self.ui.modbus.getUpdateAll()
        # values = [i for i in range(1,15)]
        # # print(values)
        # lb = ["lbSetFrequency", "lbOutputFrequency","lbRotationalSpeed", "lbOperatingHoursCounter", "lbFeedbackPidMode", "lbDCBusVoltage", "lbOutputCurrent", "lbErrorRecord1", "lbErrorRecord2", "lbErrorRecord3", "lbErrorRecord4", "lbErrorFreq", "lbErrorOutFreq", "lbErrorCurrent", "lbErrorOutVoltage"]
        # # print(lb)
        # new = [[values], [lb]]
        # for i in len(new):
        #     print(i)
        # exec('self.ui.%s.setText(%s)' % self.ui.funcRec % self.value)

    def showDialog(self):

        text, ok = QtWidgets.QInputDialog.getText(self, 'Окно заблокировано',
                                                  'Введите парль:')
        print(text)
        print(ok)
        if ok:
            pasw = self.config.getPassword(text)
            if not pasw:
                self.showDialog()
        else:
            self.showDialog()

    def ApiSave(self):
        self.config.setApiIp(self.ui.ipEdit.text())
        self.config.setApiPort(self.ui.portEdit.text())

        self.sock = classSocketServer.Server(self.api_ip, self.api_port)

        self.ui.labelApiRun.setText("Сервер запущен")

        print(self.sock.isRunning())

    def ApiStop(self):
        self.sock.running = False
        self.ui.labelApiRun.setText("Сервер остановлен")

        print(self.sock.isRunning())

    def requestApi(self, state):
        if state == Qt.Checked:
            self.config.setApiReq("True")
        else:
            self.config.setApiReq("False")

    def closeEvent(self, QCloseEvent):
        print("Стоп сервер")
        self.sock.terminate()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    config = classConfig.Config()
    requestpass = config.getRequestPassword()
    if requestpass:
        login = LoginDialog()
        if login.exec_() == QtWidgets.QDialog.Accepted:
            window = mywindow()
            window.show()
            sys.exit(app.exec_())

    else:
        window = mywindow()
        window.show()
        sys.exit(app.exec_())
