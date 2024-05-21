import numpy as np
from scipy.optimize import curve_fit


class ModelFunctions():
    @staticmethod
    def sine(variables: list, amp: int = 1, waveNum: int = 1, phase: int = 0, offset: int = 0):
        """
        Computes the sine function for the given arguments. Can compute for
        sine wave in 2D or 3D space all multidimensional variable
        argument must be size (k,M) with k being number of independent
        variables.
        """
        multiDimCheck = len(np.shape(variables)) > 1
        if multiDimCheck:
            norms = miscellaneous.norms(variables)
            return amp * np.sin(waveNum*norms + phase) + offset
        else:
            return amp * np.sin(waveNum*variables + phase) + offset

    @staticmethod
    def population_growth(time, initialPop, rate):
        """
        Computes the population growth equation: P(1+R)^t
        """
        return initialPop * (1 + rate)**time


class miscellaneous():
    @staticmethod
    def norms(variables):
        """
        Computes norms for multidimensional data. Assumes dimensions > 4.
        """
        norms = np.zeros(len(variables[0]))
        for i in range(len(variables[0])):
            norms[i] = np.linalg.norm((variables[0][i], variables[1][i]))
        return norms

    @staticmethod
    def multi_dimension(variables):
        """
        Checks if data is 4D or 6D.
        """
        bool = False
        dimension = len(np.shape(variables))
        if dimension > 1:
            bool = True
        return bool, dimension

    # Define best fit model
    @staticmethod
    def best_fit(model: ModelFunctions, indepData: list, depData: list, uncertainty: list):
        """
        Computes the best fit parameters given the provided model and data
        using scipy.optimize.curve_fit. Returns best fit parameters and
        uncertainties.
        """
        bestpar, covariance = curve_fit(model, indepData,
                                        depData, sigma=uncertainty)
        bestparUncertainty = np.sqrt(np.diag(covariance))
        return bestpar, bestparUncertainty

    # columns should be in order of: (dependent variable, independent variable 1,
    # independent variable 2, error in depVar, error in indepvar 1,
    # error in indepvar 2)
    @staticmethod
    def parse(fileName):
        """
        Will parse the file by column and get the dimension of the data.
        Returns the parsed data and dimension. Columns should be in order
        of: (dependent variable, independent variable 1, independent
        variable 2, error in depVar, error in indepvar 1, error in indepvar 2)
        """
        file = np.genfromtxt(fileName, str)
        columns = dict()
        for column in range(len(file[0])):
            columns[f"{file[0, column]}"] = file[1:, column].astype(np.float32)
        keys = list(columns.keys())
        dimension = len(columns)
        if dimension == 4:
            depData = columns[keys[0]]
            depUncertainty = columns[keys[2]]
            indepData = columns[keys[1]]
            indepUncertainty = columns[keys[3]]
        elif dimension == 6:
            depData = columns[keys[0]]
            depUncertainty = columns[keys[3]]
            indepData = [columns[keys[1]], columns[keys[2]]]
            indepUncertainty = [columns[keys[4]], columns[keys[5]]]
        return depData, depUncertainty, indepData, indepUncertainty, dimension
