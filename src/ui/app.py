import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from ui.search_panel import SearchPanel
from ui.result_panel import ResultPanel
from ui.detail_viewer import DetailViewer
from ui.summary_page import CVSummaryPage
from SearchEngine.SearchEngine import SearchEngine
from extraction.extractor import extract_cv_summary
from database.db import get_applicant_profile_by_cv_path
from pathlib import Path

class ApplicantTrackingSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        SearchEngine.Initialize()
        self.detail_viewer = None
        self.summary_dialog = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Applicant Tracking System')
        self.setGeometry(100, 100, 1400, 900)
        
        # Set application style with blue-purple gradient
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.3 #764ba2, stop:0.7 #f093fb, stop:1 #f5576c);
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Enhanced title with gradient text effect
        title = QLabel('Applicant Tracking System')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: white;
                margin: 25px 0 50px 0;
                background: transparent;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                padding: 20px;
                border-radius: 20px;
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
            }
        """)
        
        # Content layout with glass morphism effect
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        
        # Create scrollable left panel
        left_scroll_area = QScrollArea()
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        left_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        left_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
                border-radius: 15px;
            }
            QScrollBar:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255,255,255,0.2), stop:1 rgba(240,147,251,0.2));
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255,255,255,0.8), stop:1 rgba(240,147,251,0.8));
                border-radius: 5px;
                min-height: 20px;
                margin: 1px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255,255,255,0.9), stop:1 rgba(240,147,251,0.9));
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)
        
        # Left side content widget
        left_content_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(25)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # Search panel
        self.search_panel = SearchPanel()
        self.search_panel.search_requested.connect(self.perform_search)
        left_layout.addWidget(self.search_panel)
        
        # Add some spacing at the bottom
        left_layout.addStretch()
        
        left_content_widget.setLayout(left_layout)
        left_scroll_area.setWidget(left_content_widget)
        
        # Set fixed width for left panel to ensure proper layout
        left_scroll_area.setFixedWidth(600)
        
        # Results panel
        self.result_panel = ResultPanel()
        self.result_panel.cv_view_requested.connect(self.show_cv_detail)
        self.result_panel.cv_summary_requested.connect(self.show_cv_summary)
        
        content_layout.addWidget(left_scroll_area)
        content_layout.addWidget(self.result_panel, 1)
        
        main_layout.addWidget(title)
        main_layout.addLayout(content_layout)
        
        central_widget.setLayout(main_layout)
    def perform_search(self, search_params):
        keywords = search_params.get('keywords', '').split()
        algorithm = search_params.get('algorithm', 'KMP')
        max_results = search_params.get('max_results', 10)

        results = SearchEngine.SearchExact(keywords, algorithm if algorithm != "Aho-Corasick" else "AC", max_results)
        cv_list = []

        for path, match_count in results:
            raw_text = SearchEngine._preprocessed[path]
            extracted = extract_cv_summary(raw_text)

            profile = get_applicant_profile_by_cv_path(str(path.resolve()))

            if profile:
                full_name = f"{profile['first_name']} {profile['last_name']}"
                birthdate = str(profile['date_of_birth'])
                address = profile['address']
                phone = profile['phone_number']
            else:
                first_line = raw_text.strip().split('\n', 1)[0]
                full_name = first_line if len(first_line.split()) <= 5 else path.stem
                birthdate = "Unknown"
                address = "Unknown"
                phone = "Unknown"

            cv_list.append({
                'name': full_name,
                'matches': match_count,
                'skills': ', '.join(extracted.get('skills', [])),
                'experience': f"{len(extracted.get('job', []))} jobs",
                'birthdate': birthdate,
                'address': address,
                'phone': phone,
                'job_history': [],
                'education': []
            })

        self.result_panel.update_results(cv_list)
        
    def handle_file_upload(self, file_paths):
        print(f"Files uploaded: {file_paths}")
        self.result_panel.refresh_results()
        
    def show_cv_detail(self, cv_data):
        if not self.detail_viewer:
            self.detail_viewer = DetailViewer()
        
        self.detail_viewer.load_cv_data(cv_data)
        self.detail_viewer.show()
    
    def show_cv_summary(self, cv_data):
        # Create new summary dialog each time to ensure fresh data
        self.summary_dialog = CVSummaryPage(cv_data)
        self.summary_dialog.show()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set enhanced color palette with blue-purple theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(102, 126, 234))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(118, 75, 162))
    palette.setColor(QPalette.AlternateBase, QColor(240, 147, 251))
    app.setPalette(palette)
    
    window = ApplicantTrackingSystem()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()