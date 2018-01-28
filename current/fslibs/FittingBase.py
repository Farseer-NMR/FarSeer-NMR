from abc import ABCMeta, abstractmethod


class FittingBase(metaclass=ABCMeta):

    @abstractmethod
    def equation(self, *args):
        pass

    @abstractmethod
    def log_okay(self, *args):
        pass

    @abstractmethod
    def results(self, *args):
        pass

    @abstractmethod
    def txt_plot(self, *args):
        pass

    @abstractmethod
    def results_header(self):
        pass

    @abstractmethod
    def fit_log_header(self, col):
        pass

    # FITTING LOG FILE FAILED:
    def fit_failed(self, res, x, y):
        s2w = \
            """
            ResNo:  {}
            xdata: {}
            ydata: {}
            !¡FIT FAILED TO FIND MINIMIZATION!¡
            **************************
            """. \
                format(res, list(x), list(y))

        return s2w

    # NOT ENOUGH DATA
    def not_enough_data(self, res, x, y):
        s2w = \
            """
            ResNo:  {}
            xdata: {}
            ydata: {}
            !¡NOT ENOUGH DATA POINTS - FIT NOT PERFORMED!¡
            **************************
            """. \
                format(res, list(x), list(y))

        return s2w

    @abstractmethod
    def fit_data(self, *args):
        pass

