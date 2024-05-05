from modules.utils import Cryptosystem

from .subForm import ClientWindow
from .tcpModel import Server, Client
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox
from PyQt6.QtCore import Qt
from bestconfig import Config
import socket


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
        self.cryptosystem_parameters = QGroupBox("Получены следующие параметры из файла конфигураций")
        vbox = QVBoxLayout()
        label = QLabel(f"""Модуль эллиптической кривой: {self.cryptosystem.curve.p}\nЭллиптическая кривая E: ({self.cryptosystem.curve.a}, {self.cryptosystem.curve.b})\nНачальная точка генерации GP: [{self.cryptosystem.generation_point.x}, {self.cryptosystem.generation_point.y}]\nПорядок циклической подгруппы точек: {self.cryptosystem.subgroup_order}""")
        vbox.addWidget(label)
        self.cryptosystem_parameters.setLayout(vbox)
        return self.cryptosystem_parameters
    

    def create_check_parameters_block(self):
        self.system_parameters_check_block = QGroupBox("Требования к параметрам")
        vbox = QVBoxLayout()
        text = """Модуль эллиптической кривой - простое число\nПорядок циклической подгруппы точек - простое число\nПроизведение GP и Порядок циклической подгруппы точек - точка О"""
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
            self.start_button.setDisabled(True)


    def check_p_parameter(self):
        self.create_message_box_for_primary_checked_parameter(self.cryptosystem.check_p())
    
    def check_q_parameter(self):
        self.create_message_box_for_primary_checked_parameter(self.cryptosystem.check_subgroup_order())

    def check_generation_point(self):
        if self.cryptosystem.check_generation_point():
            QMessageBox.information(self, "Тест Начальной точки GP", "Произведение Начальной точки и Порядка циклической\nподгруппы точек дает несуществующую точку")
        else:
            QMessageBox.critical(self, "Тест Начальной точки GP", "Произведение Начальной точки и Порядка циклической\nподгруппы точек не дает несуществующую точку")
            self.start_button.setDisabled(True)
        

    def create_server_parameters_block(self):
        self.server_parameters_block = QGroupBox("Технические параметры")
        vbox = QVBoxLayout()

        label = QLabel("В конфигурационном файле определен системный порт, который используется для работы клиент-серверной архитектуры")
        label2 = QLabel(f"Установлен следующий порт: {self.config.tcp_ports}")
        button = QPushButton("Проверить доступность порта")
        button.clicked.connect(self.check_port_and_show_message)
        
        vbox.addWidget(label)
        vbox.addWidget(label2)
        vbox.addWidget(button)

        self.server_parameters_block.setLayout(vbox)
        return self.server_parameters_block
    
    def check_port_and_show_message(self):
        if self.check_port():
            QMessageBox.information(self, "Успех", "Установленный порт подходит для работы")
        else:
            QMessageBox.critical(self, "Ошибка", f"произошла ошибка при попытке захватить порт")
            self.start_button.setDisabled(True)




    def check_port(self):
        port = self.config.tcp_ports
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", port)) 
            return True
        except socket.error as e:
            return False
        finally:
            s.close()  

    def create_start_system_block(self):
        self.start_button = QPushButton("Запустить одноранговое соединение")
        self.start_button.clicked.connect(self.create_p2p_subwindows)

        return self.start_button

    def create_p2p_subwindows(self):
        
        if self.subwindow1_server != -1:
            self.subwindow1_server.close()
            self.cryptosystem.unit1 = -1
        if self.subwindow2_client != -1:
            self.subwindow2_client.close()
            self.cryptosystem.unit2 = -1

        if self.cryptosystem.check_p() and self.cryptosystem.check_subgroup_order() and  self.cryptosystem.check_generation_point() and self.check_port():

            self.tcpserver = Server(int(self.config.tcp_ports))
            self.tcpclient = Client(int(self.config.tcp_ports))
            
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
            self.subwindow1_server.triesToClose.connect(self.tries_to_close)
            self.subwindow2_client.triesToClose.connect(self.tries_to_close)
        else:
            QMessageBox.critical(self, "Ошибка в параметрах", "Полученные параметры криптосистемы оказались неверны.\nПроверьте каждый из параметров перед запуском соединения")

    def tries_to_close(self):
        reply = QMessageBox.question(self, "Подтверждение", "Закрытие этого окна вызовет закрытие всего приложения.\nВы уверены, что хотите продолжить?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
        

    def onClose(self):
        if self.subwindow1_server != -1:
            self.subwindow1_server.network_manager.server.close()
            self.subwindow1_server.close()
        if self.subwindow2_client != -1:
            self.subwindow2_client.network_manager.client.close()
            self.subwindow2_client.close()
        
    def closeEvent(self, event):
        self.onClose()
        event.accept()

