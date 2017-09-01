from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5 import QtCore
from parsing import read_peaklist
import os


class SideBar(QTreeWidget):
    def __init__(self, parent=None, peakLists=None, gui_settings=None):
        QTreeWidget.__init__(self, parent)
        self.header().hide()
        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setDragDropMode(self.InternalMove)
        self.acceptDrops()
        self.setMinimumWidth(200)
        self.setMaximumWidth(320)

        self.setFixedHeight(gui_settings['sideBar_height'])
        self.addLists()
        self.peakLists = peakLists

    def addLists(self):
        pass

    def dragEnterEvent(self, event):
        event.accept()
        if not event.mimeData().hasUrls():

            item = self.itemAt(event.pos())
            if not item:
                pass
            text = item.text(0)
            event.mimeData().setText(text)

    def dropEvent(self, event):

        if event.mimeData().hasUrls():
            event.accept()
            filePaths = [url.path() for url in event.mimeData().urls()]
            for filePath in filePaths:
                self.load_from_path(filePath)

    def load_from_path(self, filePath):
        if os.path.isdir(filePath):
            for root, dirs, filenames in os.walk(filePath):
                for filename in filenames:
                    try:
                        path = os.path.join(root, filename)
                        self.load_peaklist(path)
                    except IOError:
                        pass
        else:
            print(filePath)
            self.load_peaklist(filePath)


    def load_peaklist(self, filePath):
        if os.path.isdir(filePath):
            return
        peaklist = read_peaklist(filePath)
        if peaklist:
            item = self.addItem(filePath.split('/')[-1].split('.')[0])
            self.peakLists[item.text(0)] = peaklist
        else:
            print("Invalid file: %s" % filePath)

    def addItem(self, name):
        newItem = QTreeWidgetItem(self)
        newItem.setFlags(newItem.flags() & ~(QtCore.Qt.ItemIsDropEnabled))
        newItem.setText(0, name)
        return newItem
