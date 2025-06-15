import mysql.connector 
from PyQt5.QtWidgets import QApplication

from SearchEngine import SearchEngine
from database.Database import Database
from database.Encryptor import Encryptor
from ui import App

import sys
import time

def main():
    SearchEngine.Initialize()
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()