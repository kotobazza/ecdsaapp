import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox
from PyQt6.QtGui import QGuiApplication
import json
from modules.Cryptrography.Math import Point
from modules.Cryptrography.Keys.ECDSAkeys import Signature, ECDSAPublicKey
from modules.TextWorks import wrapText


class ClientWindow(QWidget):
    def __init__(self, unit, network_manager, parent=None):
        super().__init__()
        self.unit = unit
        self.setWindowTitle(f"Пользователь №{self.unit.number}")
        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        screen_width = size.width()
        screen_height  = size.height()
        width = 900
        height= 600
        if self.unit.number%2 == 0:
            self.setGeometry(10, screen_height//2-300, screen_width//2, 800)
            
        else:
            self.setGeometry(screen_width//2+10, screen_height//2-300, screen_width//2, 800)
        
        self.setFixedSize(screen_width//2, 800)
        
        self.wrapSize = 130
        self.network_manager = network_manager 
        self.network_manager.initialize()
        self.parent = parent
        self.network_manager.messageReceived.connect(self.receive_message)
        self.initUI()
        self.otherpublic_key = None

        

    def receive_message(self, message):
        data = json.loads(message)
        if data['type'] == "public_key":
            self.otherpublic_key = Point(
                int(data['body']['point']['x']),
                int(data['body']['point']['y']),
                self.parent.cryptosystem.generation_point.curve
            )
            
            self.otherpublic_key_label.setText(wrapText(f"Публичный ключ: {self.otherpublic_key}", self.wrapSize))
        if data['type'] == "subscription":
            self.subscription = Signature(
                int(data['body']['subscription']['r']),
                int(data['body']['subscription']['s']),
                int(data['body']['subscription']['message'])
            )
            self.subscripted_text.setText(
                wrapText(
                    f"""
                        r: {self.subscription.r}\n
                        s: {self.subscription.s}\n
                        message: {self.subscription.message}
                    """,
                    self.wrapSize)
            )



    def initUI(self):
        generate_keys_button = QPushButton("Сгенерировать новые ключи")
        generate_keys_button.clicked.connect(self.generate_keys)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(generate_keys_button)

        self.create_self_keydescription_block()
        self.create_other_keydescription_block()

        self.subscription_block = QWidget()
        self.subscription_hbox = QVBoxLayout()
        self.subscription_block.setLayout(self.subscription_hbox)


        self.create_sending_block()
        self.create_subcription_checking_block()

        self.vbox.addWidget(self.subscription_block)

        self.setLayout(self.vbox)

    def create_self_keydescription_block(self):
        self.private_key_label = QLabel(f"Здесь будет отображен приватный ключ")
        self.public_key_label = QLabel(f"Здесь будет отображен публичный ключ")

        self.send_pubkey_button = QPushButton("Отправить публичный ключ\nдругому участнику")
        self.send_pubkey_button.setDisabled(True)
        self.send_pubkey_button.clicked.connect(self.send_public_key)

        key_description_block = QGroupBox("Параметры ключа")
        key_description_block_vbox = QVBoxLayout()
        key_description_block_vbox.addWidget(self.private_key_label)
        key_description_block_vbox.addWidget(self.public_key_label)
        key_description_block_vbox.addWidget(self.send_pubkey_button)

        key_description_block.setLayout(key_description_block_vbox)
        self.vbox.addWidget(key_description_block)

    def create_other_keydescription_block(self):
        self.otherpublic_key_label = QLabel(f"Здесь будет отображен публичный ключ соседа")

        key_description_block = QGroupBox("Публичный ключ соседа")
        key_description_block_vbox = QVBoxLayout()
        key_description_block_vbox.addWidget(self.otherpublic_key_label)

        key_description_block.setLayout(key_description_block_vbox)
        self.vbox.addWidget(key_description_block)

    def generate_keys(self):
        self.unit.set_keypair(self.parent.cryptosystem.generate_keypair())


        self.private_key_label.setText(wrapText(f"Приватный ключ: {self.unit.private_key}", self.wrapSize))
        self.public_key_label.setText(wrapText(f"Публичный ключ: {self.unit.public_key}", self.wrapSize))

        self.send_pubkey_button.setDisabled(False)



    def send_public_key(self):
        data = {
            "type":"public_key",
            "body":{
                "point": {
                    "x": self.unit.public_key.x,
                    "y": self.unit.public_key.y
                }
            }
        }

        data_jsoned = json.dumps(data)
        
        self.network_manager.send_message(data_jsoned)

    def create_sending_block(self):
        
        subwidget1 = QGroupBox("Создание подписи сообщения")
        textlabel = QLabel("Введите свое сообщение здесь")
        self.nosubscription_text = QLineEdit()
        self.subscribe_text_button = QPushButton("Подписать сообщение")
        self.subcriptionLineEdit = QLineEdit("Здесь будет текст подписи")
        self.subscribe_text_button.clicked.connect(self.subscribe_text)
        self.send_subscription_button = QPushButton("Отправить подпись")
        self.send_subscription_button.clicked.connect(self.send_subscription)
        self.send_subscription_button.setDisabled(True)



        vbox1 = QVBoxLayout()
        vbox1.addWidget(textlabel)
        vbox1.addWidget(self.nosubscription_text)
        vbox1.addWidget(self.subscribe_text_button)
        vbox1.addWidget(self.subcriptionLineEdit)
        vbox1.addWidget(self.send_subscription_button)
        subwidget1.setLayout(vbox1)
        self.subscription_hbox.addWidget(subwidget1)

    def send_subscription(self):
        data = {
            "type":"subscription",
            "body":{
                "subscription": {
                    "r": self.generated_subscription.r,
                    "s": self.generated_subscription.s,
                    "message": self.generated_subscription.message
                }
            }
        }

        data_jsoned = json.dumps(data)
        
        self.network_manager.send_message(data_jsoned)
        

    def subscribe_text(self):
        self.generated_subscription = self.unit.sign_message(int(self.nosubscription_text.text()))
        #TODO: перепиши этот ужас
        self.subcriptionLineEdit.setText(
            f"""
            r: {self.generated_subscription.r}\n
            s: {self.generated_subscription.s}\n
            message: {self.generated_subscription.message}
        """)
        self.send_subscription_button.setDisabled(False)
        

    def create_subcription_checking_block(self):
        subwidget1 = QGroupBox("Проверка подписи сообщения")
        textlabel = QLabel("Здесь будет попись, полученная от другого пользователя")
        self.subscripted_text = QLabel("Здесь будет сама подпись")
        self.check_subscription_button = QPushButton("Проверить подпись")
        self.check_subscription_button.clicked.connect(self.check_subscription)
        self.raw_text = QLabel("Здесь будет готовое сообщение")
        

        vbox1 = QVBoxLayout()
        vbox1.addWidget(textlabel)
        vbox1.addWidget(self.subscripted_text)
        vbox1.addWidget(self.check_subscription_button)
        vbox1.addWidget(self.raw_text)
        subwidget1.setLayout(vbox1)
        self.subscription_hbox.addWidget(subwidget1)

    def check_subscription(self):
        
        if self.unit.check_signature(self.subscription, ECDSAPublicKey(
            self.parent.cryptosystem.subgroup_order, 
            self.otherpublic_key,
            self.parent.cryptosystem.generation_point
        )):
            self.raw_text.setText(str(self.subscription.message))
            QMessageBox.information(self, "Успех", "Подпись верна")
        else:
            QMessageBox.critical(self, "Ошибка", "Подпись не подтвердилась")

    


        