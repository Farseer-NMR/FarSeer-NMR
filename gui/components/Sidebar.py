from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5 import QtCore
from parsing import read_peaklist


class SideBar(QTreeWidget):
    def __init__(self, parent=None, peakLists=None):
        QTreeWidget.__init__(self, parent)
        self.header().hide()
        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setDragDropMode(self.InternalMove)
        self.acceptDrops()
        self.setMinimumWidth(200)
        self.setMaximumWidth(320)
        self.addLists()
        self.peakLists = peakLists

    def addLists(self):
        pass

    def dragEnterEvent(self, event):
        event.accept()
        if not event.mimeData().hasUrls():

            item = self.itemAt(event.pos())
            text = item.text(0)
            event.mimeData().setText(text)

    def dropEvent(self, event):
        event.accept()
        if event.mimeData().hasUrls():
            filePaths = [url.path() for url in event.mimeData().urls()]
            for filePath in filePaths:
                peaklist = read_peaklist(filePath)
                if peaklist:
                    item = self.addItem(filePath.split('/')[-1].split('.')[0])
                    self.peakLists[item.text(0)] = peaklist
                else:
                    print("Invalid file")


    def addItem(self, name):
        newItem = QTreeWidgetItem(self)
        newItem.setFlags(newItem.flags() & ~(QtCore.Qt.ItemIsDropEnabled))
        newItem.setText(0, name)
        return newItem
