__author__ = 'mcagriaksoy'

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QListWidget
from PyQt6.uic import loadUi
from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from subprocess import Popen, PIPE, CalledProcessError

torrent_name = ""

class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    @pyqtSlot() # use a decorator to indicate that this method is a slot
    def __init__(self, torrent_name): # define the constructor method of the class
        super(Worker, self).__init__() # call the constructor of the parent class
        self.working = True # set an attribute named working to True
        self.torrent_name = torrent_name
        
    def work(self): # define a method named work that will perform the main task of the worker
        
        cmd = "python torrent_client.py " + self.torrent_name

        #print(cmd)
        with Popen(cmd, stderr=PIPE, bufsize=1, universal_newlines=True) as p:
            while True:
                line = p.stderr.readline()
                if not line: break
                self.intReady.emit(line) # emit the line as a signal

        self.finished.emit() # when the loop ends, emit the finished signal
    
class App(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('main.ui', self)
        
        self.thread = None
        self.worker = None
        
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
        self.textEdit.setText('')
        self.label_2.setText('Downloading..')
        
        self.worker = Worker(torrent_name)   # a new worker to perform those tasks
        self.thread = QThread()  # a new thread to run our background tasks in
        
        self.worker.moveToThread(self.thread)  # move the worker into the thread, do this first before connecting the signals
        self.thread.started.connect(self.worker.work) # begin our worker object's loop when the thread starts running
        self.worker.intReady.connect(self.onIntReady)
        self.worker.finished.connect(self.finish_download)       # do something in the gui when the worker loop ends
        self.worker.finished.connect(self.thread.quit)         # tell the thread it's time to stop running
        self.worker.finished.connect(self.worker.deleteLater)  # have worker mark itself for deletion
        self.thread.finished.connect(self.thread.deleteLater)  # have thread mark itself for deletion
        self.thread.start()
     
    def onIntReady(self, data):
        self.textEdit.insertPlainText("{}".format(data))

    def stop_download(self):
        self.label_2.setText('Stopped.')
        
    def finish_download(self):
        self.label_2.setText('Done.')
        self.textEdit.insertPlainText('The download process has been finished!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
