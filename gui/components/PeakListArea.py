from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsScene, QGraphicsView, QGraphicsLineItem, QGraphicsTextItem, QMessageBox, QMenu
from PyQt5 import QtCore, QtGui
import pickle

width = 600

import math

class PeakListArea(QWidget):
    def __init__(self, parent, variables, gui_settings):

        QWidget.__init__(self, parent)
        self.scene = QGraphicsScene(self)
        self.height = gui_settings['peaklistarea_height']
        self.scrollContents = QGraphicsView(self.scene, self)
        self.scrollContents.setRenderHint(QtGui.QPainter.Antialiasing)
        self.scene.setSceneRect(0, 0, width, self.height)
        layout = QGridLayout()
        self.setLayout(layout)
        self.layout().addWidget(self.scrollContents)
        self.scrollContents.setMinimumSize(gui_settings['scene_width'], gui_settings['scene_height'])
        self.scrollContents.setAcceptDrops(True)
        self.variables = variables
        self.setEvents()
        self.updateClicks = 0


    def setEvents(self):
        self.scrollContents.scene().dragEnterEvent = self._dragEnterEvent

    def _dragEnterEvent(self, event):
        event.accept()


    def sideBar(self):
        return self.parent().parent().parent().sideBar


    def update_variables(self, variables):
        self.variables = variables
        self.updateTree()

    def show_update_warning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Reset Experimental Series")
        msg.setInformativeText("Do you want to all peaklists from the Experimental Series and re-draw the series?")
        msg.setWindowTitle("Reset Experimental Series")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()
        return retval

    def show_duplicate_key_warning(self, axis):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Duplicate conditions")
        msg.setInformativeText("There are duplicate conditions on the %s axis. " % axis)
        msg.setWindowTitle("Duplicate conditions")
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()
        return retval

    def show_empty_condition_warning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Empty conditions")
        msg.setInformativeText("There are empty conditions, so dataset cannot be drawn.")
        msg.setWindowTitle("Empty conditions")
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()
        return retval
    #
    def update_experimental_dataset(self, valuesDict):

        tmp_dict = {}
        for z in valuesDict["z"]:
            tmp_dict[z] = {}
            for y in valuesDict["y"]:
                tmp_dict[z][y] = {}
                for x in valuesDict["x"]:
                    tmp_dict[z][y][x] = ''
                    if self.variables["experimental_dataset"][z][y].keys():
                        tmp_dict[z][y][x] = self.variables["experimental_dataset"][z][y][x]
        return tmp_dict


    def check_conditions_for_tree(self):

        self.valuesDict = self.variables["conditions"]
        print(self.valuesDict)
        #
        # Check if condition boxes are empty and throw warning if so.
        if not all(x for v in self.valuesDict.values() for x in v):
            self.show_empty_condition_warning()
            return False

        if len(set(self.valuesDict['z'])) != len(self.valuesDict['z']):
            self.show_duplicate_key_warning('z')
            return False

        if len(set(self.valuesDict['y'])) != len(self.valuesDict['y']):
            self.show_duplicate_key_warning('y')
            return False

        if len(set(self.valuesDict['x'])) != len(self.valuesDict['x']):
            self.show_duplicate_key_warning('x')
            return False

        return True


    def updateTree(self):


        if not self.check_conditions_for_tree():
            return

        if self.updateClicks > 0:
            self.show_update_warning()


        self.peak_list_objects = []
        self.fasta_files = {}
        self.peak_list_dict = {}
        self.show()
        self.sideBar().refresh_sidebar()
        self.scene.clear()
        z_conds = self.valuesDict['z']
        y_conds = self.valuesDict['y']
        x_conds = self.valuesDict['x']
        num_x = len(x_conds)
        num_y = len(y_conds)
        num_z = len(z_conds)
        total_x = num_x*num_y*num_z
        if total_x > 10:
            self.scrollContents.setSceneRect(0, 0, width, total_x * 22)
        else:
            self.scrollContents.setSceneRect(0, 0, width, self.height)

        self.scrollContents.fitInView(0, 0, width, self.height, QtCore.Qt.KeepAspectRatio)

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
                    # if not z in self.variables["experimental_dataset"].keys() or not self.variables["experimental_dataset"][z][y][x]:
                    pl = PeakListLabel(self, 'Drop peaklist here', self.scene,
                                   [pl_pos, xx_vertical], x_cond=x, y_cond=y, z_cond=z)
                    self.peak_list_dict[z][y][x] = ''
                    # else:
                    #     pl_name = self.variables["experimental_dataset"][z][y][x]
                    #     pl = PeakListLabel(self, pl_name, self.scene,
                    #                        [pl_pos, xx_vertical], x_cond=x, y_cond=y, z_cond=z, peak_list=pl_name)
                    #     self.peak_list_dict[z][y][x] = pl_name
                    #     self.sideBar().removeItem(pl_name)

                    self.peak_list_objects.append(pl)
                    self.scene.addItem(pl)
                    self._addConnectingLine(xx, pl)
                    x_markers.append(xx)
                    num+=1
                    xx_vertical += x_spacing
                if len(x_markers) % 2 == 1:
                    yy_vertical = x_markers[int(math.ceil(len(x_markers))/2)].y()
                else:
                    yy_vertical = x_markers[int(math.ceil(len(x_markers))/2)].y()-(x_spacing/2)
                yy = ConditionLabel(str(y), [yy_pos, yy_vertical])
                y_markers.append(yy)
                self.scene.addItem(yy)
                for x_marker in x_markers:
                    self._addConnectingLine(yy, x_marker)
            if len(y_markers) % 2 == 1:
                zz_vertical = y_markers[int(math.ceil(len(y_markers))/2)].y()
            else:
                zz_vertical = (y_markers[0].y()+y_markers[-1].y())/2
            zz = ConditionLabel(str(z), [zz_pos, zz_vertical])
            self.scene.addItem(zz)
            for x_marker in y_markers:
                self._addConnectingLine(zz, x_marker)

        self.updateClicks += 1
        # self.variables["fasta_files"] = self.fasta_files
        self.variables["experimental_dataset"] = self.peak_list_dict

    def _addConnectingLine(self, atom1, atom2):
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


        newLine = QGraphicsLineItem(x1, y1, x2, y2)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("#FAFAF7"))
        pen.setCosmetic(True)
        pen.setWidth(1)
        newLine.setPen(pen)
        self.scene.addItem(newLine)


class ConditionLabel(QGraphicsTextItem):


  def __init__(self, text, pos=None):
      QGraphicsTextItem.__init__(self)
      self.setHtml('<div style="color: %s; font-size: 10pt; ">%s</div>' % ('#FAFAF7', text))
      self.setPos(QtCore.QPointF(pos[0], pos[1]))

class PeakListLabel(QGraphicsTextItem):

  def __init__(self, parent, text, scene, pos=None, x_cond=None, y_cond=None, z_cond=None, peak_list=None):
      QGraphicsTextItem.__init__(self)
      self.setHtml('<div style="color: %s; font-size: 10pt;">%s</div>' % ('#FAFAF7', text))
      self.setPos(QtCore.QPointF(pos[0], pos[1]))
      self.setAcceptDrops(True)
      self.scene = scene
      self.x_cond = x_cond
      self.y_cond = y_cond
      self.z_cond = z_cond
      self.peak_list = peak_list
      self.peak_list_dict = parent.peak_list_dict
      self.sideBar = parent.sideBar

  def mousePressEvent(self, event):

      if event.button() == QtCore.Qt.RightButton:
          if self.peak_list:
            self._raiseContextMenu(event)


  def _raiseContextMenu(self, event):
      contextMenu = QMenu()
      contextMenu.addAction('Delete', self.removeItem)
      contextMenu.exec_(event.screenPos())

  def removeItem(self):
      self.setHtml('<div style="color: %s; font-size: 10pt;">%s</div>' % ('#FAFAF7', "Drop peaklist here"))
      self.sideBar().addItem(self.peak_list)
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
        self.setHtml('<div style="color: %s; font-size: 10pt;">%s</div>' % ('#FAFAF7', mimeData.text()))
        self.peak_list = mimeData.text()
        self.peak_list_dict[self.z_cond][self.y_cond][self.x_cond] = self.peak_list
        event.accept()
    else:
        self.sideBar().addItem(mimeData.text())
        event.ignore()

