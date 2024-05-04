from modules.Cryptrography import ECDSAPrivateKey
from modules.Cryptrography.Math.EclipticCurve import Point, EllipticCurve

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from bestconfig import Config



class PeerWindow(QWidget):
    def __init__(self, number, parent):
        super().__init__()
        self.parent = parent
        self.number = number

        label = QLabel(f"Peer №{self.number}")
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        self.setLayout(vbox)

