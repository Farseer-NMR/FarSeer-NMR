
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QPushButton

class TabFooter(QGroupBox):

    def __init__(self, parent):
        QGroupBox.__init__(self, parent)

        buttons_groupbox_layout = QHBoxLayout()
        self.setLayout(buttons_groupbox_layout)

        self.load_config_button = QPushButton("Load Configuration", self)
        self.save_config_button = QPushButton("Save Configuration", self)
        self.run_farseer_button = QPushButton("Run FarSeer-NMR", self)
        self.layout().addWidget(self.load_config_button)
        self.load_config_button.clicked.connect(self.load_config)
        self.save_config_button.clicked.connect(self.save_config)
        self.run_farseer_button.clicked.connect(self.run_farseer_calculation)
        self.layout().addWidget(self.save_config_button)
        self.layout().addWidget(self.run_farseer_button)

        self.setFixedHeight(75)

    def load_config(self):
        pass

    def save_config(self):
        pass

    def run_farseer_calculation(self):
        pass