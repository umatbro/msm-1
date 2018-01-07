from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget, QHBoxLayout, QComboBox, QSpinBox, QPushButton, QSlider, \
    QRadioButton
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIntValidator
from gui.utils import add_widgets_to_layout
from enum import auto
from ca.grain_field import CA_METHOD, MC_METHOD, EnergyDistribution, NucleationModule


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


class ComboBoxButton(QWidget):
    def __init__(self, button_caption='', options=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if options is None:
            options = []
        self.combo_box = QComboBox(self)
        self.button = QPushButton(self)

        self.button.setText(button_caption)
        self.combo_box.addItems(options)

        h_box = QHBoxLayout(self)
        h_box.addWidget(self.combo_box)
        h_box.addWidget(self.button)
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
        # layout
        v_box = QtWidgets.QVBoxLayout(self)
        # setup input fields
        self.text = QLabel('Default text')
        self.text.setAlignment(Qt.AlignHCenter)
        self.simulation_type = LabelComboBox(self, 'Simulation', [CA_METHOD, MC_METHOD])
        self.x_input = LabelSpinBox(self, 'Width: ')
        self.y_input = LabelSpinBox(self, 'Height: ')
        self.nucleon_amount = LabelSpinBox(self, 'Nucleon amount: ', 10000)
        self.max_iterations = LabelSpinBox(self, 'Iterations', 10000, 0)

        self.x_input.spin_box.setSingleStep(100)
        self.y_input.spin_box.setSingleStep(100)
        self.max_iterations.spin_box.setSingleStep(5)

        add_widgets_to_layout(v_box, [
            self.text,
            self.simulation_type,
            self.x_input, self.y_input, self.nucleon_amount,
            self.max_iterations,
        ])
        self.setLayout(v_box)

    def setEnabled(self, setting: bool):
        # self.text.setEnabled(setting)
        self.x_input.setEnabled(setting)
        self.y_input.setEnabled(setting)
        self.nucleon_amount.setEnabled(setting)


class ResolutionWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolution_input = LabelSpinBox(self, 'Resolution: ', 30, 1)
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


class ProbabilityWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(90)
        self.l1 = QLabel('Probability')
        self.label = QLabel('0%')
        self.probability = QSlider(Qt.Vertical)
        self.probability.setMinimum(0)
        self.probability.setMaximum(100)
        self.probability.setTickInterval(10)
        self.probability.setTickPosition(QSlider.TicksRight)
        self.probability.valueChanged.connect(lambda: self.label.setText('{}%'.format(self.probability.value())))
        v_box = QtWidgets.QVBoxLayout(self)
        v_box.addWidget(self.l1)
        v_box.addWidget(self.label)
        v_box.addWidget(self.probability)
        self.setLayout(v_box)
        self.setToolTip('Probability')

    @property
    def value(self):
        return self.probability.value()

    @value.setter
    def value(self, val):
        self.probability.setValue(val)


class BoundaryWidget(QWidget):
    ALL = auto()
    SELECTED = auto()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = QLabel('Boundaries')
        self.all_boundaries_radio = QRadioButton('all')
        self.all_boundaries_radio.setChecked(True)
        self.selected_boundaries_radio = QRadioButton('selected grains')

        v_box = QtWidgets.QVBoxLayout(self)
        v_box.addWidget(self.label)
        v_box.addWidget(self.all_boundaries_radio)
        v_box.addWidget(self.selected_boundaries_radio)
        self.setLayout(v_box)

    @property
    def value(self):
        if self.all_boundaries_radio.isChecked():
            return BoundaryWidget.ALL
        elif self.selected_boundaries_radio.isChecked():
            return BoundaryWidget.SELECTED
        else:
            return None


class EnergyWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = QLabel('Energy distribution')
        self.energy_distribution = ComboBoxButton('Distribute energy', [
            distribution_type.value for distribution_type in EnergyDistribution.__members__.values()
        ], self)
        # disable energy on edges when heterogeneous option is selected
        self.energy_distribution.combo_box.activated[str].connect(lambda selected: self.energy_on_edges.setEnabled(
            selected == EnergyDistribution.HETEROGENOUS.value
        ))
        self.energy_inside = LabelSpinBox(self, 'Energy inside', 15)
        self.energy_on_edges = LabelSpinBox(self, 'Energy on edges', 15)
        self.nucleons_on_start = LabelSpinBox(self, 'Nucleons on start', 100)
        self.nucleation_module = LabelComboBox(
            self, 'Nucleation module',
            options=[val.value for val in NucleationModule.__members__.values()]
        )
        self.nucleons_to_add = LabelSpinBox(self, 'Nucleons to add', 100)
        self.after_iterations = LabelSpinBox(self, 'After how many iterations?', 50)
        self.run_recrystalization_button = QPushButton('srxmc')

        # layout
        v_box = QtWidgets.QVBoxLayout(self)
        v_box.addWidget(self.label)
        v_box.addWidget(self.energy_distribution)
        v_box.addWidget(self.energy_inside)
        v_box.addWidget(self.energy_on_edges)
        v_box.addWidget(self.nucleons_on_start)
        v_box.addWidget(self.nucleation_module)
        v_box.addWidget(self.nucleons_to_add)
        v_box.addWidget(self.after_iterations)
        v_box.addStretch()
        v_box.addWidget(self.run_recrystalization_button)
        self.setLayout(v_box)


def separator(parent):
    frame = QtWidgets.QFrame(parent)
    frame.setGeometry(QtCore.QRect(0, 0, parent.width(), 1))
    frame.setFrameShape(QtWidgets.QFrame.HLine)
    frame.setFrameShadow(QtWidgets.QFrame.Sunken)

    return frame
