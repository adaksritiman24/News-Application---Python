from PyQt5.QtWidgets import QSplashScreen, QApplication
from PyQt5 import QtGui

class LoaderScreen(QSplashScreen):
    def __init__(self):
        pixmap = QtGui.QPixmap("loading.jpg")
        super().__init__(pixmap)

    def showLoading(self):
        self.show()


    def stopLoading(self):
        self.close()  