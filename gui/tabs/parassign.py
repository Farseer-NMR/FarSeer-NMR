from functools import partial
import os

from PyQt5 import QtCore


from PyQt5.QtWidgets import QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, \
    QLabel, QMessageBox, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox

from gui.popups.BarPlotPopup import BarPlotPopup
from gui.popups.ExtendedBarPopup import ExtendedBarPopup
from gui.popups.CompactBarPopup import CompactBarPopup
from gui.popups.CSPExceptionsPopup import CSPExceptionsPopup
from gui.popups.FastaSelectionPopup import FastaSelectionPopup
from gui.popups.GeneralResidueEvolution import GeneralResidueEvolution
from gui.popups.HeatMapPopup import HeatMapPopup
from gui.popups.OscillationMapPopup import OscillationMapPopup
from gui.popups.PreAnalysisPopup import PreAnalysisPopup
from gui.popups.ResidueEvolution import ResidueEvolutionPopup
from gui.popups.ScatterFlowerPlotPopup import ScatterFlowerPlotPopup
from gui.popups.ScatterPlotPopup import ScatterPlotPopup
from gui.popups.SeriesPlotPopup import SeriesPlotPopup
from gui.popups.VerticalBar import VerticalBarPopup

class Parassign(QWidget):
    def __init__(self, parent=None, gui_settings=None, variables=None):
        QWidget.__init__(self, parent=parent)
