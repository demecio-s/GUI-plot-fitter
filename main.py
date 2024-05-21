
from PySide6.QtWidgets import QApplication, QLabel
from widgets import OpenFile, MainWindow
from modelfuncs import miscellaneous
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from plot import Plot
import sys


def analyze(mainWindow: MainWindow):
    try:
        depData, depUncertainty, indepData, indepUncertainty, dimension = miscellaneous.parse(mainWindow.file)
    except AttributeError:
        popUpErr = QLabel('Make sure to select a file and model curve first!')
        popUpErr.show()

    try:
        modelFunc, parameterNames = mainWindow.check_radio()
    except TypeError:
        popUpErr = QLabel('Make sure to choose a model curve!')
        popUpErr.show()

    bestPar, bestParUncertainties = miscellaneous.best_fit(modelFunc,
                                                           indepData,
                                                           depData,
                                                           depUncertainty)

    plot = Plot([indepData, indepUncertainty],
                [depData, depUncertainty],
                modelFunc,
                bestPar,
                dimension)
    plot.plot()

    # MAKE FUNCTION TO DIPLAY BESTFITPAR
    graph = QPixmap('plot.png')
    graph = graph.scaled(QSize(400, 400),
                         Qt.KeepAspectRatioByExpanding,
                         Qt.SmoothTransformation)
    mainWindow.figure.setPixmap(graph)

    mainWindow.set_text(bestPar, bestParUncertainties, parameterNames)


# Example
if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    fileDialog = OpenFile()

    # open file on toolbar allows to choose file you want to read and shows it
    mainWindow.openFile.clicked.connect(
        lambda: mainWindow.show_file(
            fileDialog.file_dialog(), mainWindow.dataEdit))

    # analyze button should produce best fit params and plot
    mainWindow.analyzeButton.pressed.connect(
        lambda: analyze(mainWindow))

    mainWindow.show()
    app.exec()
