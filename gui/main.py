import sys
from multiprocessing.pool import ThreadPool
from collections import namedtuple
from time import sleep

from ca import visualisation, grain_field
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.components import LabelLineEdit, InclusionWidget, GrainFieldSetterWidget, separator, ResolutionWidget
from gui.utils import add_widgets_to_layout
from files import export_text, export_image, import_text


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MSM proj')

        # initial grain field
        default_x, default_y = 100, 100
        self.grain_field = grain_field.GrainField(default_x, default_y)

        self.init_menubar()
        self.init_status_bar()
        self.init_center()

        self.setFixedSize(self.sizeHint())
        self.setFixedWidth(300)

        self.update_layout()

        self.show()

    def init_menubar(self):
        # setup top menu
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        microstructure_menu = filemenu.addMenu('&Microstructure')

        # setup import and export actions
        import_action = QtWidgets.QAction("&Import", self)
        import_action.triggered.connect(self.import_field)

        export_action = QtWidgets.QAction('&Export', self)
        export_action.triggered.connect(self.export_field)
        export_image_action = QtWidgets.QAction('E&xport Image', self)
        export_image_action.triggered.connect(self.export_field_image)

        microstructure_menu.addAction(import_action)
        microstructure_menu.addAction(export_action)
        microstructure_menu.addAction(export_image_action)

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
        self.grain_field_widget = GrainFieldSetterWidget(central_wrapper)
        self.inclusion_widget = InclusionWidget(central_wrapper)
        self.resolution_picker = ResolutionWidget(central_wrapper)
        # layout
        v_box = QtWidgets.QVBoxLayout(central_wrapper)
        v_box_items = []
        # setup input fields
        self.set_default_values()

        # buttons
        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.clicked.connect(self.run_visualisation)
        self.inclusion_widget.button.clicked.connect(self.add_inclusions)
        v_box_items.extend([
            self.grain_field_widget,
            separator(central_wrapper),
            self.inclusion_widget,
            separator(central_wrapper),
            self.resolution_picker,
            separator(central_wrapper),
            self.start_button
        ])
        add_widgets_to_layout(v_box, v_box_items)
        central_wrapper.setLayout(v_box)
        self.setCentralWidget(central_wrapper)

    def get_values(self):
        """
        Get values from GUI fields

        :return: namedtuple with: width, height, nucleon_amount, resolution
        """
        Values = namedtuple('FieldValues', ['width', 'height', 'nucleon_amount', 'resolution', 'probability',
                                            'inclusion_type', 'inclusion_amount', 'inclusion_size'])
        return Values(
            width=self.grain_field_widget.x_input.value,
            height=self.grain_field_widget.y_input.value,
            nucleon_amount=self.grain_field_widget.nucleon_amount.value,
            probability=self.grain_field_widget.probability.value,
            inclusion_type=self.inclusion_widget.inclusion_type.value,
            inclusion_amount=self.inclusion_widget.inclusion_amount.value,
            inclusion_size=self.inclusion_widget.inclusion_size.value,
            resolution=self.resolution_picker.resolution_input.value
        )

    def import_field(self):
        """
        Import grain field from file
        """
        src = QtWidgets.QFileDialog().getOpenFileName(self, 'Import field', filter='*.txt')[0]
        if src:
            self.grain_field = import_text(src)
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

    def run_visualisation(self):
        self.centralWidget().setEnabled(False)
        sleep(0.5)
        try:
            values = self.get_values()
            pool = ThreadPool(processes=1)
            # if field is empty start analysis on random field, else continue analyzing current field
            async_result = pool.apply_async(func=visualisation.run, kwds={
                'x_size': values.width,
                'y_size': values.height,
                'num_of_grains': values.nucleon_amount,
                'probability': values.probability,
                'resolution': values.resolution,
                'num_of_inclusions': values.inclusion_amount,
                'type_of_inclusions': values.inclusion_type,
                'inclusions_size': values.inclusion_size
            }) if not self.grain_field else pool.apply_async(func=visualisation.run_field, args=(
                self.grain_field, values.resolution
            ))
            res = async_result.get()
            print(res)
            self.grain_field = res
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
        self.grain_field_widget.nucleon_amount.value = 100
        self.grain_field_widget.probability.value = 50

        # inclusions
        self.inclusion_widget.inclusion_size.value = 1

        # resolution
        self.resolution_picker.resolution_input.value = 6


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
