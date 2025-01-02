import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_coffee_data()
        self.setup_table()

    def load_coffee_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        coffee_data = cursor.fetchall()

        for row in coffee_data:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for col, data in enumerate(row):
                item = QTableWidgetItem(str(data))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, col, item)

        conn.close()

    def setup_table(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
