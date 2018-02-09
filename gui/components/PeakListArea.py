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
import math

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QGridLayout, QGraphicsScene,
                             QGraphicsView, QGraphicsLineItem,
                             QGraphicsTextItem, QMessageBox, QMenu)
from core.fslibs.Variables import Variables


width = 600


class PeakListArea(QWidget):
    """
    A widget containing a QGraphicsScene for rendering the drag and drop
    creation of the Farseer-NMR cube.

    When a peaklist is dropped on a PeakListLabel instance, the variables
    instance is updated and its position in the Farseer-NMR cube is specified.

    Parameters:
        parent (QWidget): specifies the parent widget containing the QLabel
            and the QSpinBox.
        gui_settings (dict): a dictionary carrying the settings required to
            correctly render the graphics based on screen resolution.

    Methods:
        .setEvents()
        .side_bar()
        .update_variables()
        .show_update_warning()
        .show_duplicate_key_warning()
        .update_experimental_dataset(values_dict)
        .check_conditions_for_tree()
        .update_tree()
        .add_connecting_line()
    """

    variables = Variables()._vars

    def __init__(self, parent, gui_settings):

        QWidget.__init__(self, parent)
        self.scene = QGraphicsScene(self)
        self.height = gui_settings['peaklistarea_height']
        self.scrollContents = QGraphicsView(self.scene, self)
        self.scrollContents.setRenderHint(QtGui.QPainter.Antialiasing)
        self.scene.setSceneRect(0, 0, width, self.height)
        layout = QGridLayout()
        self.setLayout(layout)
        self.layout().addWidget(self.scrollContents)
        self.scrollContents.setMinimumSize(gui_settings['scene_width'],
                                           gui_settings['scene_height'])
        self.scrollContents.setAcceptDrops(True)
        self.set_events()
        self.updateClicks = 0

    def set_events(self):
        self.scrollContents.scene().dragEnterEvent = self._dragEnterEvent

    def _dragEnterEvent(self, event):
        event.accept()

    def side_bar(self):
        return self.parent().parent().parent().side_bar

    def update_variables(self):
        self.update_tree()

    def show_update_warning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Reset Experimental Series")
        msg.setInformativeText("Do you want to all peaklists from the "
                               "Experimental Series and re-draw the series?")
        msg.setWindowTitle("Reset Experimental Series")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()
        return retval

    def show_duplicate_key_warning(self, axis):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Duplicate conditions")
        msg.setInformativeText("There are duplicate "
                               "conditions on the %s axis. " % axis)
        msg.setWindowTitle("Duplicate conditions")
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()
        return retval

    def show_empty_condition_warning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Empty conditions")
        msg.setInformativeText("There are empty conditions, "
                               "so dataset cannot be drawn.")
        msg.setWindowTitle("Empty conditions")
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()
        return retval

    def update_experimental_dataset(self, values_dict):

        tmp_dict = {}
        for z in values_dict["z"]:
            tmp_dict[z] = {}
            for y in values_dict["y"]:
                tmp_dict[z][y] = {}
                for x in values_dict["x"]:
                    tmp_dict[z][y][x] = ''
                    if self.variables["experimental_dataset"][z][y].keys():
                        tmp_dict[z][y][x] = \
                            self.variables["experimental_dataset"][z][y][x]
        return tmp_dict

    def check_conditions_for_tree(self):

        self.values_dict = self.variables["conditions"]

        # Check if condition boxes are empty and throw warning if so.
        if not all(x for v in self.values_dict.values() for x in v):
            self.show_empty_condition_warning()
            return False

        if len(set(self.values_dict['z'])) != len(self.values_dict['z']):
            self.show_duplicate_key_warning('z')
            return False

        if len(set(self.values_dict['y'])) != len(self.values_dict['y']):
            self.show_duplicate_key_warning('y')
            return False

        if len(set(self.values_dict['x'])) != len(self.values_dict['x']):
            self.show_duplicate_key_warning('x')
            return False

        return True

    def update_tree(self):

        if not self.check_conditions_for_tree():
            return

        if self.updateClicks > 0:
            if self.show_update_warning() == QMessageBox.Cancel:
                return

        self.peak_list_objects = []
        self.fasta_files = {}
        self.peak_list_dict = {}
        self.show()
        self.side_bar().refresh_sidebar()
        self.scene.clear()
        z_conds = self.values_dict['z']
        y_conds = self.values_dict['y']
        x_conds = self.values_dict['x']
        num_x = len(x_conds)
        num_y = len(y_conds)
        num_z = len(z_conds)
        total_x = num_x*num_y*num_z
        if total_x > 10:
            self.scrollContents.setSceneRect(0, 0, width, total_x * 22)
        else:
            self.scrollContents.setSceneRect(0, 0, width, self.height)

        self.scrollContents.fitInView(0, 0, width,
                                      self.height, QtCore.Qt.KeepAspectRatio)

        if total_x < 2:
            x_spacing = self.scene.height()/2
        elif 2 < total_x < 10:
            x_spacing = self.scene.height()/(total_x+1)
        else:
            x_spacing = 20
        zz_pos = 0
        yy_pos = self.scene.width()*0.25
        xx_pos = self.scene.width()*0.5
        pl_pos = self.scene.width()*0.75
        xx_vertical = x_spacing
        num = 0

        for i, z in enumerate(z_conds):
            self.peak_list_dict[z] = {}
            y_markers = []
            for j, y in enumerate(y_conds):
                self.peak_list_dict[z][y] = {}
                self.fasta_files[y] = ''
                x_markers = []
                for k, x in enumerate(x_conds):
                    xx = ConditionLabel(str(x), [xx_pos, xx_vertical])
                    self.scene.addItem(xx)
                    if z not in self.variables["experimental_dataset"].keys() \
                            or y not in self.variables[
                                "experimental_dataset"][z].keys() \
                            or x not in self.variables[
                                "experimental_dataset"][z][y].keys():
                        pl = PeakListLabel(self, 'Drop peaklist here',
                                           self.scene, [pl_pos, xx_vertical],
                                           x_cond=x, y_cond=y, z_cond=z)
                        self.peak_list_dict[z][y][x] = ''

                    elif not self.variables["experimental_dataset"][z][y][x]:
                        pl = PeakListLabel(self, 'Drop peaklist here',
                                           self.scene, [pl_pos, xx_vertical],
                                           x_cond=x, y_cond=y, z_cond=z)
                        self.peak_list_dict[z][y][x] = ''
                    else:
                        pl_name = self.variables["experimental_dataset"][z][y][x]
                        pl = PeakListLabel(self, pl_name, self.scene,
                                           [pl_pos, xx_vertical], x_cond=x,
                                           y_cond=y, z_cond=z,
                                           peak_list=pl_name)
                        self.peak_list_dict[z][y][x] = pl_name
                        self.side_bar()._raise_context_menu(pl_name)

                    self.peak_list_objects.append(pl)
                    self.scene.addItem(pl)
                    self.add_connecting_line(xx, pl)
                    x_markers.append(xx)
                    num += 1
                    xx_vertical += x_spacing
                if len(x_markers) % 2 == 1:
                    yy_vertical = x_markers[int(math.ceil(
                        len(x_markers))/2)].y()
                else:
                    yy_vertical = x_markers[int(math.ceil(
                        len(x_markers))/2)].y()-(x_spacing/2)
                yy = ConditionLabel(str(y), [yy_pos, yy_vertical])
                y_markers.append(yy)
                self.scene.addItem(yy)
                for x_marker in x_markers:
                    self.add_connecting_line(yy, x_marker)
            if len(y_markers) % 2 == 1:
                zz_vertical = y_markers[int(math.ceil(len(y_markers))/2)].y()
            else:
                zz_vertical = (y_markers[0].y()+y_markers[-1].y())/2
            zz = ConditionLabel(str(z), [zz_pos, zz_vertical])
            self.scene.addItem(zz)
            for x_marker in y_markers:
                self.add_connecting_line(zz, x_marker)

        self.updateClicks += 1
        self.variables["experimental_dataset"] = self.peak_list_dict

    def add_connecting_line(self, atom1, atom2):
        if atom1.y() > atom2.y():
            y1 = atom1.y() + (atom1.boundingRect().height() * .5)
            y2 = atom2.y() + (atom2.boundingRect().height() * .5)

        elif atom1.y() < atom2.y():
            y1 = atom1.y() + (atom1.boundingRect().height() * .5)
            y2 = atom2.y() + (atom2.boundingRect().height() * .5)

        else:
            y1 = atom1.y() + (atom1.boundingRect().height() * 0.5)
            y2 = atom2.y() + (atom2.boundingRect().height() * 0.5)

        if atom1.x() > atom2.x():
            x1 = atom1.x()
            x2 = atom2.x() + atom2.boundingRect().width()

        elif atom1.x() < atom2.x():
            x1 = atom1.x() + atom1.boundingRect().width()
            x2 = atom2.x()

        else:
            x1 = atom1.x() + (atom1.boundingRect().width() / 2)
            x2 = atom2.x() + (atom1.boundingRect().width() / 2)

        new_line = QGraphicsLineItem(x1, y1, x2, y2)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("#FAFAF7"))
        pen.setCosmetic(True)
        pen.setWidth(1)
        new_line.setPen(pen)
        self.scene.addItem(new_line)


class ConditionLabel(QGraphicsTextItem):
    """""
    A re-implementation of a QGraphicsTextItem to enable specification of text
    and positioning of the widget on instantiation.

    When a peaklist is dropped on a PeakListLabel instance, the variables
    instance is updated and its position in the Farseer-NMR cube is specified.

    Parameters:
        text (str): text displayed in the QGraphicsTextItem.
        pos (sequence): x and y values specifying the absolute position of the
            QGraphicsTextItem
    """
    def __init__(self, text, pos=None):

        QGraphicsTextItem.__init__(self)
        self.setHtml('<div style="color: %s; font-size: 10pt; ">%s</div>'
                     % ('#FAFAF7', text))
        self.setPos(QtCore.QPointF(pos[0], pos[1]))


class PeakListLabel(QGraphicsTextItem):
    """
    A re-implementation of a QGraphicsTextItem to enable drag and drop creation
    of the Farseer-Cube.

    The drag-and-drop behaviour has been implemented to ensure than when a
    peaklist is dragged from the side_bar onto a PeakListLabel, all the
    necessary book keeping is performed and the correct specification of the
    peaklist's conditions is recorded in the variables object. A peaklist can
    be deleted from the tree using the right mouse menu.

    Parameters:
    text (str): text displayed in the QGraphicsTextItem.
        pos (sequence): x and y values specifying the absolute position of the
           QGraphicsTextItem
        x_cond (str): condition specifying the x-axis of the Farseer-NMR cube
        y_cond (str): condition specifying the y-axis of the Farseer-NMR cube
        z_cond (str): condition specifying the z-axis of the Farseer-NMR cube
        peak_list (str): peak_list label

    Methods:
        .mousePressEvent(QMouseEvent)
        ._raise_context_menu(QMouseEvent)
        .remove_item()
        .dragEnterEvent(QMouseEvent)
        .dragMoveEvent(QMouseEvent)
        .dropEvent(QMouseEvent)

    """
    def __init__(self, parent, text, scene, pos=None,
                 x_cond=None, y_cond=None, z_cond=None, peak_list=None):

        QGraphicsTextItem.__init__(self)

        self.setHtml('<div style="color: %s; font-size: 10pt;">%s</div>'
                     % ('#FAFAF7', text))
        self.setPos(QtCore.QPointF(pos[0], pos[1]))
        self.setAcceptDrops(True)
        self.scene = scene
        self.x_cond = x_cond
        self.y_cond = y_cond
        self.z_cond = z_cond
        self.peak_list = peak_list
        self.peak_list_dict = parent.peak_list_dict
        self.side_bar = parent.side_bar

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.RightButton:
            if self.peak_list:
                self._raise_context_menu(event)
            else:
                print('no_peaklist')

    def _raise_context_menu(self, event):
        contextMenu = QMenu()
        contextMenu.addAction('Delete', self.remove_item)
        contextMenu.exec_(event.screenPos())

    def remove_item(self):
        self.setHtml('<div style="color: %s; font-size: 10pt;">%s</div>' %
                     ('#FAFAF7', "Drop peaklist here"))
        self.side_bar().add_item(self.peak_list)
        self.peak_list = None

    def dragEnterEvent(self, event):
        if not self.peak_list:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if not self.peak_list:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not self.peak_list:
            mimeData = event.mimeData()
            self.setHtml('<div style="color: %s; font-size: 10pt;">%s</div>'
                         % ('#FAFAF7', mimeData.text()))
            self.peak_list = mimeData.text()
            self.peak_list_dict[self.z_cond][self.y_cond][self.x_cond] = \
            self.peak_list
            event.accept()
        else:
            self.sideBar().addItem(event.mimeData.text())
            event.ignore()
