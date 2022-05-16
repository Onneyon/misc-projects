# import logging
import multiprocessing
from curio import sleep
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from bricknil import attach, start
from bricknil.process import Process
from bricknil.const import Color
from bricknil.hub import CPlusHub
from bricknil.sensor.light import LED
from bricknil.sensor.motor import CPlusLargeMotor, CPlusXLMotor


@attach(LED, name="hub_led")
@attach(CPlusXLMotor, name="motor_a")
@attach(CPlusXLMotor, name="motor_b")
class Digger(CPlusHub):

    def __init__(self, queue, name, id):
        self.q = queue
        self.running = True
        self.startup = True
        super().__init__(name, ble_id=id)

    async def run(self):
        if self.startup:
            self.startup = False
            print("startup complete")
            await self.hub_led.set_color(Color.green)
            await sleep(0.2)

        while not q.empty():
            q_item = q.get()
            print(f"received: {q_item}")

            if q_item == "STOP":
                self.running = False
            elif "LIGHT_" in q_item:
                print("changing colour...", end=" ")

                colour = q_item.replace("LIGHT_", "").lower()
                await self.hub_led.set_color(eval(f"Color.{colour}"))

                await sleep(0.2)
                print("done!")

        if self.running:
            # time.sleep(0.2)
            await sleep(0.2)
            await self.run()


class Ui_mainWindow(object):

    def __init__(self, q):
        self.q = q

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(547, 353)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_stop = QtWidgets.QPushButton(self.centralwidget)
        self.button_stop.setGeometry(QtCore.QRect(10, 10, 81, 41))
        self.button_stop.setObjectName("button_stop")
        self.button_red = QtWidgets.QPushButton(self.centralwidget)
        self.button_red.setGeometry(QtCore.QRect(100, 10, 81, 41))
        self.button_red.setObjectName("button_red")
        self.button_green = QtWidgets.QPushButton(self.centralwidget)
        self.button_green.setGeometry(QtCore.QRect(190, 10, 81, 41))
        self.button_green.setObjectName("button_green")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 547, 24))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        self.button_stop.clicked.connect(partial(self.q.put, "STOP"))
        self.button_red.clicked.connect(self.hub_light_red)
        self.button_green.clicked.connect(self.hub_light_green)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Lego controller"))
        self.button_stop.setText(_translate("mainWindow", "Disconnect"))
        self.button_red.setText(_translate("mainWindow", "Red"))
        self.button_green.setText(_translate("mainWindow", "Green"))

    def hub_stop(self):
        self.q.put("STOP")

    def hub_light_red(self):
        self.q.put("LIGHT_RED")

    def hub_light_green(self):
        self.q.put("LIGHT_GREEN")


async def system(q):
    # digger = Digger(q, "top", "90:84:2B:4D:D3:53")
    digger = Digger(q, "base", "90:84:2B:4D:D0:91")


def start_handler(q, system):
    s = partial(system, q)
    start(s)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)

    q = multiprocessing.Queue()

    app = QtWidgets.QApplication([])
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow(q)
    ui.setupUi(mainWindow)
    mainWindow.show()

    p_hub = multiprocessing.Process(target=start_handler, args=(q, system))
    p_hub.start()

    app.exec_()
    p_hub.join()
