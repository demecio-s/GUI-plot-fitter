from modelfuncs import ModelFunctions, miscellaneous
import matplotlib.pyplot as plt
import numpy as np


class Plot():
    def __init__(self, indepData: list, depData: list, modelFunc: ModelFunctions,
                 bestfitPar: list, graphDimension: int):
        """
        Creates a 2D or 3D figure based on the given dimension, model function,
        and data.
        """
        self.graphDimension = graphDimension
        self.fig = plt.figure()
        if graphDimension == 4:
            self.axs = self.fig.add_subplot()
            xrange = np.linspace(np.min(indepData[0]),
                                 np.max(indepData[0]), 100)
            bestFitPlot = modelFunc(xrange, *bestfitPar)
            self.axs.plot(xrange, bestFitPlot, label='Best fit')
            self.axs.errorbar(indepData[0],
                              depData[0],
                              xerr=indepData[1],
                              yerr=depData[1],
                              marker='o', linestyle='None', label='LABEL ME')
        elif graphDimension == 6:
            self.axs = self.fig.add_subplot(projection='3d')
            print(indepData[0][0])
            xrange = np.linspace(np.min(indepData[0][0]),
                                 np.max(indepData[0][0]), 100)
            yrange = np.linspace(np.min(indepData[0][1]),
                                 np.max(indepData[0][1]), 100)
            bestFitPlot = modelFunc([xrange, yrange], *bestfitPar)
            self.axs.plot(xrange, yrange,
                          bestFitPlot, label='Best fit')
            self.axs.errorbar(indepData[0][0],
                              indepData[0][1],
                              depData[0],
                              xerr=indepData[1][0],
                              yerr=indepData[1][1],
                              zerr=depData[1],
                              marker='o', linestyle='None', label='LABEL ME')

    def plot(self, xlabel: str = 'x-axis',
             ylabel: str = 'y-axis', zlabel: str = 'z-axis'):
        """
        Call to save the plot.
        """
        self.axs.set_xlabel(xlabel)
        self.axs.set_ylabel(ylabel)
        if self.graphDimension == 6:
            self.axs.set_zlabel(zlabel)
        plt.legend()
        plt.tight_layout()
        plt.savefig('plot.png')
        plt.show()

if __name__ == '__main__':
    population, popUncertainty, timeData, timeUncertainty, dimension = miscellaneous.parse('wavedata.txt')
    bestpar, bestparUncertainty = miscellaneous.best_fit(ModelFunctions.sine, timeData, population, popUncertainty)
    graph = Plot([timeData,timeUncertainty], [population,popUncertainty], ModelFunctions.sine, bestpar, dimension)
    graph.plot()
