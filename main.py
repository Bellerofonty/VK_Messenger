# -*- coding: utf-8 -*-
''' Мессенджер на VK API с графическим интерфейсом'''

import sys

from PyQt5 import QtWidgets

import msg_app


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = msg_app.VkMessApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()