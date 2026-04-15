import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFileDialog,
    QTableWidget, QHBoxLayout, QHeaderView, QScrollArea,
    QFrame, QTableWidgetItem, QMenu
)
from PyQt6.QtCore import Qt
from Backend.DataHandler import DataHandler

class FileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CalDS")
        self.resize(1200, 800)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.table_list = []
        self.active_table = None
        self.theme_mode = "dark"
        self.make_menu()
        self.make_workspace()
        self.apply_theme()

    # ── Menu screen ────────────────────────────────────────────────────────────
    def make_menu(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("CalDS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 100px; font-weight: bold;")

        subtitle = QLabel("Calculator for Data and Statistic System")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color:#888; font-size:16px;")

        btn_new = QPushButton("Create New File")
        btn_new.setFixedSize(200, 50)
        btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_new.clicked.connect(self.go_to_tables)

        btn_import = QPushButton("Import File")
        btn_import.setFixedSize(200, 50)
        btn_import.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_import.clicked.connect(self.handle_import)

        btn_exit = QPushButton("Exit")
        btn_exit.setFixedSize(100, 30)
        btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exit.clicked.connect(QApplication.instance().quit)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_import)
        btn_row.addWidget(btn_new)
        btn_row.addStretch()

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(btn_row)
        layout.addSpacing(10)
        layout.addWidget(btn_exit, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.stack.addWidget(page)

    # ── Workspace screen ───────────────────────────────────────────────────────
    def make_workspace(self):
        page = QWidget()
        main = QVBoxLayout(page)
        self.stack.addWidget(page)

        # Header bar
        header = QFrame()
        header.setObjectName("Header")
        header.setFixedHeight(50)
        h = QHBoxLayout(header)
        h.setContentsMargins(12, 0, 12, 0)
        lbl_title = QLabel("CalDS Dashboard")
        lbl_title.setStyleSheet("font-weight: bold; font-size: 15px;")
        self.status = QLabel("System ready")
        h.addWidget(lbl_title)
        h.addStretch()
        h.addWidget(self.status)
        main.addWidget(header)

        # Toolbar
        row = QHBoxLayout()
        self.add_btn = QPushButton("Add Table (Max 3)")
        btn_remove   = QPushButton("Remove")
        btn_clear    = QPushButton("Clear")
        btn_formula  = QPushButton("Formula")
        btn_export   = QPushButton("Export CSV")
        btn_import   = QPushButton("Import CSV")
        btn_theme    = QPushButton("Theme")
        btn_back     = QPushButton("Back")

        self.add_btn.clicked.connect(self.add_new_table)
        btn_remove.clicked.connect(self.remove_table)
        btn_clear.clicked.connect(self.clear_table)
        btn_formula.clicked.connect(lambda: self.show_formula_menu(btn_formula))
        btn_export.clicked.connect(self.export_csv)
        btn_import.clicked.connect(self.handle_import)
        btn_theme.clicked.connect(self.switch_theme)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        for b in [self.add_btn, btn_remove, btn_clear, btn_formula,
                  btn_export, btn_import, btn_theme, btn_back]:
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            row.addWidget(b)
        row.addStretch()

        main.addLayout(row)

        # Result display
        self.result_display = QLabel("Add a table and enter data to begin.")
        self.result_display.setWordWrap(True)
        self.result_display.setObjectName("ResultDisplay")
        main.addWidget(self.result_display)

        # Scrollable table area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.tables_layout = QHBoxLayout(self.scroll_content)
        scroll.setWidget(self.scroll_content)
        main.addWidget(scroll)

    # ── IntegratedTable ────────────────────────────────────────────────────────
    class IntegratedTable(QTableWidget):
        def __init__(self, label):
            super().__init__(32, 1)
            self.setHorizontalHeaderLabels([label])
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.verticalHeader().setVisible(False)
            self.setMinimumSize(350, 480)
            self.itemChanged.connect(self.sync)
            self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.customContextMenuRequested.connect(self.show_cell_menu)

        def sync(self, item):
            try:
                text = item.text().strip()
                if text == "":
                    self.handler.mod_data(item.row(), 0)
                else:
                    self.handler.mod_data(item.row(), float(text))
            except (ValueError, AttributeError):
                pass

        def show_cell_menu(self, pos):
            item = self.itemAt(pos)
            if item is None:
                return
            menu = QMenu(self)
            delete_action = menu.addAction("Clear Cell")
            action = menu.exec(self.viewport().mapToGlobal(pos))
            if action == delete_action:
                self.itemChanged.disconnect(self.sync)
                item.setText("")
                self.handler.mod_data(item.row(), 0)
                self.itemChanged.connect(self.sync)

    # ── Table management ───────────────────────────────────────────────────────

    def add_new_table(self):
        if len(self.table_list) >= 3:
            return
        label = ["Data X", "Data Y", "Data Z"][len(self.table_list)]
        t = self.IntegratedTable(label)
        t.handler = DataHandler(label)
        t.itemClicked.connect(lambda: self.select_table(t))
        self.table_list.append(t)
        self.tables_layout.addWidget(t)
        self.select_table(t)
        if len(self.table_list) == 3:
            self.add_btn.setEnabled(False)
        self.status.setText(f"Table created ({len(self.table_list)} total)")

    def select_table(self, table):
        self.active_table = table
        self.status.setText("Table selected")

    def remove_table(self):
        #error handling for no tables
        if not self.table_list:
            return

        table = self.active_table or self.table_list[-1]
        self.tables_layout.removeWidget(table)
        table.deleteLater()
        self.table_list.remove(table)
        self.active_table = self.table_list[-1] if self.table_list else None
        self.add_btn.setEnabled(True)
        self.status.setText(f"Table removed ({len(self.table_list)} remaining)")

    def clear_table(self):
        if self.active_table:
            self.active_table.clearContents()
            label = self.active_table.horizontalHeaderItem(0).text()
            self.active_table.handler = DataHandler(label)
            self.status.setText("Table cleared")

    # ── CSV import / export ────────────────────────────────────────────────────
    def handle_import(self):
        file, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV Files (*.csv);;All Files (*)")
        if not file:
            return
        self.go_to_tables()
        errors = []
        for table in self.table_list:
            try:
                # Uses DataHandler.import_data — matches column by data name
                table.handler.import_data(file)
                data = table.handler.get_data()
                table.itemChanged.disconnect(table.sync)
                for row, val in enumerate(data):
                    table.setItem(row, 0, QTableWidgetItem(str(val)))
                table.itemChanged.connect(table.sync)
            except KeyError:
                errors.append(f"Column '{table.handler.get_data_name()}' not found in CSV.")
            except Exception as e:
                errors.append(str(e))
        if errors:
            self.result_display.setText("Import issues:\n" + "\n".join(errors))
            self.status.setText("Import finished with errors")
        else:
            self.result_display.setText("CSV imported successfully.")
            self.status.setText("CSV imported")

    def export_csv(self):
        if not self.table_list:#check no tables
            self.result_display.setText("No tables to export.")
            return
        file, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV (*.csv)")
        if not file:
            return
        try:
            primary = self.table_list[0].handler
            # Pass remaining tables as other_datas if they exist
            others = tuple(t.handler for t in self.table_list[1:]) or None
            primary.export_data(file, other_datas=others)
            self.status.setText("CSV exported successfully")
            self.result_display.setText("CSV exported successfully.")
        except Exception as e:
            self.status.setText("Export failed")
            self.result_display.setText(f"Export error: {e}")

    # ── Formula menu ───────────────────────────────────────────────────────────
    def show_formula_menu(self, btn):
        if not self.table_list:
            self.result_display.setText("Invalid: No tables exist.")
            return

        menu = QMenu(self)
        h_x = self.table_list[0].handler

        def safe_exec(func, name):
            try:
                res = func()
                self.result_display.setText(f"{name}: {res:.4f}")
            except Exception:
                self.result_display.setText("Result: Invalid input / output")

        menu.addAction("Mean (Table X)",    lambda: safe_exec(h_x.mean, "Mean"))
        menu.addAction("Median (Table X)",  lambda: safe_exec(h_x.median, "Median"))
        menu.addAction("Mode (Table X)",    lambda: safe_exec(h_x.mode, "Mode"))
        menu.addAction("Std Dev (Table X)", lambda: safe_exec(lambda: h_x.sd(2), "SD"))

        if len(self.table_list) >= 2:
            h_y = self.table_list[1].handler
            menu.addAction("Mean (Table Y)",    lambda: safe_exec(h_y.mean, "Mean"))
            menu.addAction("Median (Table Y)",  lambda: safe_exec(h_y.median, "Median"))
            menu.addAction("Mode (Table Y)",    lambda: safe_exec(h_y.mode, "Mode"))
            menu.addAction("Std Dev (Table Y)", lambda: safe_exec(lambda: h_y.sd(2), "SD"))
            menu.addSeparator()
            data_y = self.table_list[1].handler.get_data()
            menu.addAction("Pearson R (X vs Y)",
                           lambda: safe_exec(lambda: h_x.pearson_r(data_y), "Pearson R"))

        menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

    # ── Navigation ─────────────────────────────────────────────────────────────
    def go_to_tables(self):
        if not self.table_list:
            self.add_new_table()
        self.stack.setCurrentIndex(1)

    # ── Theme ──────────────────────────────────────────────────────────────────
    def switch_theme(self):
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(self.dark() if self.theme_mode == "dark" else self.light())

    def dark(self):
        return """
        QWidget { background:#0B0B0B; color:#EAEAEA; }
        QFrame#Header {
            background:#121212;
            border-bottom:1px solid #222;
        }
        QLabel#ResultDisplay {
            color:#ff9f00;
            font-size:14px;
            padding:10px;
            background:#222;
            border-radius:5px;
        }
        QPushButton {
            background:#151515;
            border:1px solid #2A2A2A;
            padding:8px;
            border-radius:8px;
        }
        QPushButton:hover { background:#1C1C1C; }
        QPushButton:disabled { color:#555; }
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
        QTableWidget::item:selected { background:#2F2F2F; }
        QHeaderView::section {
            background:#151515;
            border:1px solid #2A2A2A;
            padding:6px;
            color:#BFBFBF;
        }
        QScrollArea { border:none; }
        """

    def light(self):
        return """
        QWidget { background:#F5F5F5; color:#111; }
        QFrame#Header {
            background:#FFFFFF;
            border-bottom:1px solid #DDD;
        }
        QLabel#ResultDisplay {
            color:#8a5700;
            font-size:14px;
            padding:10px;
            background:#FFF8EC;
            border-radius:5px;
        }
        QPushButton {
            background:#FFFFFF;
            border:1px solid #CCC;
            padding:8px;
            border-radius:8px;
        }
        QPushButton:hover { background:#F0F0F0; }
        QPushButton:disabled { color:#AAA; }
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
        QTableWidget::item:selected { background:#DADADA; }
        QHeaderView::section {
            background:#F2F2F2;
            border:1px solid #D0D0D0;
            padding:6px;
        }
        QScrollArea { border:none; }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileApp()
    window.show()
    sys.exit(app.exec())
