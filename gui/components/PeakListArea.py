from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsScene, QGraphicsView, QGraphicsLineItem, QGraphicsTextItem
from PyQt5 import QtCore, QtGui
import pickle

width = 1200
height = 660

import math

class PeakListArea(QWidget):
    def __init__(self, parent, valuesDict, gui_settings):

        QWidget.__init__(self, parent)
        # self.setStyleSheet("")
        self.scene = QGraphicsScene(self)
        self.scrollContents = QGraphicsView(self.scene, self)
        self.scrollContents.setRenderHint(QtGui.QPainter.Antialiasing)
        self.scene.setSceneRect(0, 0, width, height)
        layout = QGridLayout()
        self.setLayout(layout)
        self.layout().addWidget(self.scrollContents)
        # self.scrollContents.setMaximumSize(1100, height)
        self.scrollContents.setMinimumSize(920, height)
        self.scrollContents.setAcceptDrops(True)

        self.valuesDict = valuesDict
        self.setEvents()


    def setEvents(self):
        self.scrollContents.scene().dragEnterEvent = self._dragEnterEvent

    def _dragEnterEvent(self, event):
        event.accept()


    def updateTree(self):
        self.peak_list_objects = []
        self.show()
        self.parent().parent().parent().sideBar.addLists()
        self.scene.clear()
        z_conds = self.valuesDict['z']
        y_conds = self.valuesDict['y']
        x_conds = self.valuesDict['x']
        num_x = len(x_conds)
        num_y = len(y_conds)
        num_z = len(z_conds)
        total_x = num_x*num_y*num_z
        if total_x < 2:
            x_spacing = self.scene.height()/2
        else:
            x_spacing = self.scene.height()/(total_x+1)
        zz_pos = 0
        yy_pos = self.scene.width()*0.25
        xx_pos = self.scene.width()*0.5
        pl_pos = self.scene.width()*0.75
        xx_vertical = x_spacing
        num = 0
        for i, z in enumerate(z_conds):
                y_markers = []
                for j, y in enumerate(y_conds):
                    x_markers = []
                    for k, x in enumerate(x_conds):
                        xx = ConditionLabel(str(x), [xx_pos, xx_vertical])
                        self.scene.addItem(xx)
                        # self._addConnectingLine(y, x)
                        pl = PeakListLabel('Drop peaklist here', self.scene, [pl_pos, xx_vertical], x_cond=x, y_cond=y, z_cond=z)
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
                # y_markers.append(y)
                self.scene.addItem(zz)
                for x_marker in y_markers:
                    self._addConnectingLine(zz, x_marker)


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
      self.setHtml('<div style="color: %s; font-size: 12pt; ">%s</div>' % ('#FAFAF7', text))
      self.setPos(QtCore.QPointF(pos[0], pos[1]))

class PeakListLabel(QGraphicsTextItem):

  def __init__(self, text, scene, pos=None, x_cond=None, y_cond=None, z_cond=None):
      QGraphicsTextItem.__init__(self)
      self.setHtml('<div style="color: %s; font-size: 12pt;">%s</div>' % ('#FAFAF7', text))
      self.setPos(QtCore.QPointF(pos[0], pos[1]))
      self.setAcceptDrops(True)
      self.scene = scene
      self.x_cond = x_cond
      self.y_cond = y_cond
      self.z_cond = z_cond
      self.peak_list = None

  def dragEnterEvent(self, event):
    event.accept()

  def dragMoveEvent(self, event):
    event.accept()

  def dropEvent(self, event):

    mimeData = event.mimeData()
    self.setPlainText(mimeData.text())
    self.peak_list = mimeData.text()
    event.accept()

