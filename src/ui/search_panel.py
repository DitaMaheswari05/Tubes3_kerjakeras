from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QLineEdit, 
                             QComboBox, QSpinBox, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class ModernButton(QPushButton):
    def __init__(self, text, primary=False):
        super().__init__(text)
        self.primary = primary
        self.setStyleSheet(self.get_style())
        self.setCursor(Qt.PointingHandCursor)
    
    def get_style(self):
        if self.primary:
            return """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                    color: white;
                    border: none;
                    border-radius: 15px;
                    padding: 15px 30px;
                    font-weight: bold;
                    font-size: 16px;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #5a6fd8, stop:0.5 #6a4190, stop:1 #e081e6);
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #4e5bc6, stop:0.5 #5e377e, stop:1 #d16fd1);
                    transform: translateY(0px);
                }
            """
        else:
            return """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255,255,255,0.9), stop:1 rgba(240,147,251,0.3));
                    color: #4c51bf;
                    border: 2px solid rgba(102, 126, 234, 0.3);
                    border-radius: 12px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255,255,255,1), stop:1 rgba(240,147,251,0.5));
                    border-color: rgba(102, 126, 234, 0.6);
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
                }
                QPushButton:pressed {
                    background: rgba(240,147,251,0.4);
                }
            """

class SearchPanel(QFrame):
    search_requested = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.95), stop:1 rgba(240,147,251,0.1));
                border-radius: 20px;
                padding: 30px;
                border: 2px solid rgba(102, 126, 234, 0.2);
                backdrop-filter: blur(15px);
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        
        # Panel title
        panel_title = QLabel('🔍 Search Parameters')
        panel_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        panel_title.setStyleSheet("""
            color: #4c51bf;
            margin-bottom: 15px;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
            border-radius: 10px;
        """)
        
        # Input keywords
        keywords_label = QLabel('Input Keywords')
        keywords_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        keywords_label.setStyleSheet("color: #553c9a; margin-bottom: 8px;")
        
        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText("Enter skills, technologies, or keywords...")
        self.keywords_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 12px;
                padding: 15px;
                font-size: 14px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.9), stop:1 rgba(240,147,251,0.1));
                color: #4c51bf;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background: rgba(255,255,255,0.95);
                box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
            }
            QLineEdit::placeholder {
                color: rgba(76, 81, 191, 0.6);
            }
        """)
        
        # Algorithm selection
        algo_label = QLabel('Choose Algorithm')
        algo_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        algo_label.setStyleSheet("color: #553c9a; margin-bottom: 8px;")
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(['KMP', 'BM','Fuzzy Matching'])
        self.algo_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 12px;
                padding: 15px;
                font-size: 14px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.9), stop:1 rgba(240,147,251,0.1));
                color: #4c51bf;
                font-weight: 500;
            }
            QComboBox:focus {
                border: 2px solid #667eea;
                background: rgba(255,255,255,0.95);
                box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
            }
            QComboBox::drop-down {
                border: none;
                width: 35px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
            }
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUiIGhlaWdodD0iMTUiIHZpZXdCb3g9IjAgMCAxNSAxNSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMuNSA2TDcuNSAxMEwxMS41IDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
            QComboBox QAbstractItemView {
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 10px;
                background: rgba(255,255,255,0.95);
                selection-background-color: rgba(102, 126, 234, 0.2);
                color: #4c51bf;
            }
        """)
        
        # Top matches
        matches_label = QLabel('Top Matches')
        matches_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        matches_label.setStyleSheet("color: #553c9a; margin-bottom: 8px;")
        
        self.matches_spin = QSpinBox()
        self.matches_spin.setRange(1, 50)
        self.matches_spin.setValue(10)
        self.matches_spin.setStyleSheet("""
            QSpinBox {
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 12px;
                padding: 15px;
                font-size: 14px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.9), stop:1 rgba(240,147,251,0.1));
                color: #4c51bf;
                font-weight: 500;
            }
            QSpinBox:focus {
                border: 2px solid #667eea;
                background: rgba(255,255,255,0.95);
                box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
                border-radius: 6px;
                width: 20px;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)
        
        # Search button
        search_btn = ModernButton('Search CVs', primary=True)
        search_btn.clicked.connect(self.emit_search_request)
        
        layout.addWidget(panel_title)
        layout.addWidget(keywords_label)
        layout.addWidget(self.keywords_input)
        layout.addWidget(algo_label)
        layout.addWidget(self.algo_combo)
        layout.addWidget(matches_label)
        layout.addWidget(self.matches_spin)
        layout.addStretch()
        layout.addWidget(search_btn)
        
        self.setLayout(layout)
    
    def emit_search_request(self):
        search_params = {
            'keywords': self.keywords_input.text(),
            'algorithm': self.algo_combo.currentText(),
            'max_results': self.matches_spin.value()
        }
        self.search_requested.emit(search_params)