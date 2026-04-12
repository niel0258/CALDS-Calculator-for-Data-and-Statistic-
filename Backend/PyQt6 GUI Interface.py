import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QFileDialog, 
                             QTableWidget, QHBoxLayout, QHeaderView, QScrollArea, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from DataHandler import DataHandler

class FileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CalDS Application")
        # self.resize(1200, 700) # Wider default size for side-by-side tables
        self.resize(500, 650)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.init_menu_screen()
        self.init_table_screen()

    def init_menu_screen(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        button_layout = QHBoxLayout()
        
        # Control Buttons
        label_header = QLabel("[ CalDS Application ]")
        label_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_header.setStyleSheet("""
                                   font-size: 30px;
                                   font-family arial;
                                   font-weight: bold;
                                   """)

        label = QLabel("Select an action:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label.setStyleSheet("""
                            font-family: Arial;
                            font-weight: bold;
                            font-size: 20px;
                            padding: 30px;
                            """)

        btn_import = QPushButton("Import File")
        btn_import.setStyleSheet("""
                                QPushButton {
                                background-color: #ff9f00;
                                color: black;
                                font-size: 15px;
                                font-family arial;
                                font-weight: bold;
                                border-radius: 10px;
                                }

                                QPushButton:hover {
                                background-color: rgba(30, 74, 141, 0.900);
                                }
                                """)
        
        btn_import.setFixedSize(200, 50)
        btn_import.clicked.connect(self.handle_import)
        
        btn_new = QPushButton("Create New File")
        btn_new.setFixedSize(200, 50)
        btn_new.setStyleSheet("""
                              QPushButton {
                              background-color: rgba(28, 134, 184, 0.925);
                              font-size: 14px;
                              font-family: arial;
                              border-radius: 10px;
                              }
                              QPushButton:hover {
                              background-color: rgba(30, 74, 141, 0.900);
                              }
                              """)
        btn_new.clicked.connect(self.go_to_tables)

        exit_btn = QPushButton("Exit")
        exit_btn.setFixedSize(100, 25)
        exit_btn.setStyleSheet("""
                               QPushButton:hover {
                               background-color: rgba(35, 35, 35, 0.500);
                               }
                               """)
        exit_btn.clicked.connect(QApplication.instance().quit)

        layout.addStretch(1)
        layout.addWidget(label_header)
        layout.addStretch(1)
        layout.addWidget(label)
        button_layout.addWidget(btn_import)
        button_layout.addWidget(btn_new)
        layout.addLayout(button_layout)
        layout.addStretch(1)
        layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(4)
        self.stack.addWidget(page)

    def init_table_screen(self):
        self.table_page = QWidget()
        main_layout = QVBoxLayout(self.table_page)
        
        # Control Buttons

        controls = QHBoxLayout()
        self.add_btn = QPushButton("Add Table (Max 3)")
        self.add_btn.setStyleSheet("""
                                   QPushButton {
                                   background-color: darkblue;
                                   }
                                   """)
        self.add_btn.clicked.connect(self.add_new_table)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet ("""
                                QPushButton {
                                background-color: rgba(37, 37, 37, 0.900);
                                }
                                """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        formula_btn = QPushButton("Formula")
        formula_btn.setStyleSheet("""
                                  QPushButton {
                                  background-color: green;
                                  }
                                  """)
        formula_btn.clicked.connect(lambda: self.open_formula_menu(formula_btn))
        
        controls.addWidget(self.add_btn)
        controls.addWidget(back_btn)
        controls.addWidget(formula_btn)
        main_layout.addLayout(controls)

        # Scroll Area to handle overflow when tables are added side-by-side

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        
        # KEY CHANGE: Using QHBoxLayout for horizontal alignment

        self.tables_container = QHBoxLayout(self.scroll_content)
        self.tables_container.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        scroll.setWidget(self.scroll_content)
        main_layout.addWidget(scroll)

        self.table_list = []
        self.stack.addWidget(self.table_page)

    def handle_import(self):
        # file, _ = QFileDialog.getOpenFileName(self, "Open File")
        # if file: self.go_to_tables()
        # For specific, files
        file, _ = QFileDialog.getOpenFileName(None, "Open CSV", "", "CSV Files (*.csv);;All Files(*)")
        if file: self.go_to_table()

    def go_to_tables(self):
        # Clear existing tables
        while self.tables_container.count():
            item = self.tables_container.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        
        self.table_list = []
        self.add_btn.setEnabled(True)
        self.add_new_table() 
        self.stack.setCurrentIndex(1)

    def open_formula_menu(self, button):
        
        menu = QMenu(self)

        sum_action = QAction("Sum (Column B)", self)
        avg_action = QAction("Average (Column B)", self)
        max_action = QAction("Find Max", self)
        clear_action = QAction("Clear All Formulas", self)

        sum_action.triggered.connect(lambda: self.apply_formula("SUM"))
        avg_action.triggered.connect(lambda: self.apply_formula("AVERAGE"))
        max_action.triggered.connect(lambda: self.apply_formula("MAX"))

        menu.addAction(sum_action)
        menu.addAction(avg_action)
        menu.addAction(max_action)
        menu.addSeparator()
        menu.addAction(clear_action)

        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    def apply_formula(self, formula_type):
        """Logic to calculate values from the active table"""
        if not self.table_list:
            return

        target_table = self.table_list[0]
        values = []
        result = 0

        for row in range (target_table.rowCount()):
            item = target_table.item(row,1)
            if item and item.text().replace('.', '', 1).isdigit():
                values.append(float(item.text()))
        
        if not values:
            print(" No numeric data found in Column B")
            return
        
        if formula_type == "SUM":
            result = sum(values)
        elif formula_type == "AVERAGE":
            result = sum(values) / len(values)
        elif formula_type == "MAX":
            result = max(values)

        print(f"Result of {formula_type}: {result}")



    def add_new_table(self):
        if len(self.table_list) < 3:
            # Setup table
            table = QTableWidget(32, 1) #32 column, 1 row 
            table.setHorizontalHeaderLabels([ "Value"])
            table.setMinimumWidth(350) # Ensure tables have a readable width
            table.setStyleSheet("""
                                background-color: rgba(56, 55, 56, 0.925);
                                """)
            
            header = table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            header.setStyleSheet("""
                                 background-color: rgba(34, 34, 34, 0.900);
                                 """)
            
            self.tables_container.addWidget(table)
            self.table_list.append(table)
            
            if len(self.table_list) == 3:
                self.add_btn.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileApp()
    window.setStyleSheet("background-color: rgba(16,16,16,0.829)")
    window.show()
    sys.exit(app.exec())
