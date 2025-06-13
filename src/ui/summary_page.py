from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QWidget, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SkillTag(QLabel):
    def __init__(self, skill_text):
        super().__init__(skill_text)
        self.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                margin: 5px;
            }
        """)
        self.setAlignment(Qt.AlignCenter)

class InfoCard(QFrame):
    def __init__(self, title, content):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.95), stop:1 rgba(240,147,251,0.1));
                border: 2px solid rgba(102, 126, 234, 0.2);
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #4c51bf; margin-bottom: 10px;")
        
        # Content
        content_label = QLabel(content)
        content_label.setFont(QFont("Segoe UI", 13))
        content_label.setStyleSheet("color: #553c9a; line-height: 1.4;")
        content_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(content_label)
        
        self.setLayout(layout)

class CVSummaryPage(QDialog):
    def __init__(self, cv_data=None):
        super().__init__()
        self.cv_data = cv_data
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('CV Summary')
        self.setGeometry(150, 150, 1000, 800)
        self.setModal(True)
        
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.3 #764ba2, stop:0.7 #f093fb, stop:1 #f5576c);
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title_label = QLabel('CV Summary')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                margin: 20px 0 40px 0;
                background: transparent;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                padding: 15px;
                border-radius: 15px;
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
            }
        """)
        
        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
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
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(25)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Personal Information Card
        personal_info_card = self.create_personal_info_card()
        content_layout.addWidget(personal_info_card)
        
        # Skills Section
        skills_section = self.create_skills_section()
        content_layout.addWidget(skills_section)
        
        # Job History Section
        job_history_section = self.create_job_history_section()
        content_layout.addWidget(job_history_section)
        
        # Education Section
        education_section = self.create_education_section()
        content_layout.addWidget(education_section)
        
        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        
        # Close button
        button_layout = QHBoxLayout()
        
        close_btn = QPushButton("❌ Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6b7280, stop:1 #4b5563);
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
                    stop:0 #4b5563, stop:1 #374151);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(107, 114, 128, 0.4);
            }
            QPushButton:pressed {
                transform: translateY(0px);
            }
        """)
        close_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        main_layout.addWidget(title_label)
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def create_personal_info_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.95), stop:1 rgba(240,147,251,0.1));
                border: 2px solid rgba(102, 126, 234, 0.2);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(15px);
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Name header
        name_label = QLabel(f"👤 {self.cv_data['name']}")
        name_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        name_label.setStyleSheet("""
            color: #4c51bf;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            padding: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
            border-radius: 10px;
        """)
        
        # Personal details grid
        details_layout = QGridLayout()
        details_layout.setSpacing(15)
        
        # Birthdate
        birthdate_label = QLabel("🎂 Birthdate:")
        birthdate_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        birthdate_label.setStyleSheet("color: #553c9a;")
        
        birthdate_value = QLabel(self.cv_data['birthdate'])
        birthdate_value.setFont(QFont("Segoe UI", 14))
        birthdate_value.setStyleSheet("color: #7c3aed;")
        
        # Address
        address_label = QLabel("🏠 Address:")
        address_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        address_label.setStyleSheet("color: #553c9a;")
        
        address_value = QLabel(self.cv_data['address'])
        address_value.setFont(QFont("Segoe UI", 14))
        address_value.setStyleSheet("color: #7c3aed;")
        
        # Phone
        phone_label = QLabel("📱 Phone:")
        phone_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        phone_label.setStyleSheet("color: #553c9a;")
        
        phone_value = QLabel(self.cv_data['phone'])
        phone_value.setFont(QFont("Segoe UI", 14))
        phone_value.setStyleSheet("color: #7c3aed;")
        
        details_layout.addWidget(birthdate_label, 0, 0)
        details_layout.addWidget(birthdate_value, 0, 1)
        details_layout.addWidget(address_label, 1, 0)
        details_layout.addWidget(address_value, 1, 1)
        details_layout.addWidget(phone_label, 2, 0)
        details_layout.addWidget(phone_value, 2, 1)
        
        layout.addWidget(name_label)
        layout.addLayout(details_layout)
        
        card.setLayout(layout)
        return card
    
    def create_skills_section(self):
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.95), stop:1 rgba(240,147,251,0.1));
                border: 2px solid rgba(102, 126, 234, 0.2);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(15px);
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Section title
        title_label = QLabel("💼 Skills:")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("""
            color: #4c51bf;
            margin-bottom: 15px;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
            border-radius: 10px;
        """)
        
        # Skills tags container
        skills_container = QWidget()
        skills_layout = QHBoxLayout()
        skills_layout.setSpacing(10)
        
        for skill in self.cv_data['skills']:
            skill_tag = SkillTag(skill)
            skills_layout.addWidget(skill_tag)
        
        skills_layout.addStretch()
        skills_container.setLayout(skills_layout)
        
        layout.addWidget(title_label)
        layout.addWidget(skills_container)
        
        section.setLayout(layout)
        return section
    
    def create_job_history_section(self):
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.95), stop:1 rgba(240,147,251,0.1));
                border: 2px solid rgba(102, 126, 234, 0.2);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(15px);
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Section title
        title_label = QLabel("💼 Job History:")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("""
            color: #4c51bf;
            margin-bottom: 15px;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
            border-radius: 10px;
        """)
        
        # Job entries
        for job in self.cv_data['job_history']:
            job_card = QFrame()
            job_card.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
                    border: 2px solid rgba(102, 126, 234, 0.2);
                    border-radius: 15px;
                    padding: 20px;
                    margin: 5px 0;
                }
            """)
            
            job_layout = QVBoxLayout()
            job_layout.setSpacing(8)
            
            # Position
            position_label = QLabel(job['position'])
            position_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
            position_label.setStyleSheet("color: #4c51bf;")
            
            # Period
            period_label = QLabel(job['period'])
            period_label.setFont(QFont("Segoe UI", 12))
            period_label.setStyleSheet("color: #7c3aed; font-weight: 500;")
            
            # Description
            desc_label = QLabel(job['description'])
            desc_label.setFont(QFont("Segoe UI", 13))
            desc_label.setStyleSheet("color: #553c9a; margin-top: 5px;")
            desc_label.setWordWrap(True)
            
            job_layout.addWidget(position_label)
            job_layout.addWidget(period_label)
            job_layout.addWidget(desc_label)
            
            job_card.setLayout(job_layout)
            layout.addWidget(job_card)
        
        layout.addWidget(title_label)
        
        section.setLayout(layout)
        return section
    
    def create_education_section(self):
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.95), stop:1 rgba(240,147,251,0.1));
                border: 2px solid rgba(102, 126, 234, 0.2);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(15px);
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Section title
        title_label = QLabel("🎓 Education:")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("""
            color: #4c51bf;
            margin-bottom: 15px;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
            border-radius: 10px;
        """)
        
        # Education entries
        for edu in self.cv_data['education']:
            edu_card = QFrame()
            edu_card.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
                    border: 2px solid rgba(102, 126, 234, 0.2);
                    border-radius: 15px;
                    padding: 20px;
                    margin: 5px 0;
                }
            """)
            
            edu_layout = QVBoxLayout()
            edu_layout.setSpacing(8)
            
            # Degree and Institution
            degree_text = f"{edu['degree']} ({edu['institution']})"
            degree_label = QLabel(degree_text)
            degree_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
            degree_label.setStyleSheet("color: #4c51bf;")
            degree_label.setWordWrap(True)
            
            # Period
            period_label = QLabel(edu['period'])
            period_label.setFont(QFont("Segoe UI", 12))
            period_label.setStyleSheet("color: #7c3aed; font-weight: 500;")
            
            edu_layout.addWidget(degree_label)
            edu_layout.addWidget(period_label)
            
            edu_card.setLayout(edu_layout)
            layout.addWidget(edu_card)
        
        layout.addWidget(title_label)
        
        section.setLayout(layout)
        return section