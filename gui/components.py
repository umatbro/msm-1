from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget, QHBoxLayout, QComboBox, QSpinBox, QPushButton
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIntValidator
from gui.utils import add_widgets_to_layout


class LabelLineEdit(QWidget):
    """
    Horizontal HBox with label and Line edit to the right
    """
    def __init__(self, parent, label='text', line_edit_placeholder=''):
        super().__init__(parent)
        self.label = QLabel(label, self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText(line_edit_placeholder)
        self.line_edit.setValidator(QIntValidator())
        h_box = QHBoxLayout(self)
        h_box.addWidget(self.label, 1)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setAlignment(Qt.AlignVCenter)
        h_box.addWidget(self.line_edit, 4)
        self.setLayout(h_box)

    @property
    def value(self):
        return int(self.line_edit.text())

    @value.setter
    def value(self, value):
        self.line_edit.setText(value)


class LabelComboBox(QWidget):
    def __init__(self, parent, label='', options=None):
        if options is None:
            options = ['Circle', 'Square']
        if options is None:
            options = []
        super().__init__(parent)
        self.label = QLabel(label, self)
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(options)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setAlignment(Qt.AlignVCenter)

        h_box = QHBoxLayout(self)
        h_box.addWidget(self.label, 1)
        h_box.addWidget(self.combo_box, 4)
        self.setLayout(h_box)

    @property
    def value(self):
        return self.combo_box.currentText()


class LabelSpinBox(QWidget):
    def __init__(self, parent, label='', max=1000, min=0):
        super().__init__(parent)
        self.label = QLabel(label, self)
        self.spin_box = QSpinBox(self)
        self.spin_box.setMaximum(max)
        self.spin_box.setMinimum(min)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setAlignment(Qt.AlignVCenter)

        h_box = QHBoxLayout(self)
        h_box.addWidget(self.label, 1)
        h_box.addWidget(self.spin_box, 4)
        self.setLayout(h_box)

    @property
    def value(self):
        return self.spin_box.value()

    @value.setter
    def value(self, val):
        self.spin_box.setValue(val)


class GrainFieldSetterWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # main_widget = QWidget(parent)
        # layout
        v_box = QtWidgets.QVBoxLayout(self)
        # setup input fields
        self.text = QLabel('Default text')
        self.text.setAlignment(Qt.AlignHCenter)
        self.x_input = LabelSpinBox(self, 'Width: ')
        self.y_input = LabelSpinBox(self, 'Height: ')
        self.nucleon_amount = LabelSpinBox(self, 'Nucleon amount: ', 10000)

        self.x_input.spin_box.setSingleStep(100)
        self.y_input.spin_box.setSingleStep(100)

        add_widgets_to_layout(v_box, [
            self.text,
            self.x_input, self.y_input, self.nucleon_amount,
        ])
        self.setLayout(v_box)


class ResolutionWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.resolution_input = LabelSpinBox(self, 'Resolution: ', 100, 1)
        self.setToolTip('Length of squares sides (in pixels)')
        self.title = QLabel('Display options')

        v_box = QtWidgets.QVBoxLayout(self)
        v_box.addWidget(self.title)
        v_box.addWidget(self.resolution_input)
        self.setLayout(v_box)


class InclusionWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.inclusion_type = LabelComboBox(self, 'Inclusion type', ['Square', 'Circle'])
        self.inclusion_amount = LabelSpinBox(self, 'Amount of inclusions')
        self.inclusion_size = LabelSpinBox(self, 'Size: ', 100, 1)
        self.button = QPushButton('Add inclusions')

        v_box = QtWidgets.QVBoxLayout(self)
        add_widgets_to_layout(v_box, [
            self.inclusion_type, self.inclusion_amount, self.inclusion_size, self.button
        ])
        self.setLayout(v_box)


def separator(parent):
    frame = QtWidgets.QFrame(parent)
    frame.setGeometry(QtCore.QRect(0, 0, parent.width(), 1))
    frame.setFrameShape(QtWidgets.QFrame.HLine)
    frame.setFrameShadow(QtWidgets.QFrame.Sunken)

    return frame
