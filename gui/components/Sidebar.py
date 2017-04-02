from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5 import QtCore

class SideBar(QTreeWidget):
    def __init__(self, parent=None):
        QTreeWidget.__init__(self, parent)
        # self.header().hide()
        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setDragDropMode(self.InternalMove)
        self.acceptDrops()
        self.setMinimumWidth(200)
        self.addLists()

    def addLists(self):
        self.clear()
        for i in range(1, 13):
            self.projectItem = QTreeWidgetItem(self)
            self.projectItem.setFlags(self.projectItem.flags() & ~(QtCore.Qt.ItemIsDropEnabled))
            self.projectItem.setText(0, "peaklist%s" % str(i))

    def dragEnterEvent(self, event):
        event.accept()
        item = self.itemAt(event.pos())
        text = item.text(0)
        event.mimeData().setText(text)

    def dropEvent(self, event):
        event.accept()
        print(event.data())