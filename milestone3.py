import sys
import time
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone3App.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.categoryList.itemSelectionChanged.connect(self.categoryChanged)

    def executeQuery(self,sql_str):
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='changeme'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT DISTINCT state FROM Business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed!")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex()>=0):
            sql_str = "SELECT DISTINCT city FROM Business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed!")

    def cityChanged(self):
        self.ui.zipList.clear()
        state = self.ui.stateList.currentText()
        city = self.ui.cityList.currentItem().text()
        if (self.ui.cityList.currentRow() >= 0):
            sql_str = "SELECT DISTINCT zip FROM Business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY zip;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipList.addItem(row[0])
            except:
                print("Query failed!")

    def zipChanged(self):
        self.ui.categoryList.clear()
        state = self.ui.stateList.currentText()
        city = self.ui.cityList.currentItem().text()
        zip = self.ui.zipList.currentItem().text()
        if (self.ui.zipList.currentRow() >= 0):
            sql_str = "SELECT DISTINCT cat FROM Category WHERE bus_id IN (SELECT bus_id FROM Business WHERE zip = '" + zip + "');"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print("Query failed!")


            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            for i in reversed(range(self.ui.categoryTable.rowCount())):
                self.ui.categoryTable.removeRow(i)
            for i in reversed(range(self.ui.popularTable.rowCount())):
                self.ui.popularTable.removeRow(i)
            for i in reversed(range(self.ui.successTable.rowCount())):
                self.ui.successTable.removeRow(i)
            self.ui.businessNumber.clear()
            self.ui.populationNumber.clear()
            self.ui.averageIncome.clear()

            sql_str = "SELECT name, address, city, bus_rating / 30.0, reviewcount, reviewrating, numCheckins FROM Business WHERE zip ='" + zip + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Reviews', 'Review Rating', 'Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 200)
                self.ui.businessTable.setColumnWidth(1, 200)
                self.ui.businessTable.setColumnWidth(2, 70)
                self.ui.businessTable.setColumnWidth(3, 50)
                self.ui.businessTable.setColumnWidth(4, 50)
                self.ui.businessTable.setColumnWidth(5, 100)
                self.ui.businessTable.setColumnWidth(6, 50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])):
                        if colCount < 3:
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(row[colCount]))
                        else:
                            if colCount == 3:
                                if round(results[currentRowCount][colCount],1) > 5.0: rating = str(5.0)
                                else: rating = str(round(results[currentRowCount][colCount],1))
                            else:
                                rating = str(round(results[currentRowCount][colCount],1))
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(rating))
                    currentRowCount += 1
            except:
                print("Query failed!")

            sql_str = "SELECT COUNT(*), C.cat FROM Business AS B, Category AS C WHERE B.zip = '" + zip + "' AND B.bus_id = C.bus_id GROUP BY C.cat ORDER BY COUNT(*) DESC;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.categoryTable.horizontalHeader().setStyleSheet(style)
                self.ui.categoryTable.setColumnCount(len(results[0]))
                self.ui.categoryTable.setRowCount(len(results))
                self.ui.categoryTable.setHorizontalHeaderLabels(['# Businesses', 'Category'])
                self.ui.categoryTable.resizeColumnsToContents()
                self.ui.categoryTable.setColumnWidth(0, 100)
                self.ui.categoryTable.setColumnWidth(1, 200)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])):
                        if colCount == 0:
                            rating = str(results[currentRowCount][colCount])
                            self.ui.categoryTable.setItem(currentRowCount,colCount,QTableWidgetItem(rating))
                        else:
                            self.ui.categoryTable.setItem(currentRowCount,colCount,QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed!")

            sql_str = "SELECT COUNT(*) FROM Business WHERE zip = '" + zip + "' GROUP BY zip;"            
            if (self.ui.zipList.currentRow() >= 0):
                try:
                    results = self.executeQuery(sql_str)
                    self.ui.businessNumber.addItem(str(results[0][0]))
                except:
                    print("Query failed!")

            sql_str = "SELECT population FROM zipcodeData WHERE zipcode = '" + zip + "';"            
            if (self.ui.zipList.currentRow() >= 0):
                try:
                    results = self.executeQuery(sql_str)
                    self.ui.populationNumber.addItem(str(results[0][0]))
                except:
                    print("Query failed!")

            sql_str = "SELECT meanIncome FROM zipcodeData WHERE zipcode = '" + zip + "';"            
            if (self.ui.zipList.currentRow() >= 0):
                try:
                    results = self.executeQuery(sql_str)
                    self.ui.averageIncome.addItem(str(results[0][0]))
                except:
                    print("Query failed!")

            sql_str = "SELECT name, popularity, reviewcount, reviewrating FROM Business WHERE zip = '" + zip + "' AND Business.popularity IS NOT NULL ORDER BY popularity DESC;"
            if (self.ui.zipList.currentRow() >= 0):
                try:

                    results = self.executeQuery(sql_str)
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.popularTable.horizontalHeader().setStyleSheet(style)
                    self.ui.popularTable.setColumnCount(len(results[0]))
                    self.ui.popularTable.setRowCount(10)
                    self.ui.popularTable.setHorizontalHeaderLabels(['Business', 'Popularity', '# Reviews', 'Rating'])
                    self.ui.popularTable.resizeColumnsToContents()
                    self.ui.popularTable.setColumnWidth(0, 200)
                    self.ui.popularTable.setColumnWidth(1, 100)
                    self.ui.popularTable.setColumnWidth(2, 100)
                    self.ui.popularTable.setColumnWidth(3, 100)
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0,len(results[0])):
                            match colCount:
                                case 0:
                                    print_str = row[colCount]
                                case 1:
                                    number = int(results[currentRowCount][colCount])
                                    print_str = str(number)
                                case 2:
                                    print_str = str(results[currentRowCount][colCount])
                                case 3:
                                    number = round(results[currentRowCount][colCount],1)
                                    print_str = str(number)

                            self.ui.popularTable.setItem(currentRowCount,colCount,QTableWidgetItem(print_str))                         
                        currentRowCount += 1
                        if currentRowCount > 9:
                            break
                except:
                    print("Query failed!")

            sql_str = "SELECT name, bus_rating / 30.0, reviewcount, reviewrating FROM Business WHERE zip = '" + zip + "' AND Business.bus_rating IS NOT NULL ORDER BY bus_rating DESC;"
            if (self.ui.zipList.currentRow() >= 0):
                try:

                    results = self.executeQuery(sql_str)
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.successTable.horizontalHeader().setStyleSheet(style)
                    self.ui.successTable.setColumnCount(len(results[0]))
                    self.ui.successTable.setRowCount(10)
                    self.ui.successTable.setHorizontalHeaderLabels(['Business', 'Success', '# Reviews', 'Rating'])
                    self.ui.successTable.resizeColumnsToContents()
                    self.ui.successTable.setColumnWidth(0, 200)
                    self.ui.successTable.setColumnWidth(1, 100)
                    self.ui.successTable.setColumnWidth(2, 100)
                    self.ui.successTable.setColumnWidth(3, 100)
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0,len(results[0])):
                            match colCount:
                                case 0:
                                    print_str = row[colCount]
                                case 1:
                                    number = round(results[currentRowCount][colCount],1)
                                    if number > 5.0:
                                        number = 5.0
                                    print_str = str(number)
                                case 2:
                                    print_str = str(results[currentRowCount][colCount])
                                case 3:
                                    number = round(results[currentRowCount][colCount],1)
                                    print_str = str(number)

                            self.ui.successTable.setItem(currentRowCount,colCount,QTableWidgetItem(print_str))
                        currentRowCount += 1
                        if currentRowCount > 9:
                            break
                except:
                    print("Query failed!")
                        

            

    
    def categoryChanged(self):
        zip = self.ui.zipList.currentItem().text()
        category = self.ui.categoryList.currentItem().text()
        if (self.ui.categoryList.currentRow() >= 0):
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            for i in reversed(range(self.ui.popularTable.rowCount())):
                self.ui.popularTable.removeRow(i)
            for i in reversed(range(self.ui.successTable.rowCount())):
                self.ui.successTable.removeRow(i)

            sql_str = "SELECT B.name, B.address, B.city, B.bus_rating / 30.0, B.reviewcount, B.reviewrating, B.numCheckins FROM Business AS B, Category AS C WHERE B.zip ='" + zip + "' AND B.bus_id = C.bus_id AND C.cat = '" + category + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Reviews', 'Reviw Rating', 'Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 200)
                self.ui.businessTable.setColumnWidth(1, 200)
                self.ui.businessTable.setColumnWidth(2, 70)
                self.ui.businessTable.setColumnWidth(3, 50)
                self.ui.businessTable.setColumnWidth(4, 50)
                self.ui.businessTable.setColumnWidth(5, 100)
                self.ui.businessTable.setColumnWidth(6, 50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])):

                        if colCount >= 3:
                            if colCount == 3:
                                if round(results[currentRowCount][colCount],1) > 5.0: rating = str(5.0) 
                                else: rating = str(round(results[currentRowCount][colCount],1))
                            else: rating = str(round(results[currentRowCount][colCount],1))          
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(rating))
                        else:
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed!")

            
            sql_str = "SELECT B.name, B.popularity, B.reviewcount, B.reviewrating FROM Business AS B, Category AS C WHERE B.zip = '" + zip + "' AND B.bus_id = C.bus_id AND C.cat = '" + category + "' AND B.popularity IS NOT NULL ORDER BY B.popularity DESC;"
            if (self.ui.zipList.currentRow() >= 0):
                try:
                    results = self.executeQuery(sql_str)
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.popularTable.horizontalHeader().setStyleSheet(style)
                    self.ui.popularTable.setColumnCount(len(results[0]))
                    self.ui.popularTable.setRowCount(10)
                    self.ui.popularTable.setHorizontalHeaderLabels(['Business', 'Popularity', '# Reviews', 'Rating'])
                    self.ui.popularTable.resizeColumnsToContents()
                    self.ui.popularTable.setColumnWidth(0, 200)
                    self.ui.popularTable.setColumnWidth(1, 100)
                    self.ui.popularTable.setColumnWidth(2, 100)
                    self.ui.popularTable.setColumnWidth(3, 100)
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0,len(results[0])):
                            match colCount:
                                case 0:
                                    print_str = row[colCount]
                                case 1:
                                    number = int(results[currentRowCount][colCount])
                                    print_str = str(number)
                                case 2:
                                    print_str = str(results[currentRowCount][colCount])
                                case 3:
                                    number = round(results[currentRowCount][colCount],1)
                                    print_str = str(number)

                            self.ui.popularTable.setItem(currentRowCount,colCount,QTableWidgetItem(print_str))    
                        currentRowCount += 1
                        if currentRowCount > 9:
                            break
                except:
                    print("Query failed!")

            sql_str = "SELECT B.name, B.bus_rating / 30.0, B.reviewcount, B.reviewrating FROM Business AS B, Category AS C WHERE B.zip = '" + zip + "' AND B.bus_id = C.bus_id AND C.cat = '" + category + "' AND B.bus_rating IS NOT NULL ORDER BY B.bus_rating DESC;"
            if (self.ui.zipList.currentRow() >= 0):
                try:
                    results = self.executeQuery(sql_str)
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.successTable.horizontalHeader().setStyleSheet(style)
                    self.ui.successTable.setColumnCount(len(results[0]))
                    self.ui.successTable.setRowCount(10)
                    self.ui.successTable.setHorizontalHeaderLabels(['Business', 'Success', '# Reviews', 'Rating'])
                    self.ui.successTable.resizeColumnsToContents()
                    self.ui.successTable.setColumnWidth(0, 200)
                    self.ui.successTable.setColumnWidth(1, 100)
                    self.ui.successTable.setColumnWidth(2, 100)
                    self.ui.successTable.setColumnWidth(3, 100)
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0,len(results[0])):
                            match colCount:
                                case 0:
                                    print_str = row[colCount]
                                case 1:
                                    number = round(results[currentRowCount][colCount],1)
                                    if number > 5.0:
                                        number = 5.0
                                    print_str = str(number)
                                case 2:
                                    print_str = str(results[currentRowCount][colCount])
                                case 3:
                                    number = round(results[currentRowCount][colCount],1)
                                    print_str = str(number)

                            self.ui.successTable.setItem(currentRowCount,colCount,QTableWidgetItem(print_str))
                        currentRowCount += 1
                        if currentRowCount > 9:
                            break
                except:
                    print("Query failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec())