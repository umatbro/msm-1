import sys
from gui.main import MainWindow
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
win = MainWindow()
sys.exit(app.exec_())
