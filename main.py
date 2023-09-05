__author__ = 'mcagriaksoy'

from torrent_client import Run
import sys, logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QListWidget
from PyQt6.uic import loadUi
from PyQt6.QtCore import QThreadPool, QRunnable, pyqtSlot

torrent_name = ""

class Worker(QRunnable):
    @pyqtSlot()
    def run(self):
        logging.basicConfig(level=logging.ERROR)
        run = Run(torrent_name)
        run.start()

class App(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('main.ui', self)
        self.threadpool = QThreadPool()
        self.pushButton.clicked.connect(self.load_torrent_file)
        self.pushButton_2.clicked.connect(self.start_download)
        self.pushButton_3.clicked.connect(self.stop_download)

    def load_torrent_file(self):
        # Open file dialog to select directory
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Torrent Files (*.torrent)")
        if fname[0]:
            self.textBrowser.setText(fname[0])
        
        global torrent_name
        torrent_name = fname[0]
    
    def start_download(self):
        self.label_2.setText('Downloading..')
        worker = Worker()
        self.threadpool.globalInstance().start(worker)

    def stop_download(self):
        self.label_2.setText('Stopped.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
