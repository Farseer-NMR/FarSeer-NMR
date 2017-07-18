from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QToolButton
from PyQt5 import QtCore, QtGui
import os
from gui.components.Icon import Icon, ICON_DIR

class Footer(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent=parent)
        self.setFixedHeight(51)
        self.setObjectName("footer")

        affiliations = '<span style="display:inline"><span style="color: #D5FD84; font-size: 6pt; display:inline">Joao MC Texeira<span style="color: #08F2EE">* </span>' \
                       '<span style="color: #D5FD84; font-size: 6pt;">Simon P. Skinner</span><span style="color: #07C3F5">** </span>' \
                       '<span style="color: #D5FD84; font-size: 6pt;">Miguel Arbescu</span><span style="color: #08F2EE">* </span>' \
                       '<span style="color: #D5FD84; font-size: 6pt;">Alexander L. Breeze</span><span style="color: #07C3F5">** </span>' \
                       '<span style="color: #D5FD84; font-size: 6pt;">Miquel Pons</span><span style="color: #08F2EE">*</span>'
        address1 = '<span style="color: #08F2EE; font-size: 6pt;">*BioNMR Laboratory, Inorganic and Organic Chemistry Department, Universitat de Barcelona, Baldiri Reixac 10-12, 08028 Barcelona, Spain</span>'
        address2 = '<span style="color: #07C3F5; font-size: 6pt;">**Astbury Centre for Structural Molecular Biology, Faculty of Biological Sciences, University of Leeds, LS2 9JT, UK</span>'



        self.label1 = QLabel(affiliations, self)
        self.label2 = QLabel(address1, self)
        self.label3 = QLabel(address2, self)
        self.label1.setObjectName('label1')

        layout = QGridLayout()
        self.setLayout(layout)
        self.layout().setSpacing(6)
        self.layout().addWidget(self.label1, 0, 0)
        self.layout().addWidget(self.label2, 1, 0)
        self.layout().addWidget(self.label3, 2, 0)


        self.twitterButton = QToolButton()
        self.twitterButton.setIcon(Icon('icons/footer-icon-twitter.png'))

        self.paperButton = QToolButton()
        self.paperButton.setIcon(Icon('icons/footer-icon-paper.png'))

        self.emailButton = QToolButton()
        self.emailButton.setIcon(Icon('icons/footer-icon-email.png'))

        self.twitterButton.setIconSize(self.twitterButton.size())
        self.paperButton.setIconSize(self.paperButton.size())
        self.emailButton.setIconSize(self.emailButton.size())



        self.layout().addWidget(self.paperButton, 0, 4, 3, 1)
        self.layout().addWidget(self.emailButton, 0, 5, 3, 1)
        self.layout().addWidget(self.twitterButton, 0, 6, 3, 1)

        version = '<span style="color: #036D8F; font-size: 6pt; font-weight: 400; margin-right: 20px; margin-top: 4px; float: right;">v.1.0.0</span>'
        self.versionLabel = QLabel(version, self)
        self.versionLabel.setAlignment(QtCore.Qt.AlignRight)


        spacerLabel = QLabel('', self)

        self.layout().addWidget(spacerLabel, 0, 3)
        self.layout().addWidget(self.versionLabel, 0, 8, 1, 1)

        self.ctfpLabel = QLabel('', self)
        pixmap = QtGui.QPixmap(os.path.join(ICON_DIR, 'icons/footer-ctfp.png'))
        self.ctfpLabel.setPixmap(pixmap)
        self.ctfpLabel.setAlignment(QtCore.Qt.AlignRight)
        self.layout().addWidget(self.ctfpLabel, 1, 7, 2, 2)

