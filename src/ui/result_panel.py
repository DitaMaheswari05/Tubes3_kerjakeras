from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
import time

class CVCard(QFrame):
    view_requested = pyqtSignal(dict)
    summary_requested = pyqtSignal(dict)
    
    def __init__(self, cv_data):
        super().__init__()
        self.cv_data = cv_data
        self.initUI()
        
    def initUI(self):
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.95), stop:1 rgba(240,147,251,0.1));
                border: 2px solid rgba(102, 126, 234, 0.2);
                border-radius: 15px;
                margin: 10px;
                padding: 20px;
                backdrop-filter: blur(10px);
            }
            QFrame:hover {
                border: 2px solid rgba(102, 126, 234, 0.6);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,1), stop:1 rgba(240,147,251,0.2));
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
                transform: translateY(-2px);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Header with CV name and match count
        header_layout = QHBoxLayout()
        
        cv_label = QLabel(f"👤 {self.cv_data['name']}")
        cv_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        cv_label.setStyleSheet("color: #4c51bf;")
        
        match_label = QLabel(f"🎯 {self.cv_data['matches']} matches")
        match_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        match_label.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
            color: white;
            border-radius: 15px;
            padding: 8px 16px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        """)
        match_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(cv_label)
        header_layout.addStretch()
        header_layout.addWidget(match_label)
        
        # Skills with enhanced styling
        skills_label = QLabel(f"💼 {self.cv_data['skills']}")
        skills_label.setFont(QFont("Segoe UI", 12))
        skills_label.setStyleSheet("""
            color: #553c9a; 
            margin: 10px 0;
            padding: 10px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 8px;
            border-left: 4px solid #667eea;
        """)
        skills_label.setWordWrap(True)
        
        # Experience info
        exp_label = QLabel(f"⏱️ {self.cv_data.get('experience', 'N/A')} experience")
        exp_label.setFont(QFont("Segoe UI", 11))
        exp_label.setStyleSheet("color: #7c3aed; font-weight: 500;")
        
        # Buttons with enhanced styling
        button_layout = QHBoxLayout()
        
        summary_btn = QPushButton("📊 Summary")
        summary_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.9), stop:1 rgba(240,147,251,0.3));
                color: #4c51bf;
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,1), stop:1 rgba(240,147,251,0.5));
                border-color: rgba(102, 126, 234, 0.6);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
            }
        """)
        summary_btn.clicked.connect(self.emit_summary_request)
        
        view_cv_btn = QPushButton("👁️ View CV")
        view_cv_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5a6fd8, stop:0.5 #6a4190, stop:1 #e081e6);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                transform: translateY(0px);
            }
        """)
        view_cv_btn.clicked.connect(self.emit_view_request)
        
        button_layout.addWidget(summary_btn)
        button_layout.addWidget(view_cv_btn)
        button_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addWidget(skills_label)
        layout.addWidget(exp_label)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def emit_view_request(self):
        self.view_requested.emit(self.cv_data)
    
    def emit_summary_request(self):
        # Convert CV data to the format expected by CVSummaryPage
        summary_data = {
            'name': self.cv_data['name'],
            'birthdate': self.cv_data.get('birthdate', '01-01-1990'),
            'address': self.cv_data.get('address', 'Not specified'),
            'phone': self.cv_data.get('phone', 'Not provided'),
            'skills': self.cv_data['skills'].split(', ') if isinstance(self.cv_data['skills'], str) else self.cv_data.get('skills', []),
            'job_history': self.cv_data.get('job_history', [
                {
                    'position': 'Software Developer',
                    'period': '2020-2023',
                    'description': f"Working with {self.cv_data['skills']} technologies"
                }
            ]),
            'education': self.cv_data.get('education', [
                {
                    'degree': 'Computer Science',
                    'institution': 'University',
                    'period': '2016-2020'
                }
            ])
        }
        self.summary_requested.emit(summary_data)

class ResultPanel(QFrame):
    cv_view_requested = pyqtSignal(dict)
    cv_summary_requested = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.search_start_time = None  # Waktu mulai pencarian
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
        layout.setSpacing(20)
        
        # Results header with enhanced styling
        header_layout = QHBoxLayout()
        
        results_label = QLabel('📋 Search Results')
        results_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        results_label.setStyleSheet("""
            color: #4c51bf;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
            border-radius: 10px;
        """)
        
        self.stats_label = QLabel('🚀 Ready to search...')
        self.stats_label.setFont(QFont("Segoe UI", 13))
        self.stats_label.setStyleSheet("""
            color: #7c3aed; 
            font-weight: 600;
            padding: 8px 15px;
            background: rgba(124, 58, 237, 0.1);
            border-radius: 20px;
            border: 1px solid rgba(124, 58, 237, 0.2);
        """)
        
        header_layout.addWidget(results_label)
        header_layout.addStretch()
        header_layout.addWidget(self.stats_label)
        
        # Scroll area for results with enhanced styling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
                width: 15px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 6px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a6fd8, stop:1 #6a4190);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_layout.setSpacing(10)
        
        # Add initial sample results
        self.add_sample_results()
        
        self.results_widget.setLayout(self.results_layout)
        scroll_area.setWidget(self.results_widget)
        
        layout.addLayout(header_layout)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
    
    def add_sample_results(self):
        # Enhanced sample CVs with more detailed data
        sample_cvs = [
            {
                "name": "John Smith", 
                "matches": 8, 
                "skills": "React, HTML, CSS, JavaScript, Node.js", 
                "experience": "5 years",
                "birthdate": "15-03-1992",
                "address": "123 Tech Street, Silicon Valley, CA",
                "phone": "0812 1234 5678",
                "job_history": [
                    {
                        'position': 'Senior Frontend Developer',
                        'period': '2020-Present',
                        'description': "Leading frontend development team, implementing React applications with modern UI/UX practices"
                    },
                    {
                        'position': 'Frontend Developer',
                        'period': '2018-2020',
                        'description': "Developed responsive web applications using HTML, CSS, and JavaScript"
                    }
                ],
                "education": [
                    {
                        'degree': 'Computer Science',
                        'institution': 'Stanford University',
                        'period': '2014-2018'
                    }
                ]
            },
            {
                "name": "Sarah Johnson", 
                "matches": 6, 
                "skills": "Python, Django, PostgreSQL, Docker", 
                "experience": "3 years",
                "birthdate": "22-07-1995",
                "address": "456 Python Ave, New York, NY",
                "phone": "0813 2345 6789",
                "job_history": [
                    {
                        'position': 'Backend Developer',
                        'period': '2021-Present',
                        'description': "Developing scalable backend systems using Python and Django framework"
                    }
                ],
                "education": [
                    {
                        'degree': 'Software Engineering',
                        'institution': 'MIT',
                        'period': '2017-2021'
                    }
                ]
            },
            {
                "name": "Mike Chen", 
                "matches": 7, 
                "skills": "Java, Spring Boot, MySQL, AWS", 
                "experience": "4 years",
                "birthdate": "10-11-1993",
                "address": "789 Java Lane, Seattle, WA",
                "phone": "0814 3456 7890",
                "job_history": [
                    {
                        'position': 'Full Stack Java Developer',
                        'period': '2019-Present',
                        'description': "Building enterprise applications using Java Spring Boot and cloud technologies"
                    }
                ],
                "education": [
                    {
                        'degree': 'Computer Engineering',
                        'institution': 'University of Washington',
                        'period': '2015-2019'
                    }
                ]
            },
            {
                "name": "Emily Davis", 
                "matches": 5, 
                "skills": "React, TypeScript, GraphQL, MongoDB", 
                "experience": "2 years",
                "birthdate": "05-04-1997",
                "address": "321 GraphQL Street, Austin, TX",
                "phone": "0815 4567 8901",
                "job_history": [
                    {
                        'position': 'Junior Full Stack Developer',
                        'period': '2022-Present',
                        'description': "Working with modern web technologies including React, TypeScript, and GraphQL"
                    }
                ],
                "education": [
                    {
                        'degree': 'Information Technology',
                        'institution': 'University of Texas at Austin',
                        'period': '2019-2022'
                    }
                ]
            },
            {
                "name": "Alex Rodriguez", 
                "matches": 9, 
                "skills": "Full Stack, React, Node.js, Express, SQL", 
                "experience": "6 years",
                "birthdate": "18-09-1990",
                "address": "654 Full Stack Blvd, San Francisco, CA",
                "phone": "0816 5678 9012",
                "job_history": [
                    {
                        'position': 'Lead Full Stack Developer',
                        'period': '2018-Present',
                        'description': "Leading development of complete web applications from frontend to backend"
                    },
                    {
                        'position': 'Full Stack Developer',
                        'period': '2016-2018',
                        'description': "Developed end-to-end web solutions using modern JavaScript technologies"
                    }
                ],
                "education": [
                    {
                        'degree': 'Software Development',
                        'institution': 'UC Berkeley',
                        'period': '2012-2016'
                    }
                ]
            }
        ]
        
        for cv_data in sample_cvs:
            cv_card = CVCard(cv_data)
            cv_card.view_requested.connect(self.cv_view_requested.emit)
            cv_card.summary_requested.connect(self.cv_summary_requested.emit)
            self.results_layout.addWidget(cv_card)
        
        self.results_layout.addStretch()
    
    def perform_search(self, keywords, algorithm, max_results):
        # Catat waktu mulai pencarian
        self.search_start_time = time.time()
        
        self.stats_label.setText('🔍 Searching...')
        
        # Clear existing results
        self.clear_results()
        
        # Simulasi proses pencarian dengan delay yang bervariasi
        search_delay = self.calculate_search_delay(keywords, max_results)
        
        # Gunakan QTimer untuk menjalankan pencarian setelah delay
        QTimer.singleShot(search_delay, lambda: self.show_search_results(keywords, max_results))
    
    def calculate_search_delay(self, keywords, max_results):
        # Base delay minimal 50ms
        base_delay = 50
        
        # Tambah delay berdasarkan jumlah keyword (10ms per kata)
        keyword_count = len(keywords.split()) if keywords else 1
        keyword_delay = keyword_count * 10
        
        # Tambah delay berdasarkan jumlah hasil maksimal (1ms per 10 hasil)
        result_delay = max_results // 10
        
        # Total delay antara 50ms - 500ms
        total_delay = min(base_delay + keyword_delay + result_delay, 500)
        
        return total_delay
    
    def show_search_results(self, keywords, max_results):
        # Hitung waktu pencarian yang sebenarnya
        if self.search_start_time:
            elapsed_time = time.time() - self.search_start_time
            elapsed_ms = round(elapsed_time * 1000)  # Konversi ke milidetik
        else:
            elapsed_ms = 0
        
        # Tampilkan hasil dengan waktu pencarian realtime
        self.stats_label.setText(f'✅ {max_results} CVs found in {elapsed_ms}ms')
        
        # Tambahkan hasil pencarian
        self.add_sample_results()
    
    def clear_results(self):
        for i in reversed(range(self.results_layout.count())):
            child = self.results_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
    
    def refresh_results(self):
        # Catat waktu mulai refresh
        start_time = time.time()
        
        self.clear_results()
        self.add_sample_results()
        
        # Hitung waktu refresh
        elapsed_time = time.time() - start_time
        elapsed_ms = round(elapsed_time * 1000)
        
        self.stats_label.setText(f'🔄 Results refreshed in {elapsed_ms}ms')