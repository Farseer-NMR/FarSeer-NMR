from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5 import QtCore
from parsing import read_peaklist
import os


class SideBar(QTreeWidget):
    def __init__(self, parent=None, peakLists=None, gui_settings=None, variables=None):
        QTreeWidget.__init__(self, parent)
        self.header().hide()
        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setDragDropMode(self.InternalMove)
        self.acceptDrops()
        self.setMinimumWidth(200)
        self.setMaximumWidth(320)
        self.setFixedHeight(gui_settings['sideBar_height'])
        self.peakLists = peakLists
        self.setSortingEnabled(True)
        if variables:
            self.update_from_config(variables)


    def update_from_config(self, variables):
        self.clear()
        self.variables = variables["peaklists"]
        for peaklist in self.variables.values():
            self.load_peaklist(peaklist)

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
                name, path = self.load_from_path(filePath)
                self.variables[name] = path

    def load_from_path(self, filePath):
        if os.path.isdir(filePath):
            for root, dirs, filenames in os.walk(filePath):
                for filename in filenames:
                    try:
                        path = os.path.join(root, filename)
                        name, path = self.load_peaklist(path)
                    except IOError:
                        pass
        else:
            name, path = self.load_peaklist(filePath)
        return name, path



    def refresh_sidebar(self):
        self.clear()
        for peaklist in self.peakLists.keys():
            self.addItem(peaklist)

    def load_peaklist(self, filePath):
        if os.path.isdir(filePath):
            return
        peaklist = read_peaklist(filePath)

        if peaklist:
            name = filePath.split('/')[-1].split('.')[0]
            if not name in self.peakLists.keys():
                pl_name = name
            else:
                if any([name+'_' in x for x in self.peakLists.keys()]):
                    number = int(self.peakLists.keys()[-1].split('_')[1])+1
                    pl_name = name+'_%s' % number
                else:
                    pl_name = name + '_1'
            item = self.addItem(pl_name)
            self.peakLists[item.text(0)] = peaklist
            return pl_name, filePath
        else:
            print("Invalid file: %s" % filePath)

    def addItem(self, name):
        newItem = QTreeWidgetItem(self)
        newItem.setFlags(newItem.flags() & ~(QtCore.Qt.ItemIsDropEnabled))
        newItem.setText(0, name)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        return newItem

    def removeItem(self, item_name):
        import sip
        result = self.findItems(item_name, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0)
        sip.delete(result[0])
