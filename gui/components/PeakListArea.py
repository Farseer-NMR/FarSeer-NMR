from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsScene, QGraphicsView, QGraphicsLineItem, QGraphicsTextItem
from PyQt5 import QtCore

width = 600
height = 650

import math

class PeakListArea(QWidget):
    def __init__(self, parent, valuesDict):

        QWidget.__init__(self, parent)
        self.scene = QGraphicsScene(self)
        self.scrollContents = QGraphicsView(self.scene, self)
        self.scene.setSceneRect(0, 0, 1100, 650)
        layout = QGridLayout()
        self.setLayout(layout)
        self.layout().addWidget(self.scrollContents)
        self.scrollContents.setMaximumSize(1100, height)
        self.scrollContents.setMinimumSize(850, height)
        self.scrollContents.setAcceptDrops(True)

        self.valuesDict = valuesDict
        self.setEvents()


    def setEvents(self):
        self.scrollContents.scene().dragEnterEvent = self._dragEnterEvent

    def _dragEnterEvent(self, event):
        event.accept()


    def updateTree(self):
        self.show()
        # self.scrollContents.setSceneRect(0, 0, self.scrollContents.frameSize().width(), self.scrollContents.frameSize().height())
        self.parent().parent().parent().sideBar.addLists()
        self.scene.clear()
        z_conds = self.valuesDict['z']
        y_conds = self.valuesDict['y']
        x_conds = self.valuesDict['x']
        num_x = len(x_conds)
        num_y = len(y_conds)
        num_z = len(z_conds)
        total_x = num_x*num_y*num_z
        x_spacing = 50
        y_spacing = height/(num_z*num_y + 2)
        z_spacing = height / (num_z + 2)
        zz_pos = 0
        yy_pos = width*0.25
        xx_pos = width*0.5
        pl_pos = width*0.75
        zz_vertical = z_spacing
        # yy_vertical = y_spacing
        xx_vertical = x_spacing



        num = 0
        for i, z in enumerate(z_conds):
            # if i % 2 == 0:
            #     z = ConditionLabel(str(z), [zz_pos, zz_vertical])
            #     print(zz_vertical, 'vert', zz_pos)
            #     self.scene.addItem(z)
            #     zz_vertical += z_spacing
            # else:
            #     z = ConditionLabel(str(z), [zz_pos, zz_vertical])
            #     self.scene.addItem(z)
            #     zz_vertical += z_spacing
                for j, y in enumerate(y_conds):
                    x_markers = []
                    for k, x in enumerate(x_conds):
                        x = ConditionLabel(str(x), [xx_pos, xx_vertical])
                        self.scene.addItem(x)
                        # self._addConnectingLine(y, x)
                        pl = PeakListLabel('Drop peaklist here', self.scene, [pl_pos, xx_vertical])
                        self.scene.addItem(pl)
                        print(xx_vertical, 'xx')
                        self._addConnectingLine(x, pl)
                        x_markers.append(x)
                        num+=1
                        xx_vertical += x_spacing
                    if len(x_conds) == 1:
                        yy_vertical = xx_vertical - x_spacing
                    else:
                        if j > 0:
                            yy_vertical = xx_vertical - (x_spacing*(1+j/2))
                        else:
                            yy_vertical = (xx_vertical / 2)

                    print(yy_vertical)
                    y = ConditionLabel(str(y), [yy_pos, yy_vertical])
                    self.scene.addItem(y)
                    for x_marker in x_markers:
                        self._addConnectingLine(y, x_marker)






    def _addConnectingLine(self, atom1, atom2):
        """
        Adds a line between two GuiNmrAtoms using the width, colour, displacement and style specified.
        """
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
        self.scene.addItem(newLine)

class ConditionLabel(QGraphicsTextItem):


  def __init__(self, text, pos=None):
      QGraphicsTextItem.__init__(self)
      self.setPlainText(text)
      self.setPos(QtCore.QPointF(pos[0], pos[1]))


class PeakListLabel(QGraphicsTextItem):

  def __init__(self, text, scene, pos=None):
      QGraphicsTextItem.__init__(self)
      self.setPlainText(text)
      self.setPos(QtCore.QPointF(pos[0], pos[1]))
      self.setAcceptDrops(True)
      self.scene = scene


  def dragEnterEvent(self, event):
    event.accept()

  def dragMoveEvent(self, event):
    event.accept()

  def dropEvent(self, event):

    mimeData = event.mimeData()
    print(mimeData.text())
    self.setPlainText(mimeData.text())
    event.accept()

