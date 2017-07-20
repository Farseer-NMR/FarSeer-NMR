from PyQt5 import QtGui

import os

ICON_DIR = os.path.dirname(__file__)

class Icon(QtGui.QIcon):

  def __init__(self, image=None):

    assert image

    if not isinstance(image, QtGui.QIcon):
      if not os.path.exists(image):
        image = os.path.join(ICON_DIR, image)


    QtGui.QIcon.__init__(self, image)