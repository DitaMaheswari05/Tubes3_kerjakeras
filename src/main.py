import mysql.connector # harus pertama
from PyQt5.QtWidgets import QApplication
import sys

from SearchEngine import SearchEngine
from database.Database import Database
from database.Encryptor import Encryptor
from ui.app import ApplicantTrackingSystem
from ui.app import App
import time

def main():
    # SearchEngine.Initialize()
    app = QApplication(sys.argv)
    window = ApplicantTrackingSystem()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
