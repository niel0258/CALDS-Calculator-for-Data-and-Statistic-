import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QFileDialog, 
                             QTableWidget, QHBoxLayout, QHeaderView, QScrollArea, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from Backend.DataHandler import DataHandler
#PAKYU YOKO NA MABUHAY
#FUCK YOU SHIT 

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
                                   color: white;
                                   """)

        label = QLabel("Select an action:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label.setStyleSheet("""
                            font-family: Arial;
                            font-weight: bold;
                            font-size: 20px;
                            padding: 30px;
                            color: white;
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
        table_page = QWidget()
        table_page.setStyleSheet("background-color: #101010;")
        self.stack.addWidget(table_page)
        layout = QVBoxLayout(table_page)
        self.table_list = []

        self.result_display = QLabel("Add a table and enter data to begin.")
        self.result_display.setWordWrap(True)
        self.result_display.setStyleSheet("color: #ff9f00; font-size: 14px; padding: 10px; background: #222; border-radius: 5px;")
        layout.addWidget(self.result_display)

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

        formula_btn = QPushButton("Formula") # Calculate Stats
        formula_btn.setStyleSheet("""
                                  QPushButton {
                                  background-color: green;
                                  }
                                  """)

        formula_btn.clicked.connect(lambda: self.show_menu(formula_btn))
        
        controls.addWidget(self.add_btn)
        controls.addWidget(back_btn)
        controls.addWidget(formula_btn)
        layout.addLayout(controls)

        # Scroll Area to handle overflow when tables are added side-by-side

        self.scroll = QScrollArea()
        self.scroll_content = QWidget()
        self.tables_layout = QHBoxLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        
        # KEY CHANGE: Using QHBoxLayout for horizontal alignment

    def handle_import(self):
        file, _ = QFileDialog.getOpenFileName(None, "Open CSV", "", "CSV Files (*.csv);;All Files(*)")
        
        if not file:
            return

        # Go to table screen and ensure tables are initialized
        self.go_to_tables()

        # Try to load data into each existing table using its handler
        errors = []

        for table in self.table_list:
            try:
                table.handler.import_data(file)
                # Reflect imported data into the QTableWidget cells
                data = table.handler.get_data()
                table.itemChanged.disconnect(table.sync)  # Prevent feedback loop
                for row, val in enumerate(data):
                    from PyQt6.QtWidgets import QTableWidgetItem
                    item = QTableWidgetItem(str(val))
                    table.setItem(row, 0, item)
                table.itemChanged.connect(table.sync)
            except KeyError:
                errors.append(f"Column '{table.handler.get_data_name()}' not found in CSV.")
            except Exception as e:
                errors.append(str(e))

        if errors:
            self.result_display.setText("Import issues:\n" + "\n".join(errors))
        else:
            self.result_display.setText("CSV imported successfully.")

    def go_to_tables(self):
        while self.tables_layout.count():
            item = self.tables_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.add_btn.setEnabled(True)
        self.add_new_table()
        self.stack.setCurrentIndex(1)

    class IntegratedTable(QTableWidget):
        def __init__(self, label):
            super().__init__(32,1)
            self.setHorizontalHeaderLabels([label])
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            # self.styleSheet("background-color: #2b2b2b; color: white;")
            self.itemChanged.connect(self.sync)

        def sync(self, item):
            try:
                val = float(item.text())
                self.handler.mod_data(item.row(), val)
            except (ValueError, AttributeError):
                self.handler.mod_data(item.row(), None)

    def add_new_table(self):
        count = len(self.table_list)
        if count < 3:
            label = f"Data {'X' if count == 0 else 'Y' if count == 1 else 'Z'}"
            t = self.IntegratedTable(label)

            # Assign a DataHandler to the table
            t.handler = DataHandler(label)

            self.table_list.append(t)
            self.tables_layout.addWidget(t)
            if len(self.table_list) == 3:
                self.add_btn.setEnabled(False)

    def show_menu(self, btn):
            if not self.table_list:
                self.result_display.setText("Invalid: No tables exist.")
                return
                
            menu = QMenu(self)
            h_x = self.table_list[0].handler # Always use Table 1 as primary X
            
            # Helper to safely execute and display
            def safe_exec(func, name):
                try:
                    res = func() #Result is the value return by the function
                    self.result_display.setText(f"{name}: {res:.4f}") #Rounded to 4 decimal places
                except Exception:
                    self.result_display.setText("Result: Invalid input / output")

            menu.addAction("Mean (Table X)", lambda: safe_exec(h_x.mean, "Mean"))
            #ADD CENTRAL TENDENCIES TABLE X
            menu.addAction("Std Dev (Table X)", lambda: safe_exec(lambda: h_x.sd(2), "SD"))
            
            # Pearson's R appears if 2nd table exists
            if len(self.table_list) >= 2:
                #ADD CENTRAL TENDENCIES FOR TABLE Y
                menu.addSeparator()
                data_y = self.table_list[1].handler.get_data()
                menu.addAction("Pearson R (X vs Y)", 
                            lambda: safe_exec(lambda: h_x.pearson_r(data_y), "Pearson R"))
                
            menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileApp()
    window.setStyleSheet("background-color: rgba(16,16,16,0.829)")
    window.show()
    sys.exit(app.exec())
