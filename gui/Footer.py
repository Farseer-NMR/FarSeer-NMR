"""
Copyright © 2017-2018 Farseer-NMR
Simon P. Skinner and João M.C. Teixeira

@ResearchGate https://goo.gl/z8dPJU
@Twitter https://twitter.com/farseer_nmr

This file is part of Farseer-NMR.

Farseer-NMR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Farseer-NMR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.
"""
import os
import webbrowser
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QToolButton
from PyQt5 import QtCore, QtGui

from gui.components.Icon import Icon, ICON_DIR

from install import system

class Footer(QWidget):

    def __init__(self, parent, gui_settings=None):
        QWidget.__init__(self, parent=parent)
        self.setFixedHeight(gui_settings['footer_height'])
        self.setObjectName("footer")
        affiliations = '<span style="display:inline"><span style="color: #D5FD84; font-size: 6pt; display:inline">Joao MC Texeira<span style="color: #08F2EE">*&nbsp;&nbsp;</span>' \
                       '<span style="color: #D5FD84; font-size: 6pt;">Simon P. Skinner</span><span style="color: #07C3F5">**&nbsp;&nbsp;</span>' \
                       '<span style="color: #D5FD84; font-size: 6pt;"> Miguel Arbes&#250;</span><span style="color: #08F2EE">*&nbsp;&nbsp;</span>' \
                       '<span style="color: #D5FD84; font-size: 6pt;"> Alexander L. Breeze</span><span style="color: #07C3F5">**&nbsp;&nbsp;</span>' \
                       '<span style="color: #D5FD84; font-size: 6pt;"> Miquel Pons</span><span style="color: #08F2EE">*</span>'
        address1 = '<span style="color: #08F2EE; font-size: 6pt;">* BioNMR Laboratory, Inorganic and Organic Chemistry Department, Universitat de Barcelona, Baldiri Reixac 10-12, 08028 Barcelona, Spain</span>'
        address2 = '<span style="color: #07C3F5; font-size: 6pt;">** Astbury Centre for Structural Molecular Biology, Faculty of Biological Sciences, University of Leeds, LS2 9JT, UK</span>'
        #
        self.label1 = QLabel(affiliations, self)
        self.label2 = QLabel(address1, self)
        self.label3 = QLabel(address2, self)
        self.label1.setObjectName('label1')
        #
        layout = QGridLayout()
        self.setLayout(layout)
        # self.layout().setSpacing(6)
        self.layout().addWidget(self.label1, 0, 0)
        self.layout().addWidget(self.label2, 1, 0)
        self.layout().addWidget(self.label3, 2, 0)
        #
        self.paper_button = QToolButton()
        self.paper_button.setIcon(Icon(os.path.join('icons', 'footer-icon-paper.png')))
        self.paper_button.setCheckable(True)
        self.paper_button.toggled.connect(self.link_to_article)
        #
        self.documentation = QToolButton()
        self.documentation.setIcon(Icon(os.path.join('icons', 'footer-icon-documentation.png')))
        self.documentation.setCheckable(True)
        self.documentation.toggled.connect(self.show_documentation)
        #
        self.mailing_list_button = QToolButton()
        self.mailing_list_button.setIcon(Icon(os.path.join('icons', 'footer-icon-email.png')))
        self.mailing_list_button.setCheckable(True)
        self.mailing_list_button.toggled.connect(self.mailing_list)
        #
        self.git_button = QToolButton()
        # icon from
        # https://www.iconsdb.com/caribbean-blue-icons/github-11-icon.html
        self.git_button.setIcon(Icon(os.path.join('icons', 'footer-icon-git.png')))
        self.git_button.setCheckable(True)
        self.git_button.toggled.connect(self.show_git)
        #
        self.rg = QToolButton()
        self.rg.setIcon(Icon(os.path.join('icons', 'footer-icon-rg.png')))
        self.rg.setCheckable(True)
        self.rg.toggled.connect(self.open_research_gate)
        #
        self.twitter_button = QToolButton()
        self.twitter_button.setCheckable(True)
        self.twitter_button.setIcon(Icon(os.path.join('icons', 'footer-icon-twitter.png')))
        self.twitter_button.toggled.connect(self.open_twitter)
        #
        self.paper_button.setIconSize(self.paper_button.size())
        self.mailing_list_button.setIconSize(self.mailing_list_button.size())
        self.documentation.setIconSize(self.documentation.size())
        self.git_button.setIconSize(self.git_button.size())
        self.rg.setIconSize(self.rg.size())
        self.twitter_button.setIconSize(self.twitter_button.size())
        #
        self.layout().addWidget(self.paper_button, 0, 4, 3, 1)
        self.layout().addWidget(self.documentation, 0, 5, 3, 1)
        self.layout().addWidget(self.mailing_list_button, 0, 6, 3, 1)
        self.layout().addWidget(self.git_button, 0, 7, 3, 1)
        self.layout().addWidget(self.rg, 0, 8, 3, 1)
        self.layout().addWidget(self.twitter_button, 0, 9, 3, 1)
        #
        footer_version_code = "v{0[0]}.{0[1]}.{0[2]}"
        farseer_version = footer_version_code.format(system.farseer_version)
        version = '<span style="color: #036D8F; font-size: 6pt; ' \
                  'font-weight: 400; margin-right: 29px; margin-top: 4px;"' \
                  '>{}&nbsp;&nbsp;&nbsp;&nbsp;</span>'.format(farseer_version)
        self.versionLabel = QLabel(version, self)
        self.versionLabel.setAlignment(QtCore.Qt.AlignRight)
        #
        spacerLabel = QLabel('', self)
        #
        self.layout().addWidget(spacerLabel, 0, 3)
        self.layout().addWidget(self.versionLabel, 0, 10, 1, 1)
        #
        self.ctfpLabel = QLabel('', self)
        pixmap = QtGui.QPixmap(os.path.join(ICON_DIR, 'icons', 'footer-artistic-systems.png'))
        self.ctfpLabel.setPixmap(pixmap)
        self.ctfpLabel.setAlignment(QtCore.Qt.AlignRight)
        self.layout().addWidget(self.ctfpLabel, 1, 9, 2, 2)

    def link_to_article(self):
        webbrowser.open_new_tab(
            "https://link.springer.com/article/10.1007%2Fs10858-018-0182-5"
            )
    
    def show_documentation(self):
        webbrowser.open_new_tab(
            "https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Farseer-NMR_Documentation.pdf"
            )

    def mailing_list(self):
        webbrowser.open_new_tab(
            "https://groups.google.com/forum/#!forum/farseer-nmr"
            )
    
    def show_git(self):
        webbrowser.open_new_tab("https://github.com/Farseer-NMR/FarSeer-NMR")
    
    def open_research_gate(self):
        webbrowser.open_new_tab(
            "https://www.researchgate.net/project/Farseer-NMR-automatic-treatment-analysis-and-plotting-of-large-multi-variable-NMR-data"
            )
    
    
    def open_twitter(self):
        webbrowser.open_new_tab("https://twitter.com/farseer_nmr")

#    def send_email(self):
#        webbrowser.open('mailto:?to=farseer.nmr@gmail.com', new=1)
