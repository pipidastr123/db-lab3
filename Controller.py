from PyQt5.uic.properties import QtGui

from DataBase import DataBase
from design import Ui_MainWindow
from connection import ConnectionMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import datetime as dt
import datetime


class ConnectWindow(QMainWindow, ConnectionMainWindow):
    def __init__(self, dbApp):
        super().__init__()
        self.dbApp = dbApp
        self.setupUi(self)
        self.chooseFileButton.clicked.connect(self.chooseFile)
        self.confirmationButtons.accepted.connect(self.okPressed)
        self.confirmationButtons.rejected.connect(self.cancelPressed)

    def chooseFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', filter = "SQL files (*.sql)")
        self.fileTF.setText(fname[0])

    def okPressed(self):
        host = self.hostTF.text()
        name = self.dbNameTF.text()
        path = self.fileTF.text()
        port = self.portTF.text()
        login = self.loginTF.text()
        pwd = self.passwordTF.text()

        if host == '' or name == '' or path == '' or port == '' or login == '' or pwd == '':
            self.dbApp.show_alert('Error', 'Please, fill all fields')
            return
        try:
            self.dbApp.connect_to_postgres(host, port, login, pwd, name, path)
            self.close()
        except Exception as e:
            self.dbApp.show_alert('Error', str(e))

    def cancelPressed(self):
        self.close()
        self.dbApp.close()


class DBApp(QMainWindow, Ui_MainWindow):

    def __init__(self):
        self.db = None
        super().__init__()
        self.setupUi(self)
        self.c = ConnectWindow(self)
        self.actionConnect.triggered.connect(self.c.show)

        self.updating = False
        self.ordersTable.setColumnCount(6)
        self.consumersTable.setColumnCount(3)
        self.detailsTable.setColumnCount(3)
        self.useCurrentDateCheckBox.clicked.connect(self.toggle_datetime_widget)
        self.createOrderButton.clicked.connect(self.add_order)
        self.createConsumerButton.clicked.connect(self.add_consumer)
        self.createDetailButton.clicked.connect(self.add_detail)
        self.orderSearchButton.clicked.connect(self.search_order)
        self.searchConsumerButton.clicked.connect(self.search_consumer)
        self.searchDetailButton.clicked.connect(self.search_detail)
        self.orderDeleteButton.clicked.connect(self.delete_order)

        self.ordersTable.itemChanged.connect(self.update_order_record)
        self.consumersTable.itemChanged.connect(self.update_consumer_record)
        self.detailsTable.itemChanged.connect(self.update_detail_record)

        self.actionClear_All.triggered.connect(self.clear_all)
        self.actionClear_Consumers.triggered.connect(self.clear_consumers_table)
        self.actionClear_Details.triggered.connect(self.clear_details_table)
        self.actionClear_Orders.triggered.connect(self.clear_orders_table)

        self.actionRefresh_All.triggered.connect(self.refresh_all)
        self.actionRefresh_Consumers.triggered.connect(lambda: self.set_data_to_consumers_table())
        self.actionRefresh_Details.triggered.connect(lambda: self.set_data_to_details_table())
        self.actionRefresh_Orders.triggered.connect(lambda: self.set_data_to_orders_table())

    def connect_to_postgres(self, host, port, login, pwd, name, path):
        self.db = DataBase(address = host,
                           port = port,
                           login = login,
                           password = pwd,
                           db_name = name,
                           sql_file_source = path)
        self.set_data_to_consumers_table()
        self.set_data_to_details_table()
        self.set_data_to_orders_table()

    def refresh_all(self):
        self.set_data_to_consumers_table()
        self.set_data_to_details_table()
        self.set_data_to_orders_table()

    def clear_consumers_table(self):
        self.db.clear_consumers()
        self.set_data_to_consumers_table()

    def clear_details_table(self):
        self.db.clear_details()
        self.set_data_to_details_table()

    def clear_orders_table(self):
        self.db.clear_orders()
        self.set_data_to_orders_table()

    def clear_all(self):
        self.clear_consumers_table()
        self.clear_details_table()
        self.clear_orders_table()

    def toggle_datetime_widget(self):
        value = self.useCurrentDateCheckBox.isChecked()
        self.purchaseDateCreateOrderDT.setReadOnly(value)
        if value:
            self.purchaseDateCreateOrderDT.setDateTime(dt.datetime.now())

    def show_alert(self, title, message):
        QMessageBox.warning(self, title, message, QMessageBox.Ok)

    def set_data_to_orders_table(self, data = []):
        if len(data) == 0:
            data = self.db.get_orders()
        self.updating = True
        self.ordersTable.setRowCount(len(data))
        for row_num, row in enumerate(data):
            for col_num, col in enumerate(row):
                if isinstance(col, datetime.datetime):
                    self.ordersTable.setItem(row_num, col_num, QTableWidgetItem(col.strftime('%d.%m.%Y %H:%S')))
                else:
                    self.ordersTable.setItem(row_num, col_num, QTableWidgetItem(str(col)))
        self.updating = False

    def set_data_to_details_table(self, data = []):
        if len(data) == 0:
            data = self.db.get_details()
        self.updating = True
        self.detailsTable.setRowCount(len(data))
        for row_num, row in enumerate(data):
            for col_num, col in enumerate(row):
                self.detailsTable.setItem(row_num, col_num, QTableWidgetItem(str(col)))
        self.updating = False

    def set_data_to_consumers_table(self, data = []):
        if len(data) == 0:
            data = self.db.get_consumers()
        self.updating = True
        self.consumersTable.setRowCount(len(data))
        for row_num, row in enumerate(data):
            for col_num, col in enumerate(row):
                self.consumersTable.setItem(row_num, col_num, QTableWidgetItem(str(col)))
        self.updating = False

    def add_order(self):
        consumer_id = self.consumerIdCreateOrderTF.text()
        detail_id = self.detailIdCreateOrderTF.text()
        quantity = self.qunatityCreateOrderTF.text()
        try:
            quantity = int(quantity)
        except ValueError:
            self.show_alert('Warning', 'Please, check that in field "Quantity" You use only numbers')
            return
        date = self.purchaseDateCreateOrderDT.dateTime().toPyDateTime()
        self.db.add_order(consumer_id, detail_id, quantity, date)
        self.show_alert('Success', 'Record was successfully added')
        self.set_data_to_orders_table()

    def add_detail(self):
        name = self.nameDetailCreateTF.text()
        quantity = self.priceDetailCreateTF.text()
        try:
            quantity = int(quantity)
        except ValueError:
            self.show_alert('Warning', 'Please, check that in field "Quantity" You use only numbers')
            return
        self.db.add_detail(name, quantity)
        self.show_alert('Success', 'Record was successfully added')
        self.set_data_to_details_table()

    def add_consumer(self):
        name = self.nameCreateConsumerTF.text()
        address = self.addressCreateConsumerTF.text()
        self.db.add_consumer(name, address)
        self.show_alert('Success', 'Record was successfully added')
        self.set_data_to_consumers_table()

    def search_order(self):
        name = self.orderSearchTF.text()
        if not name:
            self.show_alert('Warning', 'Please, fill text field')
            return
        data = self.db.search_orders(name)
        if not data:
            self.show_alert('No matches', 'No matches were found for your query')
            return
        self.set_data_to_orders_table(data)

    def search_detail(self):
        name = self.detaiSearchTF.text()
        if not name:
            self.show_alert('Warning', 'Please, fill text field')
            return
        data = self.db.search_details(name)
        if not data:
            self.show_alert('No records', 'No matches were found for your query')
            return
        self.set_data_to_details_table(data)

    def search_consumer(self):
        name = self.consumerSearchTF.text()
        if not name:
            self.show_alert('Warning', 'Please, fill text field')
            return
        data = self.db.search_consumers(name)
        if not data:
            self.show_alert('No records', 'No matches were found for your query')
            return
        self.set_data_to_consumers_table(data)

    def delete_order(self):
        rows_nums = set([row.row() for row in self.ordersTable.selectedIndexes()])
        indexes = []
        for num in rows_nums:
            indexes.append(int(self.ordersTable.item(num, 0).text()))
        for index in indexes:
            self.db.delete_order(index)
            # self.ordersTable.setRowCount(self.ordersTable.rowCount() - 1)
        self.set_data_to_orders_table()

    def update_order_record(self, item):
        if not self.updating:
            index = int(self.ordersTable.item(item.row(), 0).text())
            col_ind = item.column()
            value = int(item.text())
            if col_ind == 2:
                try:
                    self.db.update_order_consumer_id(index, value)
                except:
                    self.show_alert('Error', 'Probably, there is no consumer with such id')
            elif col_ind == 3:
                try:
                    self.db.update_order_detail_id(index, value)
                except:
                    self.show_alert('Error', 'Probably, there is no detail with such id')
            elif col_ind == 4:
                self.db.update_order_quantity(index, value)
            else:
                self.show_alert('Warning', "You can change only consumer's and detail's ids and quantity")
                return
            self.set_data_to_orders_table()

    def update_detail_record(self, item):
        if not self.updating:
            col_ind = item.column()
            value = item.text()
            row = self.detailsTable.item(item.row(), 0)
            if row is None:
                self.show_alert('Error', 'Something went wrong')
                return
            index = int(row.text())
            print(item.column())
            if col_ind == 1:
                self.db.update_detail_name(index, value)
            elif col_ind == 2:
                try:
                    value = int(value)
                except ValueError:
                    self.show_alert('Error', 'Please, use digits only in "cost" field')
                    return
                self.db.update_detail_cost(index, value)
            else:
                self.show_alert('Warning', 'You can\' change id')
                return
            self.set_data_to_details_table()

    def update_consumer_record(self, item):
        if not self.updating:
            col_ind = item.column()
            value = item.text()
            row = self.consumersTable.item(item.row(), 0)
            if row is None:
                self.show_alert('Error', 'Something went wrong')
                return
            index = int(row.text())
            if col_ind == 1:
                try:
                    self.db.update_consumer_name(index, value)
                except:
                    self.show_alert('Error', 'Something went wrong')
            elif col_ind == 2:
                try:
                    self.db.update_consumer_address(index, value)
                except:
                    self.show_alert('Error', 'Something went wrong')
            else:
                self.show_alert('Warning', 'You can\' change id')
                return
            self.set_data_to_consumers_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DBApp()
    window.show()
    app.exec()
