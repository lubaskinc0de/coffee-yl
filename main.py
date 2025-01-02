import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget, QDialog


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_coffee_data()
        self.setup_table()
        self.addButton.clicked.connect(self.open_add_edit_form)
        self.editButton.clicked.connect(self.open_edit_form)

    def load_coffee_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        coffee_data = cursor.fetchall()
        self.tableWidget.setRowCount(0)

        for row in coffee_data:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for col, data in enumerate(row):
                item = QTableWidgetItem(str(data))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, col, item)

        conn.close()

    def setup_table(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.editButton)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def open_add_edit_form(self):
        dialog = AddEditCoffeeForm(self)
        dialog.exec()

    def open_edit_form(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            coffee_id = self.tableWidget.item(selected_row, 0).text()
            name = self.tableWidget.item(selected_row, 1).text()
            roast_level = self.tableWidget.item(selected_row, 2).text()
            type = self.tableWidget.item(selected_row, 3).text()
            description = self.tableWidget.item(selected_row, 4).text()
            price = self.tableWidget.item(selected_row, 5).text()
            volume = self.tableWidget.item(selected_row, 6).text()

            dialog = AddEditCoffeeForm(self)
            dialog.set_coffee_data((coffee_id, name, roast_level, type, description, price, volume))
            dialog.exec()

    def add_coffee_to_db(self, name, roast_level, type, description, price, volume):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, package_size)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, roast_level, type, description, price, volume))
        conn.commit()
        conn.close()
        self.load_coffee_data()

    def edit_coffee_in_db(self, coffee_id, name, roast_level, type, description, price, volume):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE coffee
            SET name = ?, roast_level = ?, ground_or_beans = ?, taste_description = ?, price = ?, package_size = ?
            WHERE id = ?
        """, (name, roast_level, type, description, price, volume, coffee_id))
        conn.commit()
        conn.close()
        self.load_coffee_data()


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.saveButton.clicked.connect(self.save_coffee)
        self.cancelButton.clicked.connect(self.reject)
        self.coffee_id = None
        self.is_editing = False

    def set_coffee_data(self, coffee_data):
        self.coffee_id, name, roast_level, type, description, price, volume = coffee_data
        self.nameLineEdit.setText(name)
        self.roastLineEdit.setText(roast_level)
        self.typeComboBox.setCurrentText(type)
        self.descriptionTextEdit.setText(description)
        self.priceLineEdit.setText(str(price))
        self.volumeLineEdit.setText(str(volume))
        self.is_editing = True

    def save_coffee(self):
        name = self.nameLineEdit.text()
        roast_level = self.roastLineEdit.text()
        type = self.typeComboBox.currentText()
        description = self.descriptionTextEdit.toPlainText()
        price = self.priceLineEdit.text()
        volume = self.volumeLineEdit.text()

        if self.is_editing:
            coffee_id = self.coffee_id
            self.parent().edit_coffee_in_db(coffee_id, name, roast_level, type, description, price, volume)
        else:
            self.parent().add_coffee_to_db(name, roast_level, type, description, price, volume)

        self.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
