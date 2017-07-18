from PyQt5 import QtGui

import os

ICON_DIR = os.path.dirname(__file__)
print(ICON_DIR)

class Icon(QtGui.QIcon):

  def __init__(self, image=None, color=None):

    assert image or color


    if color:
      image = QtGui.QPixmap(10, 10)
      painter = QtGui.QPainter(image)

      if isinstance(color, str):
        color = QtGui.QColor(color[:7])
        image.fill(color)

      elif isinstance(color, (tuple, list)):
        image.fill(color[0][:7])
        dx = 22.0/float(len(color))

        x = dx
        for i, c in enumerate(color[1:]):
          col = QtGui.QColor(c[:7])
          painter.setPen(col)
          painter.setBrush(col)
          painter.drawRect(x,0,x+dx,21)
          x += dx

      else:
        image.fill(color)

      painter.setPen(QtGui.QColor('#000000'))
      painter.setBrush(QtGui.QBrush())
      painter.drawRect(0,0,45,37)
      painter.end()


    elif not isinstance(image, QtGui.QIcon):
      if not os.path.exists(image):
        image = os.path.join(ICON_DIR, image)
        print(os.path.exists(image), image)


    QtGui.QIcon.__init__(self, image)