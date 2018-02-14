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
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QTreeWidget, QTreeWidgetItem

from core.parsing import read_peaklist

from core.fslibs.Variables import Variables


class SideBar(QTreeWidget):
    """
    A QTreeWidget that enables drag-and-drop loading and parsing of peaklists.

    Peaklist files are dropped onto the sidebar, their format is detected and
    they are loaded into Farseer-NMR identified by the file name. The labels in
    the sidebar point to in memory representations of the peaklists, which are
    parsed out when a calculation is executed.


    Parameters:
        parent (QWidget):
        gui_settings (dict): a dictionary carrying the settings required to
            correctly render the graphics based on screen resolution.

    Methods:
        .update_from_config()
        .dragEnterEvent(QMouseEvent)
        .dropEvent(QMouseEvent)
        .load_from_path(str)
        .refresh_sidebar()
        .load_peaklist(str)
        .add_item(str)
        ._raise_context_menu(str)
        """
    variables = Variables()._vars

    def __init__(self, parent=None, gui_settings=None):
        QTreeWidget.__init__(self, parent)
        self.header().hide()
        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setDragDropMode(self.InternalMove)
        self.acceptDrops()
        self.setMinimumWidth(200)
        self.setMaximumWidth(320)
        self.setFixedHeight(gui_settings['sideBar_height'])
        self.peakLists = self.variables['peaklists']
        self.setSortingEnabled(True)
        self.update_from_config()

    def update_from_config(self):
        """Update sidebar contents based on configuration file."""
        self.clear()
        used_peaklists = []
        self.peakLists = self.variables["peaklists"]

        if not all(
                x for v in self.variables["conditions"].values() for x in v):
            self.refresh_sidebar()

        else:
            for z in self.variables["conditions"]["z"]:
                for y in self.variables["conditions"]["y"]:
                    for x in self.variables["conditions"]["x"]:
                        used_peaklists.append(
                            self.variables["experimental_dataset"][z][y][x])

            unused_peaklists = [x for x, pl in self.variables[
                "peaklists"].items() if x not in used_peaklists]
            for peaklist in unused_peaklists:
                self.add_item(peaklist)

    def dragEnterEvent(self, event):
        """Re-implemenation for drag-and-drop behaviour."""
        event.accept()
        if not event.mimeData().hasUrls():

            item = self.itemAt(event.pos())
            if not item:
                pass
            text = item.text(0)
            event.mimeData().setText(text)

    def dropEvent(self, event):
        """Re-implemenation for drag-and-drop behaviour."""
        if event.mimeData().hasUrls():
            event.accept()
            file_paths = [url.path() for url in event.mimeData().urls()]
            for file_path in file_paths:
                self.load_from_path(file_path)

    def load_from_path(self, file_path):
        """load a peaklists from a directory path."""
        name = None
        if os.path.isdir(file_path):
            for root, dirs, filenames in os.walk(file_path):
                for filename in filenames:
                    try:
                        path = os.path.join(root, filename)
                        name, path = self.load_peaklist(path)
                    except IOError:
                        pass
        else:
            name, path = self.load_peaklist(file_path)
        if name:
            return name, path

    def refresh_sidebar(self):
        """ clear the sidebar and refresh the peaklist names."""
        self.clear()
        for peaklist in self.peakLists.keys():
            self.add_item(peaklist)

    def load_peaklist(self, file_path):
        """load individual peaklist from a file path."""
        if os.path.isdir(file_path):
            return

        name = file_path.split('/')[-1].split('.')[0]

        if name not in self.peakLists.keys():
            peaklist = read_peaklist(file_path)
            if peaklist:
                pl_name = name
                if peaklist[0].format in ['nmrdraw', 'nmrview']:
                    print(peaklist[0].format)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("NmrView/NmrDraw Peaklist")
                    msg.setInformativeText("This peaklist doesn't contain"
                                           "residue types. Please ensure an "
                                           "approriate FASTA file is present "
                                           "in the correct y condition")
                    msg.setWindowTitle("Duplicate conditions")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    self.variables['fasta_settings']['applyFASTA'] = True


                item = self.add_item(pl_name)
                self.peakLists[item.text(0)] = peaklist
                self.peakLists[pl_name] = file_path

                return pl_name, file_path
            else:
                print("Invalid peak list file: %s" % file_path)
                return None, None
        else:
            print('Peaklist with name %s already exists.' % name)
            return None, None

    def add_item(self, name):
        """Add a peaklist pointer to the side bar as a QTreeWidgetItem."""
        newItem = QTreeWidgetItem(self)
        newItem.setFlags(newItem.flags() & ~QtCore.Qt.ItemIsDropEnabled)
        newItem.setText(0, name)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        return newItem

    def _raise_context_menu(self, item_name):
        """raise a context menu to enabled deletion of objects."""
        import sip
        result = self.findItems(item_name, QtCore.Qt.MatchRecursive, 0)
        if result:
            sip.delete(result[0])
