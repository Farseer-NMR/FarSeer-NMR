from functools import partial

from PyQt5 import QtCore

from PyQt5.QtWidgets import QDoubleSpinBox, QGridLayout, QGroupBox, QLabel, QPushButton

from gui.components.BaseWidget import BaseWidget

class Paraset(BaseWidget):
    def __init__(self, parent=None, gui_settings=None, variables=None, footer=None):

        BaseWidget.__init__(self, parent=parent, gui_settings=gui_settings, variables=variables, footer=footer)


        pcs_datasets = ['pcs_Yb_133137', 'pcs_Tb_6973', 'pre_Tm_195199', 'pcs_Yb_195199']
        rdc_datasets = ['rdc_Yb_133137', 'rdc_Tb_6973', 'rdc_Tm_195199', 'rdc_Yb_195199']
        pre_datasets = ['pre_Gd_133137', 'pre_Gd_6973', 'pre_Gd_195199']


        self.setLayout(QGridLayout())
        self.layout().addWidget(PcsWidget(self, pcs_datasets), 0, 0)
        self.layout().addWidget(RdcWidget(self, rdc_datasets), 1, 0)
        self.layout().addWidget(PreWidget(self, pre_datasets), 2, 0)
        self.layout().addWidget(self.tab_footer, 3, 0)






class PcsWidget(QGroupBox):

    def __init__(self, parent=None, datasets=None):

        QGroupBox.__init__(self, parent)
        self.setLayout(QGridLayout(self))

        self.layout().setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignTop)

        self.pcs_widgets = []

        self.setTitle("Pseudocontact Shift Analysis")


        data_set_label = QLabel('Dataset', self)
        Xax_label = QLabel('Χ<sub>ax</sub> ( 10<sup>-32</sup>m<sup>3</sup>)', self)
        Xrh_label = QLabel('Χ<sub>rh</sub> ( 10<sup>-32</sup>m<sup>3</sup>)', self)
        alpha_label = QLabel('α (<sup>o</sup>)', self)
        beta_label = QLabel('β (<sup>o</sup>)', self)
        gamma_label = QLabel('γ (<sup>o</sup>)', self)
        x_label = QLabel('x (Å)', self)
        y_label = QLabel('y (Å)', self)
        z_label = QLabel('z (Å)', self)

        labels = [data_set_label, Xax_label, Xrh_label, alpha_label, beta_label, gamma_label, x_label, y_label, z_label]

        for label in labels:
            label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.layout().addWidget(data_set_label, 0, 0)
        self.layout().addWidget(Xax_label, 0, 1)
        self.layout().addWidget(Xrh_label, 0, 2)
        self.layout().addWidget(alpha_label, 0, 3)
        self.layout().addWidget(beta_label, 0, 4)
        self.layout().addWidget(gamma_label, 0, 5)
        self.layout().addWidget(x_label, 0, 6)
        self.layout().addWidget(y_label, 0, 7)
        self.layout().addWidget(z_label, 0, 8)

        for ii, ds in enumerate(datasets):
            dataset = QLabel(ds, self)
            Xax = QDoubleSpinBox(self)
            Xrh = QDoubleSpinBox(self)
            a = QDoubleSpinBox(self)
            b = QDoubleSpinBox(self)
            g = QDoubleSpinBox(self)
            x = QDoubleSpinBox(self)
            y = QDoubleSpinBox(self)
            z = QDoubleSpinBox(self)
            more = QPushButton('More...', self)

            self.layout().addWidget(dataset, ii+1, 0)
            self.layout().addWidget(Xax, ii+1, 1)
            self.layout().addWidget(Xrh, ii+1, 2)
            self.layout().addWidget(a, ii+1, 3)
            self.layout().addWidget(b, ii+1, 4)
            self.layout().addWidget(g, ii+1, 5)
            self.layout().addWidget(x, ii+1, 6)
            self.layout().addWidget(y, ii+1, 7)
            self.layout().addWidget(z, ii+1, 8)
            self.layout().addWidget(more, ii+1, 9)

            widgets = [Xax, Xrh, a, b, g, x, y, z]
            dataset.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            [w.setAlignment(QtCore.Qt.AlignRight) for w in widgets]
            widgets.append(more)

            self.pcs_widgets.append(widgets)



class RdcWidget(QGroupBox):

    def __init__(self, parent=None, datasets=None):

        QGroupBox.__init__(self, parent)
        self.setLayout(QGridLayout(self))

        self.layout().setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignTop)

        self.setTitle("Resdiual Dipolar Coupling Analysis")



        data_set_label = QLabel('Dataset', self)
        Dax_label = QLabel('D<sub>ax</sub> (x10<sup>-32</sup>m<sup>3</sup>)', self)
        Drh_label = QLabel('D<sub>rh</sub> (x10<sup>-32</sup>m<sup>3</sup>)', self)
        alpha_label = QLabel('α (<sup>o</sup>)', self)
        beta_label = QLabel('β (<sup>o</sup>)', self)
        gamma_label = QLabel('γ (<sup>o</sup>)', self)
        B0_label = QLabel('B<sub>0</sub> (T)', self)
        T_label = QLabel('T (K)', self)
        S2_label = QLabel('S<sup>2</sup>', self)

        self.rdc_widgets = []

        labels = [data_set_label, Dax_label, Drh_label, alpha_label, beta_label, gamma_label, B0_label, T_label, S2_label]

        for label in labels:
            label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.layout().addWidget(data_set_label, 0, 0)
        self.layout().addWidget(Dax_label, 0, 1)
        self.layout().addWidget(Drh_label, 0, 2)
        self.layout().addWidget(alpha_label, 0, 3)
        self.layout().addWidget(beta_label, 0, 4)
        self.layout().addWidget(gamma_label, 0, 5)
        self.layout().addWidget(B0_label, 0, 6)
        self.layout().addWidget(T_label, 0, 7)
        self.layout().addWidget(S2_label, 0, 8)


        for ii, ds in enumerate(datasets):
            dataset = QLabel(ds, self)
            Dax = QDoubleSpinBox(self)
            Drh = QDoubleSpinBox(self)
            a = QDoubleSpinBox(self)
            b = QDoubleSpinBox(self)
            g = QDoubleSpinBox(self)
            B0 = QDoubleSpinBox(self)
            T = QDoubleSpinBox(self)
            S2 = QDoubleSpinBox(self)
            more = QPushButton('More...', self)

            self.layout().addWidget(dataset, ii+1, 0)
            self.layout().addWidget(Dax, ii+1, 1)
            self.layout().addWidget(Drh, ii+1, 2)
            self.layout().addWidget(a, ii+1, 3)
            self.layout().addWidget(b, ii+1, 4)
            self.layout().addWidget(g, ii+1, 5)
            self.layout().addWidget(B0, ii+1, 6)
            self.layout().addWidget(T, ii+1, 7)
            self.layout().addWidget(S2, ii+1, 8)
            self.layout().addWidget(more, ii+1, 9)

            widgets = [Dax, Drh, a, b, g, B0, T, S2]
            dataset.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            [w.setAlignment(QtCore.Qt.AlignRight) for w in widgets]
            widgets.append(more)

            self.rdc_widgets.append(widgets)



class PreWidget(QGroupBox):

    def __init__(self, parent=None, datasets=None):

        QGroupBox.__init__(self, parent)
        self.setLayout(QGridLayout(self))

        self.layout().setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignTop)

        self.setTitle("Paramagnetic Relaxation Enhancement Analysis")

        self.pre_widgets = []

        data_set_label = QLabel('Dataset', self)
        x_label = QLabel('x (Å)', self)
        y_label = QLabel('y (Å)', self)
        z_label = QLabel('z (Å)', self)
        inept_time_label = QLabel('Inept Time (s)')
        tauc_label = QLabel('τ<sub>c</sub> (ns)')
        B0_label = QLabel('B<sub>0</sub> (T)')
        gj_label = QLabel('g<sub>J</sub>')
        J_label = QLabel('J')
        T_label = QLabel('T (K)')

        labels = [data_set_label, x_label, y_label, z_label, inept_time_label, tauc_label, B0_label, gj_label, J_label, T_label]

        for label in labels:
            label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)



        self.layout().addWidget(data_set_label, 0, 0)
        self.layout().addWidget(x_label, 0, 1)
        self.layout().addWidget(y_label, 0, 2)
        self.layout().addWidget(z_label, 0, 3)
        self.layout().addWidget(inept_time_label, 0, 4)
        self.layout().addWidget(tauc_label, 0, 5)
        self.layout().addWidget(B0_label, 0, 6)
        self.layout().addWidget(gj_label, 0, 7)
        self.layout().addWidget(J_label, 0, 8)
        self.layout().addWidget(T_label, 0, 9)

        for ii, ds in enumerate(datasets):
            dataset = QLabel(ds, self)
            x = QDoubleSpinBox(self)
            y = QDoubleSpinBox(self)
            z = QDoubleSpinBox(self)
            inept_time = QDoubleSpinBox(self)
            tauc = QDoubleSpinBox(self)
            B0 = QDoubleSpinBox(self)
            gj = QDoubleSpinBox(self)
            J = QDoubleSpinBox(self)
            T = QDoubleSpinBox(self)
            more = QPushButton('More...', self)

            self.layout().addWidget(dataset, ii + 1, 0)
            self.layout().addWidget(x, ii + 1, 1)
            self.layout().addWidget(y, ii + 1, 2)
            self.layout().addWidget(z, ii + 1, 3)
            self.layout().addWidget(inept_time, ii + 1, 4)
            self.layout().addWidget(tauc, ii + 1, 5)
            self.layout().addWidget(B0, ii + 1, 6)
            self.layout().addWidget(gj, ii + 1, 7)
            self.layout().addWidget(J, ii + 1, 8)
            self.layout().addWidget(T, ii + 1, 9)
            self.layout().addWidget(more, ii + 1, 10)

            widgets = [x, y, z, inept_time, tauc, B0, gj, J, T]
            dataset.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            [w.setAlignment(QtCore.Qt.AlignRight) for w in widgets]
            widgets.append(more)
            self.pre_widgets.append(widgets)