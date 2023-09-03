import sys
from datetime import datetime, timedelta
from pymongo import MongoClient
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox

from PyQt5.QtCore import QDateTime

# Initialize MongoDB
client = MongoClient(
    "mongodb+srv://jinyoonok:jinyoon981023@cmpsc487-jinyoon.vuymlgv.mongodb.net/?retryWrites=true&w=majority")
db = client['CMPSC487']
users_collection = db['users']
accesslogs_collection = db['accessLogs']


class LoginWindow(QWidget):
    def __init__(self, userId, collection):
        super().__init__()
        self.userId = userId
        self.collection = collection
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.check_password)

        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)
        self.setWindowTitle('Login')
        self.show()

    def check_password(self):
        user = self.collection.find_one({"userId": self.userId})
        if user:
            if user['password'] == self.password_input.text():
                self.close()
                self.search_window = SearchWindow(accesslogs_collection)
                self.search_window.show()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Invalid Password!")
                msg.setWindowTitle("Authentication Error")
                msg.exec_()
        else:
            self.password_label.setText('User not found!')


class SearchWindow(QWidget):
    def __init__(self, collection):
        super().__init__()
        self.collection = collection
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # User ID
        self.userId_label = QLabel('User ID', self)
        self.userId_input = QLineEdit(self)
        self.userId_input.setPlaceholderText('Enter User ID')

        # Default values
        current_date_time = QDateTime.currentDateTime()
        one_week_ago = current_date_time.addDays(-7)

        # Start Date
        self.start_date_label = QLabel('Start Date', self)
        self.start_date_input = QLineEdit(self)
        self.start_date_input.setPlaceholderText('YYYY-MM-DD')
        self.start_date_input.setText(one_week_ago.date().toString('yyyy-MM-dd'))

        # Start Time
        self.start_time_label = QLabel('Start Time', self)
        self.start_time_input = QLineEdit(self)
        self.start_time_input.setPlaceholderText('HH:MM:SS')
        self.start_time_input.setText(one_week_ago.time().toString('hh:mm:ss'))

        # End Date
        self.end_date_label = QLabel('End Date', self)
        self.end_date_input = QLineEdit(self)
        self.end_date_input.setPlaceholderText('YYYY-MM-DD')
        self.end_date_input.setText(current_date_time.date().toString('yyyy-MM-dd'))

        # End Time
        self.end_time_label = QLabel('End Time', self)
        self.end_time_input = QLineEdit(self)
        self.end_time_input.setPlaceholderText('HH:MM:SS')
        self.end_time_input.setText(current_date_time.time().toString('hh:mm:ss'))

        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_db)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["User ID", "Entry Time", "Exit Time"])

        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 250)

        self.layout.addWidget(self.userId_label)
        self.layout.addWidget(self.userId_input)
        self.layout.addWidget(self.start_date_label)
        self.layout.addWidget(self.start_date_input)
        self.layout.addWidget(self.end_date_label)
        self.layout.addWidget(self.end_date_input)
        self.layout.addWidget(self.start_time_label)
        self.layout.addWidget(self.start_time_input)
        self.layout.addWidget(self.end_time_label)
        self.layout.addWidget(self.end_time_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.setWindowTitle('Search')
        self.resize(800, 600)
        self.show()

    def search_db(self):
        query = {}

        if self.userId_input.text():
            query['userId'] = int(self.userId_input.text())

        start_date_str = self.start_date_input.text() or (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date_str = self.end_date_input.text() or datetime.now().strftime('%Y-%m-%d')
        start_time_str = self.start_time_input.text() or (datetime.now() - timedelta(days=7)).strftime('%H:%M:%S')
        end_time_str = self.end_time_input.text() or datetime.now().strftime('%H:%M:%S')

        start_datetime = datetime.strptime(f"{start_date_str} {start_time_str}", '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(f"{end_date_str} {end_time_str}", '%Y-%m-%d %H:%M:%S')

        if end_datetime < start_datetime:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("End time cannot be prior to the start time.")
            msg.setWindowTitle("Date & Time Error")
            msg.exec_()
            return  # Stop function execution

        # Adjust start and end times based on whether they've been set
        if start_time_str:
            query['entryTime'] = {"$gte": start_datetime}
        else:
            query['entryTime'] = {"$gte": start_datetime.date()}

        if end_time_str:
            if 'exitTime' in query:
                query['exitTime'].update({"$lte": end_datetime})
            else:
                query['exitTime'] = {"$lte": end_datetime}
        else:
            end_date_only = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
            if 'exitTime' in query:
                query['exitTime'].update({"$lt": end_date_only})
            else:
                query['exitTime'] = {"$lt": end_date_only}

        print("Query:", query)
        results = list(self.collection.find(query))
        print("Results Count:", len(results))

        self.table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.table.insertRow(row_number)
            self.table.setItem(row_number, 0, QTableWidgetItem(str(row_data.get('userId', ''))))
            entry_time = row_data.get('entryTime', None)
            exit_time = row_data.get('exitTime', None)
            self.table.setItem(row_number, 1,
                               QTableWidgetItem(entry_time.strftime('%Y-%m-%d %H:%M:%S') if entry_time else ''))
            self.table.setItem(row_number, 2,
                               QTableWidgetItem(exit_time.strftime('%Y-%m-%d %H:%M:%S') if exit_time else ''))


def main():
    userId = int(input("Enter userId: "))
    user = users_collection.find_one({"userId": userId})
    if user and user['userType'] == 'janitor':
        app = QApplication([])
        window = LoginWindow(userId, users_collection)
        sys.exit(app.exec_())
    else:
        print("Access Denied")


if __name__ == "__main__":
    main()
