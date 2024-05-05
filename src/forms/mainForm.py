from modules.utils import Cryptosystem

from .subForm import ClientWindow
from .tcpModel import Server, Client
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from bestconfig import Config


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.ports = self.config.tcp_ports
        self.subwindow1_server = -1
        self.subwindow2_client = -1
        self.cryptosystem = Cryptosystem(self.config)
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle('ГОСТ 34.10-2012')
        self.setGeometry(100, 100, 640, 480)
        vbox = QVBoxLayout()

        vbox.addWidget(self.create_description_block())
        vbox.addWidget(self.create_system_parameters_block())
        vbox.addWidget(self.create_check_parameters_block())
        vbox.addWidget(self.create_server_parameters_block())
        vbox.addWidget(self.create_start_system_block())
        self.setLayout(vbox)
    
    def create_description_block(self):
        self.description_block = QWidget()
        vbox = QVBoxLayout()
        text = "Реализация протокола ГОСТ 34.10-2012 виде клиент-серверной системы"
        label = QLabel(text)
        vbox.addWidget(label)
        self.description_block.setLayout(vbox)
        return self.description_block

    def create_system_parameters_block(self):
        self.system_parameters = QWidget()
        vbox = QVBoxLayout()
        text = "Получены следующие параметры из файла конфигураций:"
        label = QLabel(text)
        vbox.addWidget(label)
        cryptosystem_block = self.create_system_parameters_enumeration()
        vbox.addWidget(cryptosystem_block)
        self.system_parameters.setLayout(vbox)
        return self.system_parameters
        

    def create_system_parameters_enumeration(self):
        self.cryptosystem_parameters = QWidget()
        vbox = QVBoxLayout()
        text = f"""Модуль эллиптической кривой: {self.cryptosystem.curve.p}\n
                Эллиптическая кривая E: ({self.cryptosystem.curve.a}, {self.cryptosystem.curve.b})\n
                Начальная точка генерации GP: [{self.cryptosystem.generation_point.x}, {self.cryptosystem.generation_point.y}]\n
                Порядок циклической подгруппы точек: {self.cryptosystem.subgroup_order}
                """
        label = QLabel(text)
        vbox.addWidget(label)
        self.cryptosystem_parameters.setLayout(vbox)
        return self.cryptosystem_parameters

    def create_check_parameters_block(self):
        self.system_parameters_check_block = QWidget()
        vbox = QVBoxLayout()
        text = """Требования к параметрам:\n
                    Модуль эллиптической кривой - простое число\n
                    Порядок циклической подгруппы точек - простое число\n
                    Произведение GP и Порядок циклической подгруппы точек - точка О"""
        label = QLabel(text)
        vbox.addWidget(label)
        
        
        buttons_layout = QHBoxLayout()
        self.p_primary_checker = QPushButton(text="Проверить Модуль эллиптической\nкривой на простоту")
        self.q_primary_checker = QPushButton(text="Проверить Порядок циклической\nподгруппы точек на простоту")
        self.gp_checker = QPushButton(text="Проверить Произведение GP и Порядок\nциклической подгруппы точек - точка О")
        buttons_layout.addWidget(self.p_primary_checker)
        buttons_layout.addWidget(self.q_primary_checker)
        buttons_layout.addWidget(self.gp_checker)

        self.p_primary_checker.clicked.connect(self.check_p_parameter)
        self.q_primary_checker.clicked.connect(self.check_q_parameter)
        self.gp_checker.clicked.connect(self.check_generation_point)
        
        t = QWidget()
        t.setLayout(buttons_layout)

        vbox.addWidget(t)

        self.system_parameters_check_block.setLayout(vbox)

        return self.system_parameters_check_block

    def create_message_box_for_primary_checked_parameter(self, isValid):
        if isValid:
            QMessageBox.information(self, "Тест простоты", "Двойной тест просототы Ферма-Миллер-Рабин пройден")
        else:
            QMessageBox.critical(self, "Тест простоты", "Двойной тест просототы Ферма-Миллер-Рабин не пройден")


    def check_p_parameter(self):
        self.create_message_box_for_primary_checked_parameter(self.cryptosystem.check_p())
    
    def check_q_parameter(self):
        self.create_message_box_for_primary_checked_parameter(self.cryptosystem.check_subgroup_order())

    def check_generation_point(self):
        if self.cryptosystem.check_generation_point():
            QMessageBox.information(self, "Тест Начальной точки GP", "Произведение Начальной точки и Порядка циклической\nподгруппы точек дает несуществующую\nточку")
        else:
            QMessageBox.critical(self, "Тест Начальной точки GP", "Произведение Начальной точки и Порядка циклической\nподгруппы точек не дает несуществующую\nточку")
        

    def create_server_parameters_block(self):
        self.server_parameters_block = QWidget()
        vbox = QVBoxLayout()

        label = QLabel("Определите порты, которые будут использоваться для P2P архитектуры. По два на каждого пользователя, итого 4")

        vbox.addWidget(label)


        # выводить ли порты из конфига?

        self.server_parameters_block.setLayout(vbox)
        return self.server_parameters_block

    def create_start_system_block(self):
        button = QPushButton("Запустить одноранговое соединение")
        button.clicked.connect(self.create_p2p_subwindows)

        return button

    def create_p2p_subwindows(self):
        
        if self.subwindow1_server != -1:
            self.subwindow1_server.close()
            self.cryptosystem.unit1 = -1
        if self.subwindow2_client != -1:
            self.subwindow2_client.close()
            self.cryptosystem.unit2 = -1

        if self.cryptosystem.check_p() and self.cryptosystem.check_subgroup_order() and  self.cryptosystem.check_generation_point():

            self.tcpserver = Server(5000)
            self.tcpclient = Client(5000)
            
            self.subwindow1_server = ClientWindow(
                self.cryptosystem.get_first_unit(),
                self.tcpserver,
                self
            )
            self.subwindow2_client = ClientWindow(
                self.cryptosystem.get_second_unit(),
                self.tcpclient,
                self
            )
            self.subwindow1_server.show()
            self.subwindow2_client.show()
        else:
            QMessageBox.critical(self, "Ошибка в параметрах", "Полученные параметры криптосистемы оказались неверны.\nПроверьте каждый из параметров перед запуском соединения")

    def onClose(self):
        if self.subwindow1_server != -1:
            self.subwindow1_server.close()
        if self.subwindow2_client != -1:
            self.subwindow2_client.close()
        
    def closeEvent(self, event):
        self.onClose()
        event.accept()

