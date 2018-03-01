from PyQt5.QtWidgets import (QWidget, QTableWidget, QAbstractItemView,
                             QVBoxLayout, QApplication, QPushButton,
                             QDialogButtonBox, QTableWidgetItem,
                             QHBoxLayout)
from PyQt5.QtGui import (QPalette, QColor)
from PyQt5.QtCore import Qt
import sys

MAX_ROW = 6


class TableProxy(object):
    def makeTable(self, name, row, height):
        table = QTableWidget()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.horizontalHeader().setStretchLastSection(False)
        [self.addTableRow(table, height) for i in range(MAX_ROW)]

        table.name = name
        table.rowPos = 0
        table.colPos = 0

        return table

    def removeAlltable(self, table):
        for column in range(table.columnCount() - 1, -1, -1):
            table.removeColumn(column)
        table.rowPos = 0
        table.colPos = 0

    def addTableRow(self, table, height):
        table.insertRow(table.rowCount())
        table.setRowHeight(table.rowCount() - 1, height)

    def addTableColumn(self, table, width):
        table.insertColumn(table.columnCount())

        column = table.columnCount() - 1
        table.setColumnWidth(column, width)
        [table.setItem(row, column, QTableWidgetItem('')) for row in range(MAX_ROW)]

    def tableItem(self, table, row, column, width):
        item = table.item(row, column)
        if item is None:
            self.addTableColumn(table, width)
            return table.item(row, column)
        return item

    def emptyColumnByRow(self, table, row):
        columnCount = table.columnCount()
        for column in range(columnCount):
            item = table.item(row, column)
            if not item:
                return column + 1
            if not item.text():
                return column
        return columnCount

    def iconsByColumn(self, table, column):
        rowCount = table.rowCount()
        count = 0

        for row in range(rowCount):
            item = table.item(row, column)
            if item and item.text():
                count += 1
        return count

    def updateTable(self, table, callback, width, key):
        color = QColor(Qt.blue) if key == 'P' else QColor(Qt.red)

        row = table.rowPos
        col = table.colPos
        currentItem = self.tableItem(table, row, col, width)

        if not currentItem.text():
            currentItem.setText(key)
            currentItem.setBackground(color)

            if callback:
                callback(currentItem.row(), currentItem.column())
        elif currentItem.text() != key:
            table.rowPos = 0
            table.colPos = self.emptyColumnByRow(table, 0)

            return self.updateTable(table, callback, width, key)
        elif currentItem.text() == key:
            if table.rowPos == 5:
                table.rowPos = table.rowPos
                table.colPos = table.colPos + 1

                return self.updateTable(table, callback, width, key)

            row = table.rowPos + 1
            col = table.colPos
            nextRowItem = self.tableItem(table, row, col, width)
            if not nextRowItem.text():
                table.rowPos = table.rowPos + 1
                table.colPos = table.colPos

                return self.updateTable(table, callback, width, key)
            elif nextRowItem.text():
                table.rowPos = table.rowPos
                table.colPos = table.colPos + 1

                return self.updateTable(table, callback, width, key)


class RoadMapWindow(QWidget):

    def __init__(self):
        super(RoadMapWindow, self).__init__()

        self.proxy = TableProxy()

        self.BeadPlateTable = self.proxy.makeTable('Bead Plate Table', MAX_ROW, 30)
        self.bigRoadTable = self.proxy.makeTable('Big Road Table', MAX_ROW, 30)
        self.bigEyeRoadTable = self.proxy.makeTable('Big Eye Road Table', MAX_ROW, 15)
        self.smallRoadTable = self.proxy.makeTable('Small Road Table', MAX_ROW, 15)
        self.cockroachPigTable = self.proxy.makeTable('Cockroach Pig Table', MAX_ROW, 15)

        self.playerWinButton = QPushButton("Player Win")
        palette = self.playerWinButton.palette()
        palette.setColor(QPalette.ButtonText, Qt.blue)
        self.playerWinButton.setPalette(palette)

        self.bankerWinButton = QPushButton("Banker Win")
        palette = self.bankerWinButton.palette()
        palette.setColor(QPalette.ButtonText, Qt.red)
        self.bankerWinButton.setPalette(palette)

        self.cleanButton = QPushButton("Clean All")

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(self.playerWinButton, QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.bankerWinButton, QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.cleanButton, QDialogButtonBox.ActionRole)

        self.playerWinButton.pressed.connect(self.updatePlayerWin)
        self.bankerWinButton.pressed.connect(self.updateBankerWin)
        self.cleanButton.pressed.connect(self.cleanAllTable)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.bigEyeRoadTable)
        leftLayout.addWidget(self.smallRoadTable)
        leftLayout.addWidget(self.cockroachPigTable)

        downLayout = QHBoxLayout()
        downLayout.addLayout(leftLayout)
        downLayout.addWidget(self.BeadPlateTable)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.bigRoadTable)
        mainLayout.addLayout(downLayout)
        mainLayout.addWidget(self.buttonBox)

        mainLayout.setStretchFactor(self.bigRoadTable, 1)
        mainLayout.setStretchFactor(downLayout, 1.5)

        self.setLayout(mainLayout)

        self.setWindowTitle("Baccarat RoadMap")
        self.setMinimumSize(960, 640)

        self.bigRoadColumn = 0
        self.bigRoadRow = 0

        self.bigEyeColumn = 0
        self.bigEyeRow = 0

    def cleanAllTable(self):
        self.proxy.removeAlltable(self.bigRoadTable)
        self.proxy.removeAlltable(self.bigEyeRoadTable)
        self.proxy.removeAlltable(self.smallRoadTable)
        self.proxy.removeAlltable(self.cockroachPigTable)

    def updatePlayerWin(self):
        table = self.bigRoadTable
        callback = self.updateOtherTable

        self.proxy.updateTable(table, callback, 30, 'P')

    def updateBankerWin(self):
        table = self.bigRoadTable
        callback = self.updateOtherTable

        self.proxy.updateTable(table, callback, 30, 'B')

    def updateBigEyeRoadBlue(self):
        table = self.bigEyeRoadTable
        callback = None

        self.proxy.updateTable(table, callback, 15, 'P')

    def updateBigEyeRoadRed(self):
        table = self.bigEyeRoadTable
        callback = None

        self.proxy.updateTable(table, callback, 15, 'B')

    def updateSmallRoadBlue(self):
        table = self.smallRoadTable
        callback = None

        self.proxy.updateTable(table, callback, 15, 'P')

    def updateSmallRoadRed(self):
        table = self.smallRoadTable
        callback = None

        self.proxy.updateTable(table, callback, 15, 'B')

    def updateCockroachPigBlue(self):
        table = self.cockroachPigTable
        callback = None

        self.proxy.updateTable(table, callback, 15, 'P')

    def updateCockroachPigRed(self):
        table = self.cockroachPigTable
        callback = None

        self.proxy.updateTable(table, callback, 15, 'B')

    def updateOtherTable(self, row, column):
        self.updateBigEyeRoadTable(row, column)
        self.updateSmallRoadTable(row, column)
        self.updateCockroachPigTable(row, column)

    def updateBigEyeRoadTable(self, row, column):
        if column == 0:
            return
        if column == 1 and row == 0:
            return
        if row == 0:
            count1 = self.proxy.iconsByColumn(self.bigRoadTable, column - 1)
            count2 = self.proxy.iconsByColumn(self.bigRoadTable, column - 2)
            if count1 == count2:
                self.updateBigEyeRoadRed()
            else:
                self.updateBigEyeRoadBlue()
        else:
            item1 = self.bigRoadTable.item(row, column - 1)
            item2 = self.bigRoadTable.item(row - 1, column - 1)
            if item1.text() == item2.text():
                self.updateBigEyeRoadRed()
            else:
                self.updateBigEyeRoadBlue()

    def updateSmallRoadTable(self, row, column):
        if column in (0, 1):
            return
        if column == 2 and row == 0:
            return
        if row == 0:
            count1 = self.proxy.iconsByColumn(self.bigRoadTable, column - 1)
            count2 = self.proxy.iconsByColumn(self.bigRoadTable, column - 3)
            if count1 == count2:
                self.updateSmallRoadRed()
            else:
                self.updateSmallRoadBlue()
        else:
            item1 = self.bigRoadTable.item(row, column - 2)
            item2 = self.bigRoadTable.item(row - 1, column - 2)
            if item1.text() == item2.text():
                self.updateSmallRoadRed()
            else:
                self.updateSmallRoadBlue()

    def updateCockroachPigTable(self, row, column):
        if column in (0, 1, 2):
            return
        if column == 3 and row == 0:
            return
        if row == 0:
            count1 = self.proxy.iconsByColumn(self.bigRoadTable, column - 1)
            count2 = self.proxy.iconsByColumn(self.bigRoadTable, column - 4)
            if count1 == count2:
                self.updateCockroachPigRed()
            else:
                self.updateCockroachPigBlue()
        else:
            item1 = self.bigRoadTable.item(row, column - 3)
            item2 = self.bigRoadTable.item(row - 1, column - 3)
            if item1.text() == item2.text():
                self.updateCockroachPigRed()
            else:
                self.updateCockroachPigBlue()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = RoadMapWindow()
    window.show()

    sys.exit(app.exec_())
