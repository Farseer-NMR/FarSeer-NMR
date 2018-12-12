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
import sys
import unittest
import json
import os
from PyQt5.QtWidgets import QApplication


from core.fslibs.Variables import Variables
from core.utils import get_default_config_path

from gui import gui_utils

from gui.components.TabWidget import TabWidget
from gui.tabs.settings import Settings

app = QApplication(sys.argv)


class Test_Case(unittest.TestCase):
    def setUp(self):
        ''' Create the popup'''
        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)
        fin.close()

        screen_resolution = app.desktop().screenGeometry()
        gui_settings, stylesheet = gui_utils.deliver_settings(
            screen_resolution)

        tabWidget = TabWidget(gui_settings)
        self.widget = Settings(tabWidget, gui_settings=gui_settings, footer=True)

        self.variable_keys = tuple(self.widget.variables.keys())

    def test_defaults(self):

        general = self.defaults["general_settings"]
        fitting = self.defaults["fitting_settings"]
        cs = self.defaults["cs_settings"]
        csp = self.defaults["csp_settings"]
        fasta = self.defaults["fasta_settings"]
        plots_f1 = self.defaults["PosF1_settings"]
        plots_f2 = self.defaults["PosF2_settings"]
        plots_height = self.defaults["Height_ratio_settings"]
        plots_volume = self.defaults["Volume_ratio_settings"]
        plotting_flags = self.defaults["plotting_flags"]

        self.assertEqual(self.widget.spectrum_path.field.text(),
                         general["spectra_path"] or os.getcwd())
        self.assertEqual(self.widget.output_path.field.text(),
                         general["output_path"] or os.getcwd())
        self.assertEqual(self.widget.has_sidechains_checkbox.isChecked(),
                         general["has_sidechains"])
        self.assertEqual(self.widget.use_sidechains_checkbox.isChecked(),
                         general["use_sidechains"])
        self.assertEqual(self.widget.figure_width.field.value(),
                         general["fig_width"])
        self.assertEqual(self.widget.figure_height.field.value(),
                         general["fig_height"])
        self.assertEqual(self.widget.figure_dpi.field.value(),
                         general["fig_dpi"])
        self.assertEqual(self.widget.figure_format.fields.currentText(),
                         general["fig_file_type"])

        self.assertEqual(self.widget.expand_missing_yy.isChecked(),
                         fitting["expand_missing_yy"])
        self.assertEqual(self.widget.expand_missing_zz.isChecked(),
                         fitting["expand_missing_zz"])
        self.assertEqual(self.widget.perform_comparisons_checkbox.isChecked(),
                         fitting["perform_comparisons"])
        self.assertEqual(self.widget.x_checkbox.isChecked(),
                         fitting["do_along_x"])
        self.assertEqual(self.widget.y_checkbox.isChecked(),
                         fitting["do_along_y"])
        self.assertEqual(self.widget.z_checkbox.isChecked(),
                         fitting["do_along_z"])

        self.assertEqual(self.widget.cs_correction.isChecked(),
                         cs["perform_cs_correction"])
        self.assertEqual(self.widget.cs_correction_res_ref.field.value(),
                         cs["cs_correction_res_ref"])

        self.assertEqual(self.widget.csp_alpha.field.value(),
                         csp["csp_res4alpha"])
        self.assertEqual(self.widget.csp_missing.fields.currentText(),
                         csp["cs_missing"])

        self.assertEqual(self.widget.fasta_start.field.value(),
                         fasta["FASTAstart"])
        self.assertEqual(self.widget.apply_fasta_checkbox.isChecked(),
                         fasta["applyFASTA"])

        self.assertEqual(self.widget.plot_F1_data.isChecked(),
                         plots_f1["calcs_PosF1_delta"])
        self.assertEqual(self.widget.plot_F1_y_label.field.text(),
                         plots_f1["yy_label_PosF1_delta"])
        self.assertEqual(self.widget.plot_F1_calccol.field.text(),
                         plots_f1["calccol_name_PosF1_delta"])
        self.assertEqual(self.widget.plot_F1_y_scale.field.value(),
                         plots_f1["yy_scale_PosF1_delta"])

        self.assertEqual(self.widget.plot_F2_data.isChecked(),
                         plots_f2["calcs_PosF2_delta"])
        self.assertEqual(self.widget.plot_F2_y_label.field.text(),
                         plots_f2["yy_label_PosF2_delta"])
        self.assertEqual(self.widget.plot_F2_calccol.field.text(),
                         plots_f2["calccol_name_PosF2_delta"])
        self.assertEqual(self.widget.plot_F2_y_scale.field.value(),
                         plots_f2["yy_scale_PosF2_delta"])

        self.assertEqual(self.widget.plot_CSP.isChecked(), csp["calcs_CSP"])
        self.assertEqual(self.widget.plot_CSP_y_label.field.text(),
                         csp["yy_label_CSP"])
        self.assertEqual(self.widget.plot_CSP_calccol.field.text(),
                         csp["calccol_name_CSP"])
        self.assertEqual(self.widget.plot_CSP_y_scale.field.value(),
                         csp["yy_scale_CSP"])

        self.assertEqual(self.widget.plot_height_ratio.isChecked(),
                         plots_height["calcs_Height_ratio"])
        self.assertEqual(self.widget.plot_height_y_label.field.text(),
                         plots_height["yy_label_Height_ratio"])
        self.assertEqual(self.widget.plot_height_calccol.field.text(),
                         plots_height["calccol_name_Height_ratio"])
        self.assertEqual(self.widget.plot_height_y_scale.field.value(),
                         plots_height["yy_scale_Height_ratio"])

        self.assertEqual(self.widget.plot_volume_ratio.isChecked(),
                         plots_volume["calcs_Volume_ratio"])
        self.assertEqual(self.widget.plot_volume_y_label.field.text(),
                         plots_volume["yy_label_Volume_ratio"])
        self.assertEqual(self.widget.plot_volume_calccol.field.text(),
                         plots_volume["calccol_name_Volume_ratio"])
        self.assertEqual(self.widget.plot_volume_y_scale.field.value(),
                         plots_volume["yy_scale_Volume_ratio"])

        self.assertEqual(self.widget.ext_bar_checkbox.isChecked(),
                         plotting_flags["do_ext_bar"])
        self.assertEqual(self.widget.comp_bar_checkbox.isChecked(),
                         plotting_flags["do_comp_bar"])
        self.assertEqual(self.widget.vert_bar_checkbox.isChecked(),
                         plotting_flags["do_vert_bar"])
        self.assertEqual(self.widget.res_evo_checkbox.isChecked(),
                         plotting_flags["do_res_evo"])
        self.assertEqual(self.widget.scatter_checkbox.isChecked(),
                         plotting_flags["do_cs_scatter"])
        self.assertEqual(self.widget.scatter_flower_checkbox.isChecked(),
                         plotting_flags["do_cs_scatter_flower"])
        self.assertEqual(self.widget.dpre_checkbox.isChecked(),
                         plotting_flags["do_DPRE_plot"])
        self.assertEqual(self.widget.heat_map_checkbox.isChecked(),
                         plotting_flags["do_heat_map"])

        self.assertEqual(self.widget.do_pre_checkbox.isChecked(),
                         self.defaults["pre_settings"]["apply_PRE_analysis"])

    def test_set_values(self):

        self.widget.spectrum_path.setText(os.path.join('path', 'to', 'spectrum', 'test'))
        self.widget.output_path.setText(os.path.join('path', 'to', 'output', 'test'))
        self.widget.has_sidechains_checkbox.setChecked(True)
        self.widget.use_sidechains_checkbox.setChecked(True)
        self.widget.figure_width.setValue(5.76)
        self.widget.figure_height.setValue(18.98)
        self.widget.figure_dpi.setValue(1200)
        self.widget.figure_format.select('ps')

        self.widget.expand_missing_yy.setChecked(True)
        self.widget.expand_missing_zz.setChecked(True)
        self.widget.perform_comparisons_checkbox.setChecked(True)
        self.widget.x_checkbox.setChecked(False)
        self.widget.y_checkbox.setChecked(True)
        self.widget.z_checkbox.setChecked(True)

        self.widget.cs_correction.setChecked(True)
        self.widget.cs_correction_res_ref.setValue(15)

        self.widget.csp_alpha.setValue(0.54)
        self.widget.csp_missing.select('zero')

        self.widget.fasta_start.setValue(81)
        self.widget.apply_fasta_checkbox.setChecked(True)

        self.widget.plot_F1_data.setChecked(True)
        self.widget.plot_F1_y_label.setText('1H')
        self.widget.plot_F1_calccol.setText('col_H')
        self.widget.plot_F1_y_scale.setValue(0.5)

        self.widget.plot_F2_data.setChecked(True)
        self.widget.plot_F2_y_label.setText('15N')
        self.widget.plot_F2_calccol.setText('col_N')
        self.widget.plot_F2_y_scale.setValue(0.8)

        self.widget.plot_CSP.setChecked(False)
        self.widget.plot_CSP_y_label.setText('CSP')
        self.widget.plot_CSP_calccol.setText('col_CSP')
        self.widget.plot_CSP_y_scale.setValue(1.6)

        self.widget.plot_height_ratio.setChecked(True)
        self.widget.plot_height_y_label.setText('Height')
        self.widget.plot_height_calccol.setText('col_Height')
        self.widget.plot_height_y_scale.setValue(3.7)

        self.widget.plot_volume_ratio.setChecked(True)
        self.widget.plot_volume_y_label.setText('Volume')
        self.widget.plot_volume_calccol.setText('col_Volume')
        self.widget.plot_volume_y_scale.setValue(1.4)

        self.widget.ext_bar_checkbox.setChecked(False)
        self.widget.comp_bar_checkbox.setChecked(True)
        self.widget.vert_bar_checkbox.setChecked(True)
        self.widget.res_evo_checkbox.setChecked(True)
        self.widget.scatter_checkbox.setChecked(True)
        self.widget.scatter_flower_checkbox.setChecked(True)
        self.widget.heat_map_checkbox.setChecked(True)
        self.widget.dpre_checkbox.setChecked(True)

        self.widget.do_pre_checkbox.setChecked(True)

        general = self.widget.variables["general_settings"]
        fitting = self.widget.variables["fitting_settings"]
        cs = self.widget.variables["cs_settings"]
        csp = self.widget.variables["csp_settings"]
        fasta = self.widget.variables["fasta_settings"]
        plots_f1 = self.widget.variables["PosF1_settings"]
        plots_f2 = self.widget.variables["PosF2_settings"]
        plots_height = self.widget.variables["Height_ratio_settings"]
        plots_volume = self.widget.variables["Volume_ratio_settings"]
        plotting_flags = self.widget.variables["plotting_flags"]

        self.assertEqual(self.widget.spectrum_path.field.text(),
                         (os.path.join('path', 'to', 'spectrum', 'test')))
        self.assertEqual(self.widget.output_path.field.text(),
                        (os.path.join('path', 'to', 'output', 'test')))
        self.assertEqual(self.widget.has_sidechains_checkbox.isChecked(), True)
        self.assertEqual(self.widget.use_sidechains_checkbox.isChecked(), True)
        self.assertEqual(self.widget.figure_width.field.value(), 5.76)
        self.assertEqual(self.widget.figure_height.field.value(), 18.98)
        self.assertEqual(self.widget.figure_dpi.field.value(), 1200)
        self.assertEqual(self.widget.figure_format.fields.currentText(), 'ps')

        self.assertEqual(self.widget.expand_missing_yy.isChecked(), True)
        self.assertEqual(self.widget.expand_missing_zz.isChecked(), True)
        self.assertEqual(self.widget.perform_comparisons_checkbox.
                         isChecked(), True)
        self.assertEqual(self.widget.x_checkbox.isChecked(), False)
        self.assertEqual(self.widget.y_checkbox.isChecked(), True)
        self.assertEqual(self.widget.z_checkbox.isChecked(), True)

        self.assertEqual(self.widget.cs_correction.isChecked(), True)
        self.assertEqual(self.widget.cs_correction_res_ref.field.value(), 15)

        self.assertEqual(self.widget.csp_alpha.field.value(), 0.54)
        self.assertEqual(self.widget.csp_missing.fields.currentText(), "zero")

        self.assertEqual(self.widget.fasta_start.field.value(), 81)
        self.assertEqual(self.widget.apply_fasta_checkbox.isChecked(), True)

        self.assertEqual(self.widget.plot_F1_data.isChecked(), True)
        self.assertEqual(self.widget.plot_F1_y_label.field.text(), '1H')
        self.assertEqual(self.widget.plot_F1_calccol.field.text(), 'col_H')
        self.assertEqual(self.widget.plot_F1_y_scale.field.value(), 0.5)

        self.assertEqual(self.widget.plot_F2_data.isChecked(), True)
        self.assertEqual(self.widget.plot_F2_y_label.field.text(), '15N')
        self.assertEqual(self.widget.plot_F2_calccol.field.text(), 'col_N')
        self.assertEqual(self.widget.plot_F2_y_scale.field.value(), 0.8)

        self.assertEqual(self.widget.plot_CSP.isChecked(), False)
        self.assertEqual(self.widget.plot_CSP_y_label.field.text(), 'CSP')
        self.assertEqual(self.widget.plot_CSP_calccol.field.text(), 'col_CSP')
        self.assertEqual(self.widget.plot_CSP_y_scale.field.value(), 1.6)

        self.assertEqual(self.widget.plot_height_ratio.isChecked(), True)
        self.assertEqual(self.widget.plot_height_y_label.field.text(),
                         'Height')
        self.assertEqual(self.widget.plot_height_calccol.field.text(),
                         'col_Height')
        self.assertEqual(self.widget.plot_height_y_scale.field.value(), 3.7)

        self.assertEqual(self.widget.plot_volume_ratio.isChecked(), True)
        self.assertEqual(self.widget.plot_volume_y_label.field.text(),
                         'Volume')
        self.assertEqual(self.widget.plot_volume_calccol.field.text(),
                         'col_Volume')
        self.assertEqual(self.widget.plot_volume_y_scale.field.value(), 1.4)

        self.assertEqual(self.widget.ext_bar_checkbox.isChecked(), False)
        self.assertEqual(self.widget.comp_bar_checkbox.isChecked(), True)
        self.assertEqual(self.widget.vert_bar_checkbox.isChecked(), True)
        self.assertEqual(self.widget.res_evo_checkbox.isChecked(), True)
        self.assertEqual(self.widget.scatter_checkbox.isChecked(), True)
        self.assertEqual(self.widget.scatter_flower_checkbox.isChecked(), True)
        self.assertEqual(self.widget.dpre_checkbox.isChecked(), True)
        self.assertEqual(self.widget.heat_map_checkbox.isChecked(), True)

        self.assertEqual(self.widget.do_pre_checkbox.isChecked(), True)


        self.widget.save_config()

        self.assertEqual(general["spectra_path"], (os.path.join('path', 'to', 'spectrum', 'test')))
        self.assertEqual(general["output_path"], (os.path.join('path', 'to', 'output', 'test')))
        self.assertEqual(general["has_sidechains"], True)
        self.assertEqual(general["use_sidechains"], True)
        self.assertEqual(general["fig_width"], 5.76)
        self.assertEqual(general["fig_height"], 18.98)
        self.assertEqual(general["fig_dpi"], 1200)
        self.assertEqual(general["fig_file_type"], 'ps')

        self.assertEqual(fitting["expand_missing_yy"], True)
        self.assertEqual(fitting["expand_missing_zz"], True)
        self.assertEqual(fitting["perform_comparisons"], True)
        self.assertEqual(fitting["do_along_x"], False)
        self.assertEqual(fitting["do_along_y"], True)
        self.assertEqual(fitting["do_along_z"], True)

        self.assertEqual(cs["perform_cs_correction"], True)
        self.assertEqual(cs["cs_correction_res_ref"], 15)

        self.assertEqual(csp["csp_res4alpha"], 0.54)
        self.assertEqual(csp["cs_missing"], "zero")

        self.assertEqual(fasta["applyFASTA"], True)
        self.assertEqual(fasta["FASTAstart"], 81)

        self.assertEqual(plots_f1["calcs_PosF1_delta"], True)
        self.assertEqual(plots_f1["yy_label_PosF1_delta"], '1H')
        self.assertEqual(plots_f1["calccol_name_PosF1_delta"], 'col_H')
        self.assertEqual(plots_f1["yy_scale_PosF1_delta"], 0.5)

        self.assertEqual(plots_f2["calcs_PosF2_delta"], True)
        self.assertEqual(plots_f2["yy_label_PosF2_delta"], '15N')
        self.assertEqual(plots_f2["calccol_name_PosF2_delta"], 'col_N')
        self.assertEqual(plots_f2["yy_scale_PosF2_delta"], 0.8)

        self.assertEqual(csp["calcs_CSP"], False)
        self.assertEqual(csp["yy_label_CSP"], 'CSP')
        self.assertEqual(csp["calccol_name_CSP"], 'col_CSP')
        self.assertEqual(csp["yy_scale_CSP"], 1.6)

        self.assertEqual(plots_height["calcs_Height_ratio"], True)
        self.assertEqual(plots_height["yy_label_Height_ratio"], 'Height')
        self.assertEqual(plots_height["calccol_name_Height_ratio"],
                            'col_Height')
        self.assertEqual(plots_height["yy_scale_Height_ratio"], 3.7)

        self.assertEqual(plots_volume["calcs_Volume_ratio"], True)
        self.assertEqual(plots_volume["yy_label_Volume_ratio"], 'Volume')
        self.assertEqual(plots_volume["calccol_name_Volume_ratio"],
                            'col_Volume')
        self.assertEqual(plots_volume["yy_scale_Volume_ratio"], 1.4)

        self.assertEqual(self.widget.ext_bar_checkbox.isChecked(),
                         plotting_flags["do_ext_bar"])
        self.assertEqual(self.widget.comp_bar_checkbox.isChecked(),
                         plotting_flags["do_comp_bar"])
        self.assertEqual(self.widget.vert_bar_checkbox.isChecked(),
                         plotting_flags["do_vert_bar"])
        self.assertEqual(self.widget.res_evo_checkbox.isChecked(),
                         plotting_flags["do_res_evo"])
        self.assertEqual(self.widget.scatter_checkbox.isChecked(),
                         plotting_flags["do_cs_scatter"])
        self.assertEqual(self.widget.scatter_flower_checkbox.isChecked(),
                         plotting_flags["do_cs_scatter_flower"])
        self.assertEqual(self.widget.dpre_checkbox.isChecked(),
                         plotting_flags["do_DPRE_plot"])
        self.assertEqual(self.widget.heat_map_checkbox.isChecked(),
                         plotting_flags["do_heat_map"])

        self.assertEqual(self.widget.do_pre_checkbox.isChecked(),
                         self.widget.variables
                         ["pre_settings"]["apply_PRE_analysis"])

    def test_values_not_set(self):

        self.widget.spectrum_path.setText((os.path.join('path', 'to', 'spectrum', 'test')))
        self.widget.output_path.setText((os.path.join('path', 'to', 'output', 'test')))
        self.widget.has_sidechains_checkbox.setChecked(True)
        self.widget.use_sidechains_checkbox.setChecked(True)
        self.widget.figure_width.setValue(5.76)
        self.widget.figure_height.setValue(18.98)
        self.widget.figure_dpi.setValue(1200)
        self.widget.figure_format.select('ps')

        self.widget.expand_missing_yy.setChecked(True)
        self.widget.expand_missing_zz.setChecked(True)
        self.widget.perform_comparisons_checkbox.setChecked(True)
        self.widget.x_checkbox.setChecked(False)
        self.widget.y_checkbox.setChecked(True)
        self.widget.z_checkbox.setChecked(True)

        self.widget.cs_correction.setChecked(True)
        self.widget.cs_correction_res_ref.setValue(15)

        self.widget.csp_alpha.setValue(0.54)
        self.widget.csp_missing.select('zero')

        self.widget.fasta_start.setValue(81)
        self.widget.apply_fasta_checkbox.setChecked(True)

        self.widget.plot_F1_data.setChecked(True)
        self.widget.plot_F1_y_label.setText('1H')
        self.widget.plot_F1_calccol.setText('col_H')
        self.widget.plot_F1_y_scale.setValue(0.5)

        self.widget.plot_F2_data.setChecked(True)
        self.widget.plot_F2_y_label.setText('15N')
        self.widget.plot_F2_calccol.setText('col_N')
        self.widget.plot_F2_y_scale.setValue(0.8)

        self.widget.plot_CSP.setChecked(False)
        self.widget.plot_CSP_y_label.setText('CSP')
        self.widget.plot_CSP_calccol.setText('col_CSP')
        self.widget.plot_CSP_y_scale.setValue(1.6)

        self.widget.plot_height_ratio.setChecked(True)
        self.widget.plot_height_y_label.setText('Height')
        self.widget.plot_height_calccol.setText('col_Height')
        self.widget.plot_height_y_scale.setValue(3.7)

        self.widget.plot_volume_ratio.setChecked(True)
        self.widget.plot_volume_y_label.setText('Volume')
        self.widget.plot_volume_calccol.setText('col_Volume')
        self.widget.plot_volume_y_scale.setValue(1.4)

        self.widget.ext_bar_checkbox.setChecked(False)
        self.widget.comp_bar_checkbox.setChecked(True)
        self.widget.vert_bar_checkbox.setChecked(True)
        self.widget.res_evo_checkbox.setChecked(True)
        self.widget.scatter_checkbox.setChecked(True)
        self.widget.scatter_flower_checkbox.setChecked(True)
        self.widget.heat_map_checkbox.setChecked(True)
        self.widget.dpre_checkbox.setChecked(True)

        self.widget.do_pre_checkbox.setChecked(True)

        general = self.widget.variables["general_settings"]
        fitting = self.widget.variables["fitting_settings"]
        cs = self.widget.variables["cs_settings"]
        csp = self.widget.variables["csp_settings"]
        fasta = self.widget.variables["fasta_settings"]
        plots_f1 = self.widget.variables["PosF1_settings"]
        plots_f2 = self.widget.variables["PosF2_settings"]
        plots_height = self.widget.variables["Height_ratio_settings"]
        plots_volume = self.widget.variables["Volume_ratio_settings"]
        plotting_flags = self.widget.variables["plotting_flags"]

        self.assertEqual(self.widget.spectrum_path.field.text(),
                         os.path.join('path', 'to', 'spectrum', 'test'))
        self.assertEqual(self.widget.output_path.field.text(),
                         os.path.join('path', 'to', 'output', 'test'))
        self.assertEqual(self.widget.has_sidechains_checkbox.isChecked(), True)
        self.assertEqual(self.widget.use_sidechains_checkbox.isChecked(), True)
        self.assertEqual(self.widget.figure_width.field.value(), 5.76)
        self.assertEqual(self.widget.figure_height.field.value(), 18.98)
        self.assertEqual(self.widget.figure_dpi.field.value(), 1200)
        self.assertEqual(self.widget.figure_format.fields.currentText(), 'ps')

        self.assertEqual(self.widget.expand_missing_yy.isChecked(), True)
        self.assertEqual(self.widget.expand_missing_zz.isChecked(), True)
        self.assertEqual(self.widget.perform_comparisons_checkbox.
                         isChecked(), True)
        self.assertEqual(self.widget.x_checkbox.isChecked(), False)
        self.assertEqual(self.widget.y_checkbox.isChecked(), True)
        self.assertEqual(self.widget.z_checkbox.isChecked(), True)

        self.assertEqual(self.widget.cs_correction.isChecked(), True)
        self.assertEqual(self.widget.cs_correction_res_ref.field.value(), 15)

        self.assertEqual(self.widget.csp_alpha.field.value(), 0.54)
        self.assertEqual(self.widget.csp_missing.fields.currentText(), "zero")

        self.assertEqual(self.widget.fasta_start.field.value(), 81)
        self.assertEqual(self.widget.apply_fasta_checkbox.isChecked(), True)

        self.assertEqual(self.widget.plot_F1_data.isChecked(), True)
        self.assertEqual(self.widget.plot_F2_data.isChecked(), True)
        self.assertEqual(self.widget.plot_CSP.isChecked(), False)
        self.assertEqual(self.widget.plot_height_ratio.isChecked(), True)
        self.assertEqual(self.widget.plot_volume_ratio.isChecked(), True)

        self.assertEqual(self.widget.plot_F1_data.isChecked(), True)
        self.assertEqual(self.widget.plot_F1_y_label.field.text(), '1H')
        self.assertEqual(self.widget.plot_F1_calccol.field.text(), 'col_H')
        self.assertEqual(self.widget.plot_F1_y_scale.field.value(), 0.5)

        self.assertEqual(self.widget.plot_F2_data.isChecked(), True)
        self.assertEqual(self.widget.plot_F2_y_label.field.text(), '15N')
        self.assertEqual(self.widget.plot_F2_calccol.field.text(), 'col_N')
        self.assertEqual(self.widget.plot_F2_y_scale.field.value(), 0.8)

        self.assertEqual(self.widget.plot_CSP.isChecked(), False)
        self.assertEqual(self.widget.plot_CSP_y_label.field.text(), 'CSP')
        self.assertEqual(self.widget.plot_CSP_calccol.field.text(), 'col_CSP')
        self.assertEqual(self.widget.plot_CSP_y_scale.field.value(), 1.6)

        self.assertEqual(self.widget.plot_height_ratio.isChecked(), True)
        self.assertEqual(self.widget.plot_height_y_label.field.text(),
                         'Height')
        self.assertEqual(self.widget.plot_height_calccol.field.text(),
                         'col_Height')
        self.assertEqual(self.widget.plot_height_y_scale.field.value(), 3.7)

        self.assertEqual(self.widget.plot_volume_ratio.isChecked(), True)
        self.assertEqual(self.widget.plot_volume_y_label.field.text(),
                         'Volume')
        self.assertEqual(self.widget.plot_volume_calccol.field.text(),
                         'col_Volume')
        self.assertEqual(self.widget.plot_volume_y_scale.field.value(), 1.4)

        self.assertEqual(self.widget.ext_bar_checkbox.isChecked(), False)
        self.assertEqual(self.widget.comp_bar_checkbox.isChecked(), True)
        self.assertEqual(self.widget.vert_bar_checkbox.isChecked(), True)
        self.assertEqual(self.widget.res_evo_checkbox.isChecked(), True)
        self.assertEqual(self.widget.scatter_checkbox.isChecked(), True)
        self.assertEqual(self.widget.scatter_flower_checkbox.isChecked(), True)
        self.assertEqual(self.widget.dpre_checkbox.isChecked(), True)
        self.assertEqual(self.widget.heat_map_checkbox.isChecked(), True)

        self.assertEqual(self.widget.do_pre_checkbox.isChecked(), True)

        self.assertNotEqual(general["spectra_path"], (os.path.join('path', 'to', 'spectrum', 'test')))
        self.assertNotEqual(general["output_path"], (os.path.join('path', 'to', 'output', 'test')))
        self.assertNotEqual(general["has_sidechains"], True)
        self.assertNotEqual(general["use_sidechains"], True)
        self.assertNotEqual(general["fig_width"], 5.76)
        self.assertNotEqual(general["fig_height"], 18.98)
        self.assertNotEqual(general["fig_dpi"], 1200)
        self.assertNotEqual(general["fig_file_type"], 'ps')

        self.assertNotEqual(fitting["expand_missing_yy"], True)
        self.assertNotEqual(fitting["expand_missing_zz"], True)
        self.assertNotEqual(fitting["perform_comparisons"], True)
        self.assertNotEqual(fitting["do_along_x"], False)
        self.assertNotEqual(fitting["do_along_y"], True)
        self.assertNotEqual(fitting["do_along_z"], True)

        self.assertNotEqual(cs["perform_cs_correction"], True)
        self.assertNotEqual(cs["cs_correction_res_ref"], 15)

        self.assertNotEqual(csp["csp_res4alpha"], 0.54)
        self.assertNotEqual(csp["cs_missing"], "zero")

        self.assertNotEqual(fasta["applyFASTA"], True)
        self.assertNotEqual(fasta["FASTAstart"], 81)

        self.assertNotEqual(plots_f1["calcs_PosF1_delta"], True)
        self.assertNotEqual(plots_f1["yy_label_PosF1_delta"], '1H')
        self.assertNotEqual(plots_f1["calccol_name_PosF1_delta"], 'col_H')
        self.assertNotEqual(plots_f1["yy_scale_PosF1_delta"], 0.5)

        self.assertNotEqual(plots_f2["calcs_PosF2_delta"], True)
        self.assertNotEqual(plots_f2["yy_label_PosF2_delta"], '15N')
        self.assertNotEqual(plots_f2["calccol_name_PosF2_delta"], 'col_N')
        self.assertNotEqual(plots_f2["yy_scale_PosF2_delta"], 0.8)

        self.assertNotEqual(csp["calcs_CSP"], False)
        self.assertNotEqual(csp["yy_label_CSP"], 'CSP')
        self.assertNotEqual(csp["calccol_name_CSP"], 'CSP_col')
        self.assertNotEqual(csp["yy_scale_CSP"], 1.6)

        self.assertNotEqual(plots_height["calcs_Height_ratio"], True)
        self.assertNotEqual(plots_height["yy_label_Height_ratio"], 'Height')
        self.assertNotEqual(plots_height["calccol_name_Height_ratio"],
                         'col_Height')
        self.assertNotEqual(plots_height["yy_scale_Height_ratio"], 3.7)

        self.assertNotEqual(plots_volume["calcs_Volume_ratio"], True)
        self.assertNotEqual(plots_volume["yy_label_Volume_ratio"], 'Volume')
        self.assertNotEqual(plots_volume["calccol_name_Volume_ratio"],
                         'col_Volume')
        self.assertNotEqual(plots_volume["yy_scale_Volume_ratio"], 1.4)

        self.assertNotEqual(self.widget.ext_bar_checkbox.isChecked(),
                         plotting_flags["do_ext_bar"])
        self.assertNotEqual(self.widget.comp_bar_checkbox.isChecked(),
                         plotting_flags["do_comp_bar"])
        self.assertNotEqual(self.widget.vert_bar_checkbox.isChecked(),
                         plotting_flags["do_vert_bar"])
        self.assertNotEqual(self.widget.res_evo_checkbox.isChecked(),
                         plotting_flags["do_res_evo"])
        self.assertNotEqual(self.widget.scatter_checkbox.isChecked(),
                         plotting_flags["do_cs_scatter"])
        self.assertNotEqual(self.widget.scatter_flower_checkbox.isChecked(),
                         plotting_flags["do_cs_scatter_flower"])
        self.assertNotEqual(self.widget.dpre_checkbox.isChecked(),
                         plotting_flags["do_DPRE_plot"])
        self.assertNotEqual(self.widget.heat_map_checkbox.isChecked(),
                         plotting_flags["do_heat_map"])

        self.assertNotEqual(self.widget.do_pre_checkbox,
                         self.widget.variables
                         ["pre_settings"]["apply_PRE_analysis"])


if __name__ == "__main__":
    unittest.main()
