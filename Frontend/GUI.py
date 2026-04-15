import sys, json, csv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFileDialog,
    QTableWidget, QHBoxLayout, QHeaderView, QScrollArea,
    QFrame, QTableWidgetItem
)
from PyQt6.QtCore import Qt


class FileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CalDS")
        self.resize(1200, 800)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.tables = []
        self.active_table = None
        self.theme_mode = "dark"
        self.make_menu()
        self.make_workspace()
        self.apply_theme()

    # menu 
    def make_menu(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("CalDS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 100px; font-weight: bold;")
        subtitle = QLabel("Calculator for Data and Statistic System")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color:#888; font-size:16px;")
        start_btn = QPushButton("Start")
        start_btn.setFixedHeight(50)
        start_btn.clicked.connect(self.open_workspace)
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.stack.addWidget(page)

    # main 
    def make_workspace(self):
        self.page = QWidget()
        main = QVBoxLayout(self.page)
        self.stack.addWidget(self.page)

        # header
        header = QFrame()
        header.setObjectName("Header")
        header.setFixedHeight(50)
        h = QHBoxLayout(header)
        title = QLabel("CalDS Dashboard")
        self.status = QLabel("System ready")
        h.addWidget(title)
        h.addStretch()
        h.addWidget(self.status)
        main.addWidget(header)

        # buttons 
        row = QHBoxLayout()
        self.btn_add = QPushButton("Add Table")
        self.btn_remove = QPushButton("Remove")
        btn_clear = QPushButton("Clear")
        btn_save = QPushButton("Save")
        btn_load = QPushButton("Load")
        btn_export = QPushButton("Export CSV")
        btn_theme = QPushButton("Theme")
        btn_back = QPushButton("Back")
        self.btn_add.clicked.connect(self.add_table)
        self.btn_remove.clicked.connect(self.remove_table)
        btn_clear.clicked.connect(self.clear_table)
        btn_save.clicked.connect(self.save_project)
        btn_load.clicked.connect(self.load_project)
        btn_export.clicked.connect(self.export_csv)
        btn_theme.clicked.connect(self.switch_theme)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        for b in [self.btn_add, self.btn_remove, btn_clear, btn_save, btn_load, btn_export, btn_theme, btn_back]:
            b.setCursor(Qt.CursorShape.PointingHandCursor)
        row.addWidget(self.btn_add)
        row.addWidget(self.btn_remove)
        row.addWidget(btn_clear)
        row.addWidget(btn_save)
        row.addWidget(btn_load)
        row.addWidget(btn_export)
        row.addWidget(btn_theme)
        row.addStretch()
        row.addWidget(btn_back)
        main.addLayout(row)

        # table 
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.container = QHBoxLayout(self.content)
        scroll.setWidget(self.content)
        main.addWidget(scroll)

    # create 
    def create_table(self, data=None):
        table = QTableWidget(32, 2)
        table.setHorizontalHeaderLabels(["Key", "Value"])
        table.setMinimumSize(450, 520)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.itemClicked.connect(lambda: self.select_table(table))
        if data:
            for r, row in enumerate(data):
                for c, val in enumerate(row):
                    if val:
                        table.setItem(r, c, QTableWidgetItem(val))
        return table

    # add 
    def add_table(self):
        table = self.create_table()
        self.container.addWidget(table)
        self.tables.append(table)
        self.select_table(table)
        self.status.setText(f"Table created ({len(self.tables)} total)")

    # select 
    def select_table(self, table):
        self.active_table = table
        self.status.setText("Table selected")

    # remove 
    def remove_table(self):
        if not self.tables:
            return
        table = self.active_table or self.tables[-1]
        self.container.removeWidget(table)
        table.deleteLater()
        self.tables.remove(table)
        self.active_table = self.tables[-1] if self.tables else None
        self.status.setText(f"Table removed ({len(self.tables)} remaining)")

    # clear 
    def clear_table(self):
        if self.active_table:
            self.active_table.clearContents()
            self.status.setText("Table cleared")

    # export csv
    def export_csv(self):
        if not self.active_table:
            return
        file, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV (*.csv)")
        if not file:
            return
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            for r in range(self.active_table.rowCount()):
                row = []
                for c in range(self.active_table.columnCount()):
                    item = self.active_table.item(r, c)
                    row.append(item.text() if item else "")
                writer.writerow(row)
        self.status.setText("CSV exported successfully")

    # save 
    def save_project(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "JSON (*.json)")
        if not file:
            return
        data = []
        for t in self.tables:
            temp = []
            for r in range(t.rowCount()):
                row = []
                for c in range(t.columnCount()):
                    item = t.item(r, c)
                    row.append(item.text() if item else "")
                temp.append(row)
            data.append(temp)

        with open(file, "w") as f:
            json.dump(data, f)
        self.status.setText("Project saved successfully")

    # load 
    def load_project(self):
        file, _ = QFileDialog.getOpenFileName(self, "Load Project", "", "JSON (*.json)")
        if not file:
            return
        with open(file, "r") as f:
            data = json.load(f)
        for t in self.tables:
            self.container.removeWidget(t)
            t.deleteLater()
        self.tables = []
        for tdata in data:
            table = self.create_table(tdata)
            self.container.addWidget(table)
            self.tables.append(table)
        self.active_table = self.tables[0] if self.tables else None
        self.status.setText("Project loaded successfully")

    # switch theme
    def switch_theme(self):
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        self.apply_theme()
    def apply_theme(self):
        self.setStyleSheet(self.dark() if self.theme_mode == "dark" else self.light())

    # dark theme
    def dark(self):
        return """
        QWidget { background:#0B0B0B; color:#EAEAEA; }
        QFrame#Header {
            background:#121212;
            border-bottom:1px solid #222;
        }
        QPushButton {
            background:#151515;
            border:1px solid #2A2A2A;
            padding:8px;
            border-radius:8px;
        }
        QPushButton:hover {
            background:#1C1C1C;
        }
        QTableWidget {
            background:#121212;
            border:1px solid #2A2A2A;
            gridline-color:#3A3A3A;
        }
        QTableWidget::item {
            border-right:1px solid #2A2A2A;
            border-bottom:1px solid #2A2A2A;
            padding:4px;
        }
        QTableWidget::item:selected {
            background:#2F2F2F;
        }
        QHeaderView::section {
            background:#151515;
            border:1px solid #2A2A2A;
            padding:6px;
            color:#BFBFBF;
        }
        """

    # light theme
    def light(self):
        return """
        QWidget { background:#F5F5F5; color:#111; }
        QFrame#Header {
            background:#FFFFFF;
            border-bottom:1px solid #DDD;
        }
        QPushButton {
            background:#FFFFFF;
            border:1px solid #CCC;
            padding:8px;
            border-radius:8px;
        }
        QPushButton:hover {
            background:#F0F0F0;
        }
        QTableWidget {
            background:#FFFFFF;
            border:1px solid #D0D0D0;
            gridline-color:#CFCFCF;
        }
        QTableWidget::item {
            border-right:1px solid #E0E0E0;
            border-bottom:1px solid #E0E0E0;
            padding:4px;
        }
        QTableWidget::item:selected {
            background:#DADADA;
        }
        QHeaderView::section {
            background:#F2F2F2;
            border:1px solid #D0D0D0;
            padding:6px;
        }
        """

    # open main workspace
    def open_workspace(self):
        self.stack.setCurrentIndex(1)


# run app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileApp()
    window.show()
    sys.exit(app.exec())
