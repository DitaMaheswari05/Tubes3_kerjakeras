from SearchEngine.SearchEngine import SearchEngine
from extraction.extractor import extract_cv_summary
from .InfoWindow import InfoWindow
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy,
    QLineEdit, QComboBox, QSpinBox, QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from pathlib import Path
import time

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimal ATS")
        self.setGeometry(100, 100, 1000, 700)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter keywords...")
        self.search_input.setMinimumHeight(36)
        self.search_input.textChanged.connect(self.perform_search)

        self.algorithm_dropdown = QComboBox()
        self.algorithm_dropdown.addItems(["Aho-Corasick", "Boyer-Moore", "KMP"])
        self.algorithm_dropdown.currentIndexChanged.connect(self.perform_search)

        self.result_limit = QSpinBox()
        self.result_limit.setRange(1, 100)
        self.result_limit.setValue(10)
        self.result_limit.valueChanged.connect(self.perform_search)

        self.maximum_fuzzy = QSpinBox()
        self.maximum_fuzzy.setRange(1, 10)
        self.maximum_fuzzy.setValue(2)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: gray; font-size: 13px;")

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.algorithm_dropdown)
        search_layout.addWidget(self.result_limit)
        search_layout.addWidget(self.maximum_fuzzy)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.results_container = QWidget()
        self.results_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.results_layout = QGridLayout(self.results_container)
        self.results_layout.setSpacing(20)
        self.results_layout.setContentsMargins(10, 10, 10, 10)

        for i in range(3):
            self.results_layout.setColumnStretch(i, 1)

        self.scroll_area.setWidget(self.results_container)

        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.scroll_area)

    def perform_search(self):
        # Clear existing widgets
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if self.search_input.text() == "":
            self.status_label.setText("")
            return

        # Extract input
        keywords = [kw.strip() for kw in self.search_input.text().split(',') if kw.strip()]
        algorithm = self.algorithm_dropdown.currentText()
        max_results = self.result_limit.value()

        algo_map = {
            "Aho-Corasick": "AC",
            "Boyer-Moore": "BM",
            "KMP": "KMP"
        }
        algo_code = algo_map.get(algorithm, "KMP")

        found = True
        start1 = time.perf_counter()
        results = SearchEngine.SearchExact(keywords, algo_code, max_results)
        end1 = time.perf_counter()
        if len(results) == 0:
            start2 = time.perf_counter()
            results_fuzzy = SearchEngine.SearchFuzzy(keywords, self.maximum_fuzzy.value(), max_results)
            end2 = time.perf_counter()
            found = False

        # Render cards
        if found:
            columns = 3
            for i, (path, score) in enumerate(results):
                row = i // columns
                col = i % columns
                card = self.create_result_card(
                    path,
                    f"Found: {score}",
                )
                card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                self.results_layout.addWidget(card, row, col)
            self.status_label.setText(f"Found {len(results)} results in {end1 - start1:.4f}s")
        else:
            columns = 3
            for i, (path, score) in enumerate(results_fuzzy):
                row = i // columns
                col = i % columns
                card = self.create_result_card(
                    path,
                    f"Found: {score}",
                )
                card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                self.results_layout.addWidget(card, row, col)
            self.status_label.setText(f"Found {len(results_fuzzy)} results in {end2 - start2:.4f}s after searching exact match in {end1-start1:.4f}s")

    def create_result_card(self, path, score):
        cv_id = path.stem
        card = QFrame()
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 12px;
                padding: 16px;
                border: 1px solid black;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                padding: 4px 12px;
                border-radius: 6px;
                background-color: #dcdcdc;
            }
            QPushButton:hover {
                background-color: #cccccc;
            }
        """)

        layout = QVBoxLayout(card)
        layout.addWidget(QLabel(f"<b>{cv_id}</b>"))
        layout.addWidget(QLabel(score))

        button_layout = QHBoxLayout()
        
        summary_btn = QPushButton("Summary")
        summary_btn.clicked.connect(lambda: self.show_info_window(f"Summary of {cv_id}", extract_cv_summary(SearchEngine._preprocessed[path])))

        view_btn = QPushButton("View")
        view_btn.clicked.connect(lambda _, p=path: QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(p).resolve()))))

        button_layout.addWidget(summary_btn)
        button_layout.addWidget(view_btn)
        
        layout.addLayout(button_layout)
        return card
    
    def show_info_window(self, title, content):
        window = InfoWindow(title, content, self)
        window.exec_()