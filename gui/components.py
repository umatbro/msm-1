from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget, QHBoxLayout, QComboBox, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator


class LabelLineEdit(QWidget):
    """
    Horizontal HBox with label and Line edit to the right
    """
    def __init__(self, parent, label='text', line_edit_placeholder=''):
        super().__init__(parent)
        self.label = QLabel(label, parent)
        self.line_edit = QLineEdit(parent)
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


class LabelComboBox(QWidget):
    def __init__(self, parent, label='', options=None):
        if options is None:
            options = ['Circle', 'Square']
        if options is None:
            options = []
        super().__init__(parent)
        self.label = QLabel(label, parent)
        self.combo_box = QComboBox(parent)
        self.combo_box.addItems(options)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setAlignment(Qt.AlignVCenter)

        h_box = QHBoxLayout(self)
        h_box.addWidget(self.label, 1)
        h_box.addWidget(self.combo_box, 4)
        self.setLayout(h_box)


class LabelSpinBox(QWidget):
    def __init__(self, parent, label='', max=1000, min=0):
        super().__init__(parent)
        self.label = QLabel(label, parent)
        self.spin_box = QSpinBox(parent)
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
