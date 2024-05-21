from PySide6.QtWidgets import (QWidget, QFileDialog, QPushButton, QGridLayout,
                               QApplication, QLabel, QMainWindow,
                               QPlainTextEdit, QToolBar, QRadioButton,
                               QHBoxLayout, QVBoxLayout)
from stylesheets import (window, analyzeButtonStyle, toolbarButton, text,
                         figureStyle, RadioStyle)
from PySide6.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(window)
        self.setWindowTitle('Best Fit Plotter 5000')

        self.toolbar = QToolBar('Toolbar')
        self.toolbar.setStyleSheet(toolbarButton)
        self.openFile = QPushButton('open file')
        self.toolbar.addWidget(self.openFile)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.figure = QLabel('Figure to appear here!')
        self.figure.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.figure.setStyleSheet(figureStyle)

        self.bestFit = QLabel('Best fit paramters will appear here!')
        self.bestFit.setStyleSheet(text)

        self.dataEdit = QPlainTextEdit('Data will appear here!')
        self.dataEdit.setReadOnly(True)
        self.dataEdit.setStyleSheet(text)

        self.analyzeButton = QPushButton("Analyze")
        self.analyzeButton.setStyleSheet(analyzeButtonStyle)

        self.sineRadio = QRadioButton('Sine Curve')
        self.populationRadio = QRadioButton('Population Curve')
        self.sineRadio.setStyleSheet(RadioStyle)
        self.populationRadio.setStyleSheet(RadioStyle)

        mainWidget = QWidget()
        mainLayout = QGridLayout(mainWidget)
        rightHalfLayout = QVBoxLayout(mainWidget)
        radioLayout = QHBoxLayout(mainWidget)

        rightHalfLayout.addWidget(self.figure)
        rightHalfLayout.addLayout(radioLayout)
        rightHalfLayout.addWidget(self.analyzeButton)
        rightHalfLayout.addWidget(self.bestFit)

        radioLayout.addWidget(self.sineRadio)
        radioLayout.addWidget(self.populationRadio)

        mainLayout.addWidget(self.dataEdit, 0, 0, 3, 1)
        mainLayout.addLayout(rightHalfLayout, 0, 1, 3, 1)

        self.setCentralWidget(mainWidget)
        self.showMaximized()

    def show_file(self, fileName, showText: QPlainTextEdit):
        self.file = fileName  # captures file name for future use
        file = open(self.file).read()
        showText.setPlainText(file)
        open(self.file).close()

    def check_radio(self):
        from modelfuncs import ModelFunctions
        sineParameterNames = ['amp', 'waveNum', 'phase', 'offset']
        popGrowthNames = ['Initial Population', 'Rate']
        if self.sineRadio.isChecked():
            return ModelFunctions.sine, sineParameterNames
        elif self.populationRadio.isChecked():
            return ModelFunctions.population_growth, popGrowthNames

    def set_text(self, bestPar, bestParUncertainties, parNames):
        lines = []
        for name in range(len(parNames)):
            lines.append(f"{parNames[name]}: {bestPar[name]}    {parNames[name]} uncertainty: {bestParUncertainties[name]}\n")
        self.bestFit.setText("".join(lines))


class OpenFile(QWidget):
    def __init__(self):
        super().__init__()

    def file_dialog(self):
        self.setWindowTitle("File Explorer")

        dialog = QFileDialog()
        dialog.setNameFilters(["*.txt *.csv"])
        dialog.selectNameFilter("*.txt *.csv")
        dialog.exec()

        fileName = dialog.selectedFiles()
        return fileName[0]


if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    fileDialog = OpenFile()
    mainWindow.show()

    app.exec()
