from PyQt5.QtWidgets import (QApplication, QWidget, QCheckBox, QLabel, QGridLayout, QSpinBox, QLineEdit,
                             QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsLineItem, QTreeWidget, QTreeWidgetItem,
                             QPushButton)
from PyQt5 import QtCore
import sys
from functools import partial

valuesDict = {
            'x': [],
            'y': [],
            'z': []
        }

width = 600
height = 400

class Interface(QWidget):

    def __init__(self):
        QWidget.__init__(self, parent=None)

        self.initUI()

    def initUI(self):
        self.peakListArea = PeakListArea(self)
        grid = QGridLayout()
        grid1 = QGridLayout()
        grid2 = QGridLayout()
        grid.setVerticalSpacing(0)
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)


        widget1 = QWidget(self)
        widget1.setLayout(grid1)
        self.widget2 = QWidget(self)
        self.widget2.setLayout(grid2)
        axes_label = QLabel("Use axes", self)
        x_checkbox = LabelledCheckbox(self, "x")
        y_checkbox = LabelledCheckbox(self, "y")
        z_checkbox = LabelledCheckbox(self, "z")
        self.widget2.layout().addWidget(axes_label, 0, 0, 1, 1)
        self.widget2.layout().addWidget(x_checkbox, 3, 0)
        self.widget2.layout().addWidget(y_checkbox, 2, 0)
        self.widget2.layout().addWidget(z_checkbox, 1, 0)

        self.sideBar = SideBar(self)

        self.layout().addWidget(self.sideBar, 0, 0, 4, 1)

        num_points_label = QLabel("Number of Points", self)

        grid2.layout().addWidget(num_points_label, 0, 1)

        self.z_combobox = QSpinBox(self)
        self.y_combobox = QSpinBox(self)
        self.x_combobox = QSpinBox(self)

        self.x_combobox.valueChanged.connect(partial(self.update_condition_boxes, 3, 'x'))
        self.y_combobox.valueChanged.connect(partial(self.update_condition_boxes, 2, 'y'))
        self.z_combobox.valueChanged.connect(partial(self.update_condition_boxes, 1, 'z'))

        self.z_combobox.setFixedWidth(100)
        self.y_combobox.setFixedWidth(100)
        self.x_combobox.setFixedWidth(100)

        grid2.layout().addWidget(self.x_combobox, 3, 1, 1, 1)
        grid2.layout().addWidget(self.y_combobox, 2, 1, 1, 1)
        grid2.layout().addWidget(self.z_combobox, 1, 1, 1, 1)

        self.z_combobox.setValue(1)
        self.y_combobox.setValue(1)
        self.x_combobox.setValue(1)

        self.layout().addWidget(self.widget2, 1, 1)

        self.showTreeButton = QPushButton('Show Parameter Tree', self)

        self.layout().addWidget(self.showTreeButton, 2, 1, 1, 3)
        self.layout().addWidget(self.peakListArea, 3, 1, 1, 3)
        # self.peakListArea.updateTree(1, 1, 1)
        self.showTreeButton.clicked.connect(self.peakListArea.updateTree)
        
    def update_condition_boxes(self, row, dim, value):

        self.x, self.y, self.z = self.x_combobox.value(), self.y_combobox.value(), self.z_combobox.value()
        layout = self.widget2.layout()
        colCount = layout.columnCount()
        for m in range(2, colCount):
            item = layout.itemAtPosition(row, m)
            if item:
                if item.widget():
                    item.widget().hide()
            layout.removeItem(item)
        if len(valuesDict[dim]) < value:
            [valuesDict[dim].append(0) for x in range(value-len(valuesDict[dim]))]
        if len(valuesDict[dim]) > value:
            valuesDict[dim] = valuesDict[dim][:value]
        for x in range(value):
            text_box = ValueField(self, x, dim)
            text_box.setFixedWidth(50)
            text_box.setText(str(valuesDict[dim][x]))
            layout.addWidget(text_box, row, x+2, 1, 1)


class ValueField(QLineEdit):

    def __init__(self, parent, index, dim):
        QLineEdit.__init__(self, parent)
        self.index = index
        self.dim = dim
        self.textChanged.connect(self.updateValuesDict)

    def updateValuesDict(self, value):
        valuesDict[self.dim][self.index] = value


class PeakListArea(QWidget):
    def __init__(self, parent):

        QWidget.__init__(self, parent)
        self.scene = QGraphicsScene(self)
        self.scrollContents = QGraphicsView(self.scene, self)
        layout = QGridLayout()
        self.setLayout(layout)
        self.layout().addWidget(self.scrollContents)
        self.scrollContents.setFixedSize(width, height)
        self.scrollContents.setAcceptDrops(True)
        # self.setAcceptDrops(True)
        self.setEvents()


    def setEvents(self):
        self.scrollContents.scene().dragEnterEvent = self._dragEnterEvent

    def _dragEnterEvent(self, event):
        event.accept()


    def updateTree(self):
        self.parent().sideBar.addLists()
        self.scene.clear()
        z_conds = valuesDict['z']
        y_conds = valuesDict['y']
        x_conds = valuesDict['x']
        # z_conds = ['298K', '278K']
        # y_conds = ['dia', 'para']
        # x_conds = [0, 10, 50]
        num_x = len(x_conds)
        num_y = len(y_conds)
        num_z = len(z_conds)
        total_x = num_x*num_y*num_z
        x_spacing = height/total_x
        y_spacing = height/(num_z*num_y)
        z_spacing = height /2
        zz_pos = 0
        yy_pos = width*0.25
        xx_pos = width*0.5
        pl_pos = width*0.75

        xx_vertical = -height / 2
        yy_vertical = -height / 2 + x_spacing
        zz_vertical = -height / 3.5
        num = 0
        for i, z in enumerate(z_conds):
            if i % 2 == 0:
                z = ConditionLabel(str(z), [zz_pos, zz_vertical])
                self.scene.addItem(z)
                zz_vertical += z_spacing
            else:
                z = ConditionLabel(str(z), [zz_pos, zz_vertical])
                self.scene.addItem(z)
                zz_vertical += z_spacing
            for j, y in enumerate(y_conds):
                y = ConditionLabel(str(y), [yy_pos, yy_vertical])
                self.scene.addItem(y)
                self._addConnectingLine(z, y)
                yy_vertical+=y_spacing
                for k, x in enumerate(x_conds):
                    x = ConditionLabel(str(x), [xx_pos, xx_vertical])
                    self.scene.addItem(x)
                    self._addConnectingLine(y, x)
                    pl = PeakListLabel('Drop peaklist here', self.scene, [pl_pos, xx_vertical])
                    self.scene.addItem(pl)
                    xx_vertical+=x_spacing
                    self._addConnectingLine(x, pl)
                    num+=1


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
    self.setPlainText(mimeData.text())
    event.accept()



class LabelledCheckbox(QWidget):

    def __init__(self, parent, text, callback=None, **kw):
        QWidget.__init__(self, parent)
        grid = QGridLayout()
        self.setLayout(grid)
        checkBox = QCheckBox()

        label = QLabel(text, self)
        self.layout().addWidget(checkBox, 0, 0)
        self.layout().addWidget(label, 0, 1)
        self.setFixedWidth(50)

        if callback:
            self.setCallback(callback)

    def setCallback(self, callback):
        self.connect(self, QtCore.SIGNAL('clicked()'), callback)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    ex.raise_()
    sys.exit(app.exec_())
