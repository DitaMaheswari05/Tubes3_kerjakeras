import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QComboBox, QLabel, QListWidget, 
    QListWidgetItem, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import time

from SearchEngine.SearchEngine import SearchEngine 
from extraction.extractor import extract_cv_summary


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Search Engine!")
        self.setGeometry(200, 200, 500, 300)  
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: 'Segoe UI';
                font-size: 16px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: white;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: white;
            }
            QLabel {
                margin-top: 10px;
                font-weight: bold;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search...")
        self.search_input.textChanged.connect(self.on_search)

        # Dropdown
        self.dropdown = QComboBox()
        self.dropdown.addItems(["AC", "BM", "KMP"])

        # Label
        self.keywords = QLabel()
        self.result_list = QListWidget()
        self.result_list.itemClicked.connect(self.show_summary)


        layout.addWidget(QLabel("Search"))
        layout.addWidget(self.search_input)

        layout.addWidget(QLabel("Choose an Algorithm"))
        layout.addWidget(self.dropdown)

        layout.addWidget(self.keywords)
        
        layout.addWidget(QLabel("Results"))
        layout.addWidget(self.result_list)


        self.setLayout(layout)

    def on_search(self, text):
        keywords = [word.strip() for word in text.split(',') if word.strip()]
        algo_type = self.dropdown.currentText()

        if not keywords:
            self.keywords.setText("No keywords entered.")
            return

        try:
            t1 = time.perf_counter()
            results = SearchEngine.SearchExact(keywords, algo_type, max=5)
            t2 = time.perf_counter()
        except Exception as e:
            self.keywords.setText(f"Error during search: {str(e)}")
            return

        display_lines = [f"Keywords:\n" + "\n".join(f"• {kw}" for kw in keywords)]
        if results:
            display_lines.append(f"\nTop Results: [{t2-t1:.4f}s]")
            for path, score in results:
                display_lines.append(f"{str(path)} (score: {score})")
                item = QListWidgetItem(f"{str(path)} (score: {score})")
                item.setData(Qt.UserRole, path)
                self.result_list.addItem(item)
        else:
            display_lines.append("\nNo matching results found.")

        self.keywords.setText("\n".join(display_lines))

    def show_summary(self, item):
        path = item.data(Qt.UserRole)
        text = SearchEngine._preprocessed.get(path)
        if not text:
            QMessageBox.warning(self, "Error", "CV text not found.")
            return
        summary = extract_cv_summary(text)
        msg = ""
        msg += "Skills:\n- " + "\n- ".join(summary['skills']) + "\n\n"
        msg += "Job Titles:\n- " + "\n- ".join(summary['job']) + "\n\n"
        msg += "Education:\n- " + "\n- ".join(summary['education']) + "\n"
        QMessageBox.information(self, "CV Summary", msg)
