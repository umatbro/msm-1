import sys
from multiprocessing.pool import ThreadPool
from time import sleep
from ca import visualisation, grain_field
from PyQt5 import QtCore, QtGui, QtWidgets


def add_widgets_to_layout(layout, widgets):
    for widget in widgets:
        layout.addWidget(widget)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # initial grain field
        default_x, default_y = 100, 100
        self.grain_field = grain_field.GrainField(default_x, default_y, 6)

        self.init_menubar()
        self.init_status_bar()
        self.init_center()

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

    def init_status_bar(self):
        self.statusBar()
        self.setWindowTitle('MSM proj')
        self.update_status_bar()

    def update_status_bar(self):
        self.statusBar().showMessage(str(self.grain_field))

    def init_center(self):
        # layout
        v_box = QtWidgets.QVBoxLayout()
        v_box_items = []
        # setup input fields
        self.x_input = QtWidgets.QLineEdit()
        self.x_input.setPlaceholderText('width')
        self.y_input = QtWidgets.QLineEdit()
        self.y_input.setPlaceholderText('height')
        self.num_of_grains_input = QtWidgets.QLineEdit()
        self.num_of_grains_input.setPlaceholderText('Number of grains')
        self.resolution_input = QtWidgets.QLineEdit()
        self.resolution_input.setPlaceholderText('resolution')

        # buttons
        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.clicked.connect(self.run_visualisation)

        v_box_items.extend([
            self.x_input, self.y_input, self.num_of_grains_input, self.resolution_input,
            self.start_button
        ])
        add_widgets_to_layout(v_box, v_box_items)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(v_box)
        self.setCentralWidget(central_widget)

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
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(func=visualisation.run, kwds={
                'x_size': int(self.x_input.text()),
                'y_size': int(self.y_input.text()),
                'num_of_grains': int(self.num_of_grains_input.text()),
                'resolution': int(self.resolution_input.text())
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
        # self.setEnabled(True)


app = QtWidgets.QApplication(sys.argv)
win = MainWindow()
sys.exit(app.exec_())
