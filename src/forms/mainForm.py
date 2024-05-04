from modules.CustomRandomization.PrimeTest import double_prime_test_adaptive
from .peerForm import PeerWindow
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from bestconfig import Config


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.initUI()
        
        

    def initUI(self):
        self.setWindowTitle('ГОСТ 34.10-2012 (без хеша)')
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
        text = "Реализация протокола ГОСТ 34.10-2012 без использования хэш-функции в виде клиент-серверной системы"
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
        text = f"""Модуль эллиптической кривой: {self.config.curve.p}\n
                Эллиптическая кривая E: ({self.config.curve.a}, {self.config.curve.b})\n
                начальная точка генерации GP: [{self.config.generation_point.x}, {self.config.generation_point.y}]\n
                Порядок циклической подгруппы точек: {self.config.subgroup_order}
                """
        label = QLabel(text)
        vbox.addWidget(label)
        self.cryptosystem_parameters.setLayout(vbox)
        return self.cryptosystem_parameters

    def create_check_parameters_block(self):
        self.system_parameters_check_block = QWidget()
        vbox = QVBoxLayout()
        text = "Следующие параметры должны быть простыми числами: Модуль эллиптической кривой и Порядок циклической подгруппы точек"
        label = QLabel(text)
        vbox.addWidget(label)
        
        
        buttons_layout = QHBoxLayout()
        self.p_primary_checker = QPushButton(text="Проверить Модуль эллиптической кривой на простоту")
        self.q_primary_checker = QPushButton(text="Проверить Порядок циклической подгруппы точек на простоту")
        buttons_layout.addWidget(self.p_primary_checker)
        buttons_layout.addWidget(self.q_primary_checker)

        self.p_primary_checker.clicked.connect(self.check_p_parameter)
        self.q_primary_checker.clicked.connect(self.check_q_parameter)
        
        t = QWidget()
        t.setLayout(buttons_layout)

        vbox.addWidget(t)

        self.system_parameters_check_block.setLayout(vbox)

        return self.system_parameters_check_block

    def check_parameter(self, num):
        if double_prime_test_adaptive(num):
            QMessageBox.information(self, "Тест простоты", "Двойной тест просототы Ферма-Миллер-Рабин пройден")
        else:
            QMessageBox.critical(self, "Тест простоты", "Двойной тест просототы Ферма-Миллер-Рабин не пройден")


    def check_p_parameter(self):
        p = int(self.config.curve.p)
        self.check_parameter(p)
        
    def check_q_parameter(self):
        q = int(self.config.subgroup_order)
        self.check_parameter(q)

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
        self.subwindow1 = PeerWindow(1, self)
        self.subwindow2 = PeerWindow(2, self)
        self.subwindow1.show()
        self.subwindow2.show()








class PrimeCheckForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setGeometry(100, 100, 400, 200)

        vbox = QVBoxLayout()

        # Поле ввода очень длинных чисел
        self.number_input = QLineEdit(self)
        self.number_input.setPlaceholderText('Введите число')
        vbox.addWidget(self.number_input)

        # Кнопка "Проверить на простоту"
        self.check_button = QPushButton('Проверить на простоту', self)
        self.check_button.clicked.connect(self.check_primality)
        vbox.addWidget(self.check_button)

        # Поле ввода порта для сервера
        hbox_port = QHBoxLayout()
        self.port_label = QLabel('Порт для сервера:', self)
        hbox_port.addWidget(self.port_label)
        self.port_input = QLineEdit(self)
        hbox_port.addWidget(self.port_input)
        vbox.addLayout(hbox_port)

        # Кнопка "Открыть сервер"
        self.server_button = QPushButton('Открыть сервер', self)
        self.server_button.clicked.connect(self.open_server)
        vbox.addWidget(self.server_button)

        self.setLayout(vbox)

    def check_primality(self):
        number = int(self.number_input.text())
        if double_prime_test_adaptive(number):
            self.show_message_box('Простое число')
        else:
            self.show_message_box('Составное число')

    def open_server(self):
        port = int(self.port_input.text())
        # Код для открытия сервера по указанному порту

    def show_message_box(self, message):
        QMessageBox.information(self, "Сообщение", message)