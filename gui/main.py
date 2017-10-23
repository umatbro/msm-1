import sys
from multiprocessing.pool import ThreadPool
from time import sleep
from ca import visualisation, grain_field
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.components import LabelLineEdit, LabelSpinBox
from collections import namedtuple


def add_widgets_to_layout(layout, widgets):
    for widget in widgets:
        layout.addWidget(widget)


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

        microstructure_menu.addAction(import_action)
        microstructure_menu.addAction(export_action)

        reset_action = QtWidgets.QAction('&Reset', self)
        reset_action.triggered.connect(lambda: print('xd'))
        filemenu.addAction(reset_action)

    def init_status_bar(self):
        self.statusBar()
        self.update_status_bar()

    def update_status_bar(self):
        self.statusBar().showMessage(str(self.grain_field))

    def init_center(self):
        central_widget = QtWidgets.QWidget()
        # layout
        v_box = QtWidgets.QVBoxLayout(central_widget)
        v_box_items = []
        # setup input fields
        self.x_input = LabelLineEdit(central_widget, 'Width: ')
        self.y_input = LabelLineEdit(central_widget, 'Height: ')
        self.nucleon_amount = LabelSpinBox(central_widget, 'Nucleon amount: ')
        self.resolution_input = LabelSpinBox(central_widget, 'Resolution: ', 100)
        self.resolution_input.setToolTip('Length of squares sides (in pixels)')

        frame = QtWidgets.QFrame(central_widget)
        frame.setGeometry(QtCore.QRect(0, 0, self.width(), 1))
        frame.setFrameShape(QtWidgets.QFrame.HLine)
        frame.setFrameShadow(QtWidgets.QFrame.Sunken)

        # buttons
        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.clicked.connect(self.run_visualisation)

        v_box_items.extend([
            self.x_input, self.y_input, self.nucleon_amount, self.resolution_input,
            frame, self.start_button
        ])
        add_widgets_to_layout(v_box, v_box_items)
        central_widget.setLayout(v_box)
        self.setCentralWidget(central_widget)

    def get_values(self):
        """
        Get values from GUI fields

        :return: namedtuple with: width, height, nucleon_amount, resolution
        """
        Values = namedtuple('Fields', ['width', 'height', 'nucleon_amount', 'resolution'])
        return Values(
            width=self.x_input.value,
            height=self.y_input.value,
            nucleon_amount=self.nucleon_amount.value,
            resolution=self.resolution_input.value
        )

    def import_field(self):  # TODO
        """
        Import grain field from file
        """
        print('Import')

    def export_field(self):  # TODO
        print('Export')

    def run_visualisation(self):
        self.centralWidget().setEnabled(False)
        sleep(0.5)
        try:
            # visualisation thread
            # vis = threading.Thread(target=visualisation.run, kwargs={
            #     'x_size': int(self.x_input.text()),
            #     'y_size': int(self.y_input.text()),
            #     'num_of_grains': int(self.num_of_grains_input.text()),
            #     'resolution': int(self.resolution_input.text())
            # })
            # vis.start()
            # print(vis.join())
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
