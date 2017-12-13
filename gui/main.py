import sys
from multiprocessing.pool import ThreadPool
from collections import namedtuple
from time import sleep

from ca import visualisation, grain_field
from PyQt5 import QtCore, QtGui, QtWidgets

from ca.grain import Grain
from ca.grain_field import GrainField
from gui.components import InclusionWidget, GrainFieldSetterWidget, separator, ResolutionWidget, ProbabilityWidget, \
    BoundaryWidget, CA_METHOD, MC_METHOD
from gui.utils import add_widgets_to_layout
from files import export_text, export_image, import_text, import_img


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MSM proj')

        # initial grain field
        self.grain_field = grain_field.GrainField(100, 100)
        self.selected_cells = {}

        self.init_menubar()
        self.init_status_bar()
        self.init_center()

        self.setFixedSize(self.sizeHint())
        self.setFixedWidth(400)

        self.update_layout()

        self.show()

    def init_menubar(self):
        # setup top menu
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        microstructure_menu = filemenu.addMenu('&Microstructure')

        # setup import and export actions
        import_action = QtWidgets.QAction("Impor&t", self)
        import_action.triggered.connect(self.import_field)
        import_img_action = QtWidgets.QAction('Import &image', self)
        import_img_action.triggered.connect(self.import_field_image)

        export_action = QtWidgets.QAction('&Export', self)
        export_action.triggered.connect(self.export_field)
        export_image_action = QtWidgets.QAction('E&xport Image', self)
        export_image_action.triggered.connect(self.export_field_image)

        microstructure_menu.addAction(export_action)
        microstructure_menu.addAction(import_action)
        microstructure_menu.addAction(export_image_action)
        microstructure_menu.addAction(import_img_action)

        # reset action
        reset_action = QtWidgets.QAction('&Reset', self)
        reset_action.setShortcut('Ctrl+R')
        reset_action.setStatusTip('Clear current grain field')
        reset_action.triggered.connect(self.reset_field)
        filemenu.addAction(reset_action)

        # quitting program
        exit_action = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        filemenu.addAction(exit_action)

    def init_status_bar(self):
        self.statusBar()
        self.update_status_bar()

    def update_status_bar(self):
        self.statusBar().showMessage(str(self.grain_field))

    def init_center(self):
        central_wrapper = QtWidgets.QWidget()

        # left pane
        left_pane = QtWidgets.QWidget(central_wrapper)
        self.grain_field_widget = GrainFieldSetterWidget(left_pane)
        self.inclusion_widget = InclusionWidget(left_pane)
        self.resolution_picker = ResolutionWidget(left_pane)
        # layout
        v_box = QtWidgets.QVBoxLayout(left_pane)
        v_box_items = []

        # buttons
        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.clicked.connect(self.run_visualisation)
        self.inclusion_widget.button.clicked.connect(self.add_inclusions)
        v_box_items.extend([
            self.grain_field_widget,
            separator(left_pane),
            self.inclusion_widget,
            separator(left_pane),
            self.resolution_picker,
            separator(left_pane),
            self.start_button
        ])
        add_widgets_to_layout(v_box, v_box_items)
        left_pane.setLayout(v_box)

        # right pane
        right_pane = QtWidgets.QWidget(central_wrapper)
        self.probability = ProbabilityWidget(right_pane)
        self.boundaries = BoundaryWidget(right_pane)
        self.boundaries_button = QtWidgets.QPushButton('Add boundaries')
        self.boundaries_button.clicked.connect(self.add_boundaries)
        self.n_label = QtWidgets.QLabel('New number\nof nuclei')
        self.new_num_of_nuclei_spinbox = QtWidgets.QSpinBox(right_pane)
        self.new_num_of_nuclei_spinbox.setRange(0, 10000)
        self.new_num_of_nuclei_spinbox.setSingleStep(10)
        self.clear_button = QtWidgets.QPushButton('Clear and run')
        self.clear_button.clicked.connect(self.ca_visualisation)
        self.dp_checkbox = QtWidgets.QCheckBox('Dual phase', right_pane)
        v_box_r = QtWidgets.QVBoxLayout(right_pane)
        v_box_r.addWidget(self.probability)
        v_box_r.addWidget(self.boundaries)
        v_box_r.addWidget(self.boundaries_button)
        v_box_r.addWidget(separator(right_pane))
        v_box_r.addWidget(self.n_label)
        v_box_r.addWidget(self.new_num_of_nuclei_spinbox)
        v_box_r.addWidget(self.dp_checkbox)
        v_box_r.addWidget(self.clear_button)

        h_box = QtWidgets.QHBoxLayout(central_wrapper)
        h_box.addWidget(left_pane)
        h_box.addWidget(right_pane)
        self.setCentralWidget(central_wrapper)

        # setup input fields
        self.set_default_values()

    def get_values(self):
        """
        Get values from GUI fields

        :return: namedtuple with: width, height, nucleon_amount, resolution
        """
        Values = namedtuple('FieldValues', ['width', 'height', 'nucleon_amount', 'resolution', 'probability',
                                            'inclusion_type', 'inclusion_amount', 'inclusion_size', 'dual_phase',
                                            'new_amount_of_nuclei', 'boundaries', 'max_iterations', 'simulation_method'])
        return Values(
            width=self.grain_field_widget.x_input.value,
            height=self.grain_field_widget.y_input.value,
            nucleon_amount=self.grain_field_widget.nucleon_amount.value,
            probability=self.probability.value,
            inclusion_type=self.inclusion_widget.inclusion_type.value,
            inclusion_amount=self.inclusion_widget.inclusion_amount.value,
            inclusion_size=self.inclusion_widget.inclusion_size.value,
            resolution=self.resolution_picker.resolution_input.value,
            dual_phase=self.dp_checkbox.isChecked(),
            new_amount_of_nuclei=self.new_num_of_nuclei_spinbox.value(),
            boundaries=self.boundaries.value,
            max_iterations=self.grain_field_widget.max_iterations.value,
            simulation_method=self.grain_field_widget.simulation_type.value,
        )

    def import_field(self):
        """
        Import grain field from file
        """
        src = QtWidgets.QFileDialog().getOpenFileName(self, 'Import field', filter='*.txt')[0]
        if src:
            self.grain_field = import_text(src)
        self.update_layout()

    def import_field_image(self):
        src = QtWidgets.QFileDialog().getOpenFileName(self, 'Import image', filter='*.png')[0]
        if src:
            self.grain_field = import_img(src)
        self.update_layout()

    def export_field(self):
        print('Export')
        file_dialog = QtWidgets.QFileDialog()
        filename, extension = file_dialog.getSaveFileName(self, 'Export ', filter='*.txt')

        if filename:
            export_text(self.grain_field, filename)

        print(filename)

    def export_field_image(self):
        file_dialog = QtWidgets.QFileDialog()
        filename, extension = file_dialog.getSaveFileName(self, 'Export ', filter='*.png')

        if filename:
            export_image(self.grain_field, filename)

        print(filename)

    def reset_field(self):
        self.set_default_values()
        values = self.get_values()
        self.grain_field = grain_field.GrainField(values.width, values.height)
        self.update_layout()

    def add_inclusions(self):
        values = self.get_values()
        self.grain_field.random_inclusions(
            num_of_inclusions=values.inclusion_amount,
            inclusion_size=values.inclusion_size,
            inclusion_type=values.inclusion_type
        )
        self.statusBar().showMessage('Added {} inclusions'.format(values.inclusion_amount))

    def add_boundaries(self):
        values = self.get_values()
        points = []
        if values.boundaries is BoundaryWidget.ALL:
            points = self.grain_field.grains_boundaries_points
        elif values.boundaries is BoundaryWidget.SELECTED:
            for state, cells in self.selected_cells.items():
                points.extend(self.grain_field.cells_of_state_boundary_points(state))
                # unlock selected cells
                for cell in cells:
                    cell.lock_status = Grain.ALIVE

        for point in points:
            self.grain_field[point].state = Grain.INCLUSION

        # also set status bar message
        self.statusBar().showMessage('Added boundary points. ({}% of total)'
                                     .format(100 * self.grain_field.grain_boundary_percentage))

    def run_visualisation(self):
        self.centralWidget().setEnabled(False)
        sleep(0.5)
        try:
            values = self.get_values()
            self.hide()
            pool = ThreadPool(processes=1)

            if not self.grain_field:  # empty field - create new field
                self.grain_field = GrainField(values.width, values.height)
                self.grain_field.random_inclusions(values.inclusion_amount, values.inclusion_size,
                                                   values.inclusion_type)
                if values.simulation_method == CA_METHOD:
                    self.grain_field.random_grains(values.nucleon_amount)
                elif values.simulation_method == MC_METHOD:
                    self.grain_field.fill_field_with_random_cells(values.nucleon_amount)

            async_result = pool.apply_async(func=visualisation.run_field, kwds={
                'grain_field': self.grain_field,
                'resolution': values.resolution,
                'probability': values.probability,
                'iterations_limit': values.max_iterations,
                'simulation_method': values.simulation_method,
            })

            self.grain_field, self.selected_cells = async_result.get()
            print(self.grain_field)
            self.show()
            self.update_layout()
            self.update_status_bar()
        except ValueError as e:
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle('Error')
            layout = QtWidgets.QVBoxLayout(dialog)
            label = QtWidgets.QLabel(str(e))
            layout.addWidget(label)
            dialog.exec_()

        self.centralWidget().setEnabled(True)

    def ca_visualisation(self):
        """
        Clear all grains that are not selected.
        Then, generate random seeds again (take values from input fields)
        """
        values = self.get_values()
        self.grain_field.clear_field(dual_phase=values.dual_phase)
        if values.simulation_method == CA_METHOD:
            self.grain_field.random_grains(values.new_amount_of_nuclei)
        elif values.simulation_method == MC_METHOD:
            self.grain_field.fill_field_with_random_cells(values.new_amount_of_nuclei)
        self.run_visualisation()

    def update_layout(self):
        if self.grain_field:
            wdg = self.grain_field_widget
            wdg.text.setText(str(self.grain_field))
            wdg.x_input.value = self.grain_field.width
            wdg.y_input.value = self.grain_field.height
            wdg.nucleon_amount.value = 0

        self.grain_field_widget.setEnabled(not self.grain_field)
        self.grain_field_widget.text.setText(str(self.grain_field))

    def set_default_values(self):
        """
        Set default fields values
        """
        # grain field widget
        self.grain_field_widget.x_input.value = 100
        self.grain_field_widget.y_input.value = 100
        self.probability.value = 50
        self.grain_field_widget.nucleon_amount.value = 10
        self.grain_field_widget.max_iterations.value = 0

        # inclusions
        self.inclusion_widget.inclusion_size.value = 1

        # resolution
        self.resolution_picker.resolution_input.value = 6


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
