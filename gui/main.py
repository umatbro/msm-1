import sys
from multiprocessing.pool import ThreadPool
from collections import namedtuple
from time import sleep

from ca import visualisation, grain_field
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.components import LabelLineEdit, InclusionWidget, GrainFieldSetterWidget, separator, ResolutionWidget
from gui.utils import add_widgets_to_layout
from files import export_text, export_image


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MSM proj')

        # initial grain field
        default_x, default_y = 100, 100
        self.grain_field = grain_field.GrainField(default_x, default_y, 6)

        self.init_menubar()
        self.init_status_bar()
        self.init_center()

        self.setFixedSize(self.sizeHint())
        self.setFixedWidth(300)

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

        reset_action = QtWidgets.QAction('&Reset', self)
        reset_action.triggered.connect(lambda: print('xd'))
        filemenu.addAction(reset_action)

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

        # buttons
        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.clicked.connect(self.run_visualisation)
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
        Values = namedtuple('FieldValues', ['width', 'height', 'nucleon_amount', 'resolution'])
        return Values(
            width=self.grain_field_widget.x_input.value,
            height=self.grain_field_widget.y_input.value,
            nucleon_amount=self.grain_field_widget.nucleon_amount.value,
            resolution=self.grain_field_widget.resolution_input.value
        )

    def import_field(self):  # TODO
        """
        Import grain field from file
        """
        print('Import')

    def export_field(self):
        print('Export')
        file_dialog = QtWidgets.QFileDialog()
        filename, extension = file_dialog.getSaveFileName(self, 'Export ', filter='.txt')

        if filename:
            export_text(self.grain_field, filename + extension)

        print(filename)

    def export_field_image(self):
        file_dialog = QtWidgets.QFileDialog()
        filename, extension = file_dialog.getSaveFileName(self, 'Export ', filter='.png')

        if filename:
            export_image(self.grain_field, filename + extension)

        print(filename)

    def run_visualisation(self):
        self.centralWidget().setEnabled(False)
        sleep(0.5)
        try:
            values = self.get_values()
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(func=visualisation.run, kwds={
                'x_size': values.width,
                'y_size': values.height,
                'num_of_grains': values.nucleon_amount,
                'resolution': values.resolution
            })
            res = async_result.get()
            print(res)
            self.grain_field = res
            self.update_status_bar()
        except ValueError as e:
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle('Error')
            layout = QtWidgets.QVBoxLayout(dialog)
            label = QtWidgets.QLabel(str(e))
            layout.addWidget(label)
            dialog.exec_()

        self.centralWidget().setEnabled(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
