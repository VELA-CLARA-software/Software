import sys, time
from PyQt4.QtCore import Qt, QTimer, QThread
from PyQt4.QtGui import *


class MovieSplashScreen(QSplashScreen,QThread):

    def __init__(self, movie, parent=None):
        QThread.__init__(self)
        movie.jumpToFrame(0)
        pixmap = QPixmap(movie.frameRect().size())
        pixmap.scaledToWidth(2000)

        QSplashScreen.__init__(self, pixmap)
        self.movie = movie
        self.movie.frameChanged.connect(self.repaint)

    def showEvent(self, event):
        self.movie.start()

    def hideEvent(self, event):
        self.movie.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        # pixmap.scaledToWidth(200)
        # pixmap.scaledToHeight(400)
        self.setMask(pixmap.mask())
        # painter.drawPixmap(0, 0,400,200, pixmap)
        painter.drawPixmap(0, 0, pixmap)

    def sizeHint(self):
        return self.movie.scaledSize(QSize(4.0, 4.0))


import os, random
from gui.splash import MovieSplashScreen
from PyQt4.QtGui import *

worker = []

def work():
    secure_random = random.SystemRandom()
    a = os.getcwd() + '\\splash\\' + secure_random.choice(
        os.listdir(os.getcwd() + '\splash'))  # change dir name to whatever
    movie = QMovie(os.getcwd()+'\splash\\' + random.choice(os.listdir(os.getcwd()+'\\splash')))
    #movie = QMovie(a)

    splash = MovieSplashScreen(movie)
    worker.append(splash)
    splash.start()
    splash.show()
    return movie

    # start = time.time()
    # while movie.state() == QMovie.Running and time.time() < start + 10:
    #     app.processEvents()