import math
import os
from pathlib import Path
import sys
import random
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QMainWindow, \
    QVBoxLayout
from PySide6.QtCore import QFile, Qt, QSize
from PySide6.QtUiTools import QUiLoader
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from functions import DivideHashData, MiddleSquareHashData, CloteHashData, MultiplyHashData, ConvertNumberSystemHashData

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()
        self.window().setFixedSize(1073, 700)

        # размер массива
        self.spinbox1 = self.findChild(QSpinBox, "spinBox_1")
        self.array_size = self.spinbox1.value()
        self.spinbox1.valueChanged.connect(lambda: self.set_value(self.spinbox1.value()))

        # максимальный элемент
        self.spinbox2 = self.findChild(QSpinBox, "spinBox_2")
        self.max_element = self.spinbox2.value()
        self.spinbox2.valueChanged.connect(lambda: self.set_max_size(self.spinbox2.value()))

        # вкладка 1
        self.button1 = self.findChild(QPushButton, "pushButton_1")
        self.button1.clicked.connect(lambda: self.tab1_button_click())

        # таблица
        self.table1 = self.findChild(QTableWidget, "tableWidget_1")
        self.table1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table1.horizontalHeader().hide()
        self.table1.verticalHeader().hide()
        self.table1.setColumnCount(5)
        self.table1.setColumnWidth(0, 161)
        self.table1.setColumnWidth(1, 214)
        self.table1.setColumnWidth(2, 214)
        self.table1.setColumnWidth(3, 214)
        self.table1.setColumnWidth(4, 214)
        self.table1.setRowCount(3)
        self.table1.setRowHeight(0, 30)
        self.table1.setRowHeight(1, 30)
        self.table1.setRowHeight(2, 30)

        # названия столбцов
        self.table1.setItem(1, 0, QTableWidgetItem("Значение делителя"))
        self.table1.item(1, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table1.setItem(2, 0, QTableWidgetItem("Количество коллизий"))
        self.table1.item(2, 0).setTextAlignment(QtCore.Qt.AlignCenter)

        # названия строк
        self.table1.setItem(0, 1, QTableWidgetItem("Делитель 1"))
        self.table1.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table1.setItem(0, 2, QTableWidgetItem("Делитель 2"))
        self.table1.item(0, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table1.setItem(0, 3, QTableWidgetItem("Делитель 3"))
        self.table1.item(0, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table1.setItem(0, 4, QTableWidgetItem("Делитель 4"))
        self.table1.item(0, 4).setTextAlignment(QtCore.Qt.AlignCenter)

        # график
        self.graphicWidget1 = QMainWindow()
        self.graphic1 = pg.PlotWidget(name="plotWidget_1")
        self.graphic1.addLegend()
        self.graphic1.plot([0], [0], pen=pg.mkPen("b", width=2), name="Делитель 1", clear=True)
        self.graphic1.plot([0], [0], pen=pg.mkPen("g", width=2), name="Делитель 2")
        self.graphic1.plot([0], [0], pen=pg.mkPen("y", width=2), name="Делитель 3")
        self.graphic1.plot([0], [0], pen=pg.mkPen("r", width=2), name="Делитель 4")
        self.graphic1.setXRange(0, self.array_size * 1.05)
        self.graphic1.setYRange(0, self.array_size * 1.05)
        self.graphic1.setBackground("w")
        self.graphic1.showGrid(x=True, y=True)
        self.graphic1.setLabel("left", "Колллизии")
        self.graphic1.setLabel("bottom", "Элементы массива")
        self.graphic1.setMouseEnabled(x=False, y=False)
        self.graphicWidget1.setCentralWidget(self.graphic1)
        self.layout1 = self.findChild(QVBoxLayout, "verticalLayout_1")
        self.layout1.addWidget(self.graphicWidget1)

        # вкладка 2
        self.button2 = self.findChild(QPushButton, "pushButton_2")
        self.button2.clicked.connect(lambda: self.tab2_button_click())

        # таблица
        self.table2 = self.findChild(QTableWidget, "tableWidget_2")
        self.table2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table2.horizontalHeader().hide()
        self.table2.verticalHeader().hide()
        self.table2.setColumnCount(3)
        self.table2.setColumnWidth(0, 261)
        self.table2.setColumnWidth(1, 378)
        self.table2.setColumnWidth(2, 378)
        self.table2.setRowCount(2)
        self.table2.setRowHeight(0, 30)
        self.table2.setRowHeight(1, 30)

        # названия столбцов
        self.table2.setItem(0, 0, QTableWidgetItem("Сторона, с которой обрезано больше"))
        self.table2.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table2.setItem(1, 0, QTableWidgetItem("Количество коллизий"))
        self.table2.item(1, 0).setTextAlignment(QtCore.Qt.AlignCenter)

        # названия строк
        self.table2.setItem(0, 1, QTableWidgetItem("Справа"))
        self.table2.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table2.setItem(0, 2, QTableWidgetItem("Слева"))
        self.table2.item(0, 2).setTextAlignment(QtCore.Qt.AlignCenter)

        # график
        self.graphicWidget2 = QMainWindow()
        self.graphic2 = pg.PlotWidget(name="plotWidget_2")
        self.graphic2.addLegend()
        self.graphic2.plot([0], [0], pen=pg.mkPen("b", width=2), name="Справа", clear=True)
        self.graphic2.plot([0], [0], pen=pg.mkPen("g", width=2), name="Слева")
        self.graphic2.setXRange(0, self.array_size * 1.05)
        self.graphic2.setYRange(0, self.array_size * 1.05)
        self.graphic2.setBackground("w")
        self.graphic2.showGrid(x=True, y=True)
        self.graphic2.setLabel("left", "Колллизии")
        self.graphic2.setLabel("bottom", "Элементы массива")
        self.graphic2.setMouseEnabled(x=False, y=False)
        self.graphicWidget2.setCentralWidget(self.graphic2)
        self.layout2 = self.findChild(QVBoxLayout, "verticalLayout_2")
        self.layout2.addWidget(self.graphicWidget2)

        # вкладка 3
        self.button3 = self.findChild(QPushButton, "pushButton_3")
        self.button3.clicked.connect(lambda: self.tab3_button_click())

        # таблица
        self.table3 = self.findChild(QTableWidget, "tableWidget_3")
        self.table3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table3.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table3.horizontalHeader().hide()
        self.table3.verticalHeader().hide()
        self.table3.setColumnCount(3)
        self.table3.setColumnWidth(0, 261)
        self.table3.setColumnWidth(1, 378)
        self.table3.setColumnWidth(2, 378)
        self.table3.setRowCount(2)
        self.table3.setRowHeight(0, 30)
        self.table3.setRowHeight(1, 30)

        # названия столбцов
        self.table3.setItem(0, 0, QTableWidgetItem("Направление свертывания"))
        self.table3.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table3.setItem(1, 0, QTableWidgetItem("Количество коллизий"))
        self.table3.item(1, 0).setTextAlignment(QtCore.Qt.AlignCenter)

        # названия строк
        self.table3.setItem(0, 1, QTableWidgetItem("Слева направо"))
        self.table3.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table3.setItem(0, 2, QTableWidgetItem("Справа налево"))
        self.table3.item(0, 2).setTextAlignment(QtCore.Qt.AlignCenter)

        # график
        self.graphicWidget3 = QMainWindow()
        self.graphic3 = pg.PlotWidget(name="plotWidget_3")
        self.graphic3.addLegend()
        self.graphic3.plot([0], [0], pen=pg.mkPen("y", width=2), name="Слева направо", clear=True)
        self.graphic3.plot([0], [0], pen=pg.mkPen("c", width=2), name="Справа налево")
        self.graphic3.setXRange(0, self.array_size * 1.05)
        self.graphic3.setYRange(0, self.array_size * 1.05)
        self.graphic3.setBackground("w")
        self.graphic3.showGrid(x=True, y=True)
        self.graphic3.setLabel("left", "Колллизии")
        self.graphic3.setLabel("bottom", "Элементы массива")
        self.graphic3.setMouseEnabled(x=False, y=False)
        self.graphicWidget3.setCentralWidget(self.graphic3)
        self.layout3 = self.findChild(QVBoxLayout, "verticalLayout_3")
        self.layout3.addWidget(self.graphicWidget3)

        # вкладка 4
        self.button4 = self.findChild(QPushButton, "pushButton_4")
        self.button4.clicked.connect(lambda: self.tab4_button_click())

        # таблица
        self.table4 = self.findChild(QTableWidget, "tableWidget_4")
        self.table4.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table4.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table4.horizontalHeader().hide()
        self.table4.verticalHeader().hide()
        self.table4.setColumnCount(5)
        self.table4.setColumnWidth(0, 161)
        self.table4.setColumnWidth(1, 214)
        self.table4.setColumnWidth(2, 214)
        self.table4.setColumnWidth(3, 214)
        self.table4.setColumnWidth(4, 214)
        self.table4.setRowCount(3)
        self.table4.setRowHeight(0, 30)
        self.table4.setRowHeight(1, 30)
        self.table4.setRowHeight(2, 30)

        # названия столбцов
        self.table4.setItem(1, 0, QTableWidgetItem("Значение множителя"))
        self.table4.item(1, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table4.setItem(2, 0, QTableWidgetItem("Количество коллизий"))
        self.table4.item(2, 0).setTextAlignment(QtCore.Qt.AlignCenter)

        # названия строк
        self.table4.setItem(0, 1, QTableWidgetItem("Множитель 1"))
        self.table4.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table4.setItem(0, 2, QTableWidgetItem("Множитель 2"))
        self.table4.item(0, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table4.setItem(0, 3, QTableWidgetItem("Множитель 3"))
        self.table4.item(0, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table4.setItem(0, 4, QTableWidgetItem("Множитель 4"))
        self.table4.item(0, 4).setTextAlignment(QtCore.Qt.AlignCenter)

        # график
        self.graphicWidget4 = QMainWindow()
        self.graphic4 = pg.PlotWidget(name="plotWidget_4")
        self.graphic4.addLegend()
        self.graphic4.plot([0], [0], pen=pg.mkPen("b", width=2), name="Множитель 1", clear=True)
        self.graphic4.plot([0], [0], pen=pg.mkPen("g", width=2), name="Множитель 2")
        self.graphic4.plot([0], [0], pen=pg.mkPen("y", width=2), name="Множитель 3")
        self.graphic4.plot([0], [0], pen=pg.mkPen("r", width=2), name="Множитель 4")
        self.graphic4.setXRange(0, self.array_size * 1.05)
        self.graphic4.setYRange(0, self.array_size * 1.05)
        self.graphic4.setBackground("w")
        self.graphic4.showGrid(x=True, y=True)
        self.graphic4.setLabel("left", "Колллизии")
        self.graphic4.setLabel("bottom", "Элементы массива")
        self.graphic4.setMouseEnabled(x=False, y=False)
        self.graphicWidget4.setCentralWidget(self.graphic4)
        self.layout4 = self.findChild(QVBoxLayout, "verticalLayout_4")
        self.layout4.addWidget(self.graphicWidget4)

        # вкладка 5
        self.button5 = self.findChild(QPushButton, "pushButton_5")
        self.button5.clicked.connect(lambda: self.tab5_button_click())

        # таблица
        self.table5 = self.findChild(QTableWidget, "tableWidget_5")
        self.table5.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table5.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table5.horizontalHeader().hide()
        self.table5.verticalHeader().hide()
        self.table5.setColumnCount(5)
        self.table5.setColumnWidth(0, 161)
        self.table5.setColumnWidth(1, 214)
        self.table5.setColumnWidth(2, 214)
        self.table5.setColumnWidth(3, 214)
        self.table5.setColumnWidth(4, 214)
        self.table5.setRowCount(3)
        self.table5.setRowHeight(0, 30)
        self.table5.setRowHeight(1, 30)
        self.table5.setRowHeight(2, 30)

        # названия столбцов
        self.table5.setItem(1, 0, QTableWidgetItem("Значение основания"))
        self.table5.item(1, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table5.setItem(2, 0, QTableWidgetItem("Количество коллизий"))
        self.table5.item(2, 0).setTextAlignment(QtCore.Qt.AlignCenter)

        # названия строк
        self.table5.setItem(0, 1, QTableWidgetItem("Система 1"))
        self.table5.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table5.setItem(0, 2, QTableWidgetItem("Система 2"))
        self.table5.item(0, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table5.setItem(0, 3, QTableWidgetItem("Система 3"))
        self.table5.item(0, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table5.setItem(0, 4, QTableWidgetItem("Система 4"))
        self.table5.item(0, 4).setTextAlignment(QtCore.Qt.AlignCenter)

        # график
        self.graphicWidget5 = QMainWindow()
        self.graphic5 = pg.PlotWidget(name="plotWidget_5")
        self.graphic5.addLegend()
        self.graphic5.plot([0], [0], pen=pg.mkPen("b", width=2), name="Система 1", clear=True)
        self.graphic5.plot([0], [0], pen=pg.mkPen("g", width=2), name="Система 2")
        self.graphic5.plot([0], [0], pen=pg.mkPen("y", width=2), name="Система 3")
        self.graphic5.plot([0], [0], pen=pg.mkPen("r", width=2), name="Система 4")
        self.graphic5.setXRange(0, self.array_size * 1.05)
        self.graphic5.setYRange(0, self.array_size * 1.05)
        self.graphic5.setBackground("w")
        self.graphic5.showGrid(x=True, y=True)
        self.graphic5.setLabel("left", "Колллизии")
        self.graphic5.setLabel("bottom", "Элементы массива")
        self.graphic5.setMouseEnabled(x=False, y=False)
        self.graphicWidget5.setCentralWidget(self.graphic5)
        self.layout5 = self.findChild(QVBoxLayout, "verticalLayout_5")
        self.layout5.addWidget(self.graphicWidget5)

        # вкладка 6
        self.button6 = self.findChild(QPushButton, "pushButton_6")
        self.button6.clicked.connect(lambda: self.tab6_button_click())

        # таблица
        self.table6 = self.findChild(QTableWidget, "tableWidget_6")
        self.table6.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table6.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table6.horizontalHeader().hide()
        self.table6.verticalHeader().hide()
        self.table6.setColumnCount(6)
        self.table6.setColumnWidth(0, 153)
        self.table6.setColumnWidth(1, 110)
        self.table6.setColumnWidth(2, 184)
        self.table6.setColumnWidth(3, 144)
        self.table6.setColumnWidth(4, 135)
        self.table6.setColumnWidth(5, 290)
        self.table6.setRowCount(2)
        self.table6.setRowHeight(0, 30)
        self.table6.setRowHeight(1, 30)

        # названия столбцов
        self.table6.setItem(0, 0, QTableWidgetItem("Метод"))
        self.table6.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table6.setItem(1, 0, QTableWidgetItem("Количество коллизий"))
        self.table6.item(1, 0).setTextAlignment(QtCore.Qt.AlignCenter)

        # названия строк
        self.table6.setItem(0, 1, QTableWidgetItem("Метод деления"))
        self.table6.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table6.setItem(0, 2, QTableWidgetItem("Метод середины квадрата"))
        self.table6.item(0, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table6.setItem(0, 3, QTableWidgetItem("Метод свертывания"))
        self.table6.item(0, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table6.setItem(0, 4, QTableWidgetItem("Метод умножения"))
        self.table6.item(0, 4).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table6.setItem(0, 5, QTableWidgetItem("Метод преобразования систем счисления"))
        self.table6.item(0, 5).setTextAlignment(QtCore.Qt.AlignCenter)

        # график
        self.graphicWidget6 = QMainWindow()
        self.graphic6 = pg.PlotWidget(name="plotWidget_6")
        self.graphic6.addLegend()
        self.graphic6.plot([0], [0], pen=pg.mkPen("b", width=2), name="Метод деления", clear=True)
        self.graphic6.plot([0], [0], pen=pg.mkPen("g", width=2), name="Метод середины квадрата")
        self.graphic6.plot([0], [0], pen=pg.mkPen("y", width=2), name="Метод свертывания")
        self.graphic6.plot([0], [0], pen=pg.mkPen("k", width=2), name="Метод умножения")
        self.graphic6.plot([0], [0], pen=pg.mkPen("m", width=2), name="Метод умножения")
        self.graphic6.setXRange(0, self.array_size * 1.05)
        self.graphic6.setYRange(0, self.array_size * 1.05)
        self.graphic6.setBackground("w")
        self.graphic6.showGrid(x=True, y=True)
        self.graphic6.setLabel("left", "Колллизии")
        self.graphic6.setLabel("bottom", "Элементы массива")
        self.graphic6.setMouseEnabled(x=False, y=False)
        self.graphicWidget6.setCentralWidget(self.graphic6)
        self.layout6 = self.findChild(QVBoxLayout, "verticalLayout_6")
        self.layout6.addWidget(self.graphicWidget6)

    def load_ui(self):
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "form.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def set_value(self, num):
        self.array_size = num

    def set_max_size(self, num):
        self.max_element = num

    def tab1_button_click(self):
        data = DivideHashData(self.array_size, self.max_element)
        try:
            table = self.table1
            results = []
            for i in range(4):
                results.append(data.hash(type_of_del=i + 1))
            for i in range(4):
                table.setItem(1, i + 1, QTableWidgetItem(str(data.dividers[i])))
                table.item(1, i + 1).setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(2, i + 1, QTableWidgetItem(str(results[i][1])))
                table.item(2, i + 1).setTextAlignment(QtCore.Qt.AlignCenter)

            x = [int(self.array_size * a) for a in results[0].keys()]
            y1 = [a for a in results[0].values()]
            y2 = [a for a in results[1].values()]
            y3 = [a for a in results[2].values()]
            y4 = [a for a in results[3].values()]

            graphic = self.graphic1
            graphic.plot(x, y1, pen=pg.mkPen("b", width=2), name="Делитель 1", clear=True)
            graphic.plot(x, y2, pen=pg.mkPen("g", width=2), name="Делbтель 2")
            graphic.plot(x, y3, pen=pg.mkPen("y", width=2), name="Делитель 3")
            graphic.plot(x, y4, pen=pg.mkPen("r", width=2), name="Делитель 4")
            graphic.setYRange(0, max(10, 1.1 * math.ceil(max(*y1, *y2, *y3, *y4, 1) / pow(10, math.ceil(math.log10(max(*y1, *y2, *y3, *y4, 1)) - 1))) * pow(10, math.ceil(math.log10(max(*y1, *y2, *y3, *y4, 1))) - 1)))
            graphic.setXRange(0, max(1000, math.ceil(self.array_size) / pow(10, math.ceil(math.log10(self.array_size)) - 1) * pow(10, math.ceil(math.log10(self.array_size)) - 1)))

        except Exception as error:
            print(error)

    def tab2_button_click(self):
        data = MiddleSquareHashData(self.array_size, self.max_element)
        try:
            table = self.table2
            results = []
            for i in range(2):
                results.append(data.hash(type_of_cutting=i + 1))
            for i in range(2):
                table.setItem(1, i + 1, QTableWidgetItem(str(results[i][1])))
                table.item(1, i + 1).setTextAlignment(QtCore.Qt.AlignCenter)

            x = [int(self.array_size * a) for a in results[0].keys()]
            y1 = [a for a in results[0].values()]
            y2 = [a for a in results[1].values()]

            graphic = self.graphic2
            graphic.plot(x, y1, pen=pg.mkPen("b", width=2), name="Справа", clear=True)
            graphic.plot(x, y2, pen=pg.mkPen("g", width=2), name="Слева")
            graphic.setYRange(0, max(10, 1.1 * math.ceil(max(*y1, *y2, 1) / pow(10, math.ceil(math.log10(max(*y1, *y2, 1)) - 1))) * pow(10, math.ceil(math.log10(max(*y1, *y2, 1))) - 1)))
            graphic.setXRange(0, max(1000, math.ceil(self.array_size) / pow(10, math.ceil(math.log10(self.array_size)) - 1) * pow(10, math.ceil(math.log10(self.array_size)) - 1)))

        except Exception as error:
            print(error)

    def tab3_button_click(self):
        data = CloteHashData(self.array_size, self.max_element)
        results = []
        for i in range(2):
            results.append(data.hash(type_of_clotting=i + 1))

        try:
            table = self.table3
            for i in range(2):
                table.setItem(1, i + 1, QTableWidgetItem(str(results[i][1])))
                table.item(1, i + 1).setTextAlignment(QtCore.Qt.AlignCenter)

            x = [int(self.array_size * a) for a in results[0].keys()]
            y1 = [a for a in results[0].values()]
            y2 = [a for a in results[1].values()]

            graphic = self.graphic3
            graphic.plot(x, y1, pen=pg.mkPen("y", width=2), name="Слева направо", clear=True)
            graphic.plot(x, y2, pen=pg.mkPen("c", width=2), name="Справа налево")
            graphic.setYRange(0, max(10, 1.1 * math.ceil(max(*y1, *y2, 1) / pow(10, math.ceil(math.log10(max(*y1, *y2, 1)) - 1))) * pow(10, math.ceil(math.log10(max(*y1, *y2, 1))) - 1)))
            graphic.setXRange(0, max(1000, math.ceil(self.array_size) / pow(10, math.ceil(math.log10(self.array_size)) - 1) * pow(10, math.ceil(math.log10(self.array_size)) - 1)))

        except Exception as error:
            print(error)

    def tab4_button_click(self):
        data = MultiplyHashData(self.array_size, self.max_element, (5 ** 0.5 - 1) / 2, 0.61, 0.47, 0.83)
        try:
            table = self.table4
            results = []
            for i in range(4):
                results.append(data.hash(type_of_plural=i + 1))
            for i in range(4):
                table.setItem(1, i + 1, QTableWidgetItem(str(data.plurals[i])))
                table.item(1, i + 1).setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(2, i + 1, QTableWidgetItem(str(results[i][1])))
                table.item(2, i + 1).setTextAlignment(QtCore.Qt.AlignCenter)

            x = [int(self.array_size * a) for a in results[0].keys()]
            y1 = [a for a in results[0].values()]
            y2 = [a for a in results[1].values()]
            y3 = [a for a in results[2].values()]
            y4 = [a for a in results[3].values()]

            graphic = self.graphic4
            graphic.plot(x, y1, pen=pg.mkPen("b", width=2), name="Множитель 1", clear=True)
            graphic.plot(x, y2, pen=pg.mkPen("g", width=2), name="Множитель 2")
            graphic.plot(x, y3, pen=pg.mkPen("y", width=2), name="Множитель 3")
            graphic.plot(x, y4, pen=pg.mkPen("r", width=2), name="Множитель 4")
            graphic.setYRange(0, max(10, 1.1 * math.ceil(max(*y1, *y2, *y3, *y4, 1) / pow(10, math.ceil(math.log10(max(*y1, *y2, *y3, *y4, 1)) - 1))) * pow(10, math.ceil(math.log10(max(*y1, *y2, *y3, *y4, 1))) - 1)))
            graphic.setXRange(0, max(1000, math.ceil(self.array_size) / pow(10, math.ceil(math.log10(self.array_size)) - 1) * pow(10, math.ceil(math.log10(self.array_size)) - 1)))

        except Exception as error:
            print(error)

    def tab5_button_click(self):
        data = ConvertNumberSystemHashData(self.array_size, self.max_element, 11, 13, 19, 37)
        try:
            table = self.table5
            results = []
            for i in range(4):
                results.append(data.hash(type_of_system=i + 1))
            for i in range(4):
                table.setItem(1, i + 1, QTableWidgetItem(str(data.systems[i])))
                table.item(1, i + 1).setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(2, i + 1, QTableWidgetItem(str(results[i][1])))
                table.item(2, i + 1).setTextAlignment(QtCore.Qt.AlignCenter)

            x = [int(self.array_size * a) for a in results[0].keys()]
            y1 = [a for a in results[0].values()]
            y2 = [a for a in results[1].values()]
            y3 = [a for a in results[2].values()]
            y4 = [a for a in results[3].values()]

            graphic = self.graphic5
            graphic.plot(x, y1, pen=pg.mkPen("b", width=2), name="Система 1", clear=True)
            graphic.plot(x, y2, pen=pg.mkPen("g", width=2), name="Система 2")
            graphic.plot(x, y3, pen=pg.mkPen("y", width=2), name="Система 3")
            graphic.plot(x, y4, pen=pg.mkPen("r", width=2), name="Система 4")
            graphic.setYRange(0, max(10, 1.1 * math.ceil(max(*y1, *y2, *y3, *y4, 1) / pow(10, math.ceil(math.log10(max(*y1, *y2, *y3, *y4, 1)) - 1))) * pow(10, math.ceil(math.log10(max(*y1, *y2, *y3, *y4, 1))) - 1)))
            graphic.setXRange(0, max(1000, math.ceil(self.array_size) / pow(10, math.ceil(math.log10(self.array_size)) - 1) * pow(10, math.ceil(math.log10(self.array_size)) - 1)))

        except Exception as error:
            print(error)

    def tab6_button_click(self):
        s = random.random()
        try:
            type1 = 0
            type2 = 0
            type3 = 1
            type4 = 0
            type5 = 0
            table = self.table6
            results = []

            random.seed(s)
            data1 = DivideHashData(self.array_size, self.max_element)
            results.append(data1.hash(type_of_del=type1 + 1))

            random.seed(s)
            data2 = MiddleSquareHashData(self.array_size, self.max_element)
            results.append(data2.hash(type_of_cutting=type2 + 1))

            random.seed(s)
            data3 = CloteHashData(self.array_size, self.max_element)
            results.append(data3.hash(type_of_clotting=type3 + 1))

            random.seed(s)
            data4 = MultiplyHashData(self.array_size, self.max_element, (5 ** 0.5 - 1) / 2, 0.61, 0.47, 0.83)
            results.append(data4.hash(type_of_plural=type4 + 1))

            random.seed(s)
            data5 = ConvertNumberSystemHashData(self.array_size, self.max_element, 11, 13, 19, 37)
            results.append(data5.hash(type_of_system=type5 + 1))

            for i in range(5):
                table.setItem(1, i + 1, QTableWidgetItem(str(results[i][1])))
                table.item(1, i + 1).setTextAlignment(QtCore.Qt.AlignCenter)

            x = [int(self.array_size * a) for a in results[0].keys()]
            y1 = [a for a in results[0].values()]
            y2 = [a for a in results[1].values()]
            y3 = [a for a in results[2].values()]
            y4 = [a for a in results[3].values()]
            y5 = [a for a in results[4].values()]

            graphic = self.graphic6
            graphic.plot(x, y1, pen=pg.mkPen("b", width=2), name="Метод деления", clear=True)
            graphic.plot(x, y2, pen=pg.mkPen("g", width=2), name="Метод середины квадрата")
            graphic.plot(x, y3, pen=pg.mkPen("y", width=2), name="Метод свертывания")
            graphic.plot(x, y4, pen=pg.mkPen("k", width=2), name="Метод умножения")
            graphic.plot(x, y5, pen=pg.mkPen("m", width=2), name="Метод умножения")
            graphic.setYRange(0, max(10, 1.1 * math.ceil(max(*y1, *y2, *y3, *y4, *y5, 1) / pow(10, math.ceil(math.log10(max(*y1, *y2, *y3, *y4, *y5, 1)) - 1))) * pow(10, math.ceil(math.log10(max(*y1, *y2, *y3, *y4, *y5, 1))) - 1)))
            graphic.setXRange(0, max(1000, math.ceil(self.array_size) / pow(10, math.ceil(math.log10(self.array_size)) - 1) * pow(10, math.ceil(math.log10(self.array_size)) - 1)))

        except Exception as error:
            print(error)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
