from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QScrollArea, QWidget,
                             QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class DetailViewer(QDialog):
    def __init__(self):
        super().__init__()
        self.cv_data = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('CV Detail Viewer')
        self.setGeometry(200, 200, 900, 700)
        self.setModal(True)
        
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.3 #764ba2, stop:0.7 #f093fb, stop:1 #f5576c);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header with glass morphism effect
        header_frame = QFrame()
        header_frame.setStyleSheet("""
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
        
        header_layout = QHBoxLayout()
        
        # Profile section
        profile_layout = QVBoxLayout()
        
        self.name_label = QLabel("👤 CV Name")
        self.name_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.name_label.setStyleSheet("""
            color: #4c51bf;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        """)
        
        self.experience_label = QLabel("⏱️ Experience")
        self.experience_label.setFont(QFont("Segoe UI", 16))
        self.experience_label.setStyleSheet("""
            color: #7c3aed; 
            font-weight: 600;
            margin-top: 5px;
        """)
        
        profile_layout.addWidget(self.name_label)
        profile_layout.addWidget(self.experience_label)
        
        # Match info
        match_layout = QVBoxLayout()
        match_layout.setAlignment(Qt.AlignRight)
        
        self.match_label = QLabel("🎯 0 matches")
        self.match_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.match_label.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
            color: white;
            border-radius: 20px;
            padding: 15px 25px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        """)
        self.match_label.setAlignment(Qt.AlignCenter)
        
        match_layout.addWidget(self.match_label)
        
        header_layout.addLayout(profile_layout)
        header_layout.addStretch()
        header_layout.addLayout(match_layout)
        
        header_frame.setLayout(header_layout)
        
        # Content area with enhanced styling
        content_frame = QFrame()
        content_frame.setStyleSheet("""
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
        
        content_layout = QGridLayout()
        content_layout.setSpacing(25)
        
        # Skills section
        skills_label = QLabel("💼 Skills & Technologies")
        skills_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        skills_label.setStyleSheet("color: #4c51bf;")
        
        self.skills_text = QLabel("Skills will be displayed here")
        self.skills_text.setFont(QFont("Segoe UI", 13))
        self.skills_text.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
            padding: 15px;
            border-radius: 12px;
            color: #553c9a;
            border: 2px solid rgba(102, 126, 234, 0.2);
        """)
        self.skills_text.setWordWrap(True)
        
        # Contact section
        contact_label = QLabel("📞 Contact Information")
        contact_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        contact_label.setStyleSheet("color: #4c51bf;")
        
        self.contact_text = QLabel("Contact info will be displayed here")
        self.contact_text.setFont(QFont("Segoe UI", 13))
        self.contact_text.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(102, 126, 234, 0.1), stop:1 rgba(240, 147, 251, 0.1));
            padding: 15px;
            border-radius: 12px;
            color: #553c9a;
            border: 2px solid rgba(102, 126, 234, 0.2);
        """)
        
        # Summary section
        summary_label = QLabel("📝 Professional Summary")
        summary_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        summary_label.setStyleSheet("color: #4c51bf;")
        
        self.summary_text = QTextEdit()
        self.summary_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 12px;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.9), stop:1 rgba(240,147,251,0.05));
                font-size: 13px;
                color: #4c51bf;
            }
            QTextEdit:focus {
                border-color: #667eea;
                box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
            }
        """)
        self.summary_text.setMaximumHeight(180)
        self.summary_text.setPlainText("Professional summary will be displayed here...")
        
        # Add to grid
        content_layout.addWidget(skills_label, 0, 0)
        content_layout.addWidget(self.skills_text, 1, 0)
        content_layout.addWidget(contact_label, 0, 1)
        content_layout.addWidget(self.contact_text, 1, 1)
        content_layout.addWidget(summary_label, 2, 0, 1, 2)
        content_layout.addWidget(self.summary_text, 3, 0, 1, 2)
        
        content_frame.setLayout(content_layout)
        
        # Enhanced buttons
        button_layout = QHBoxLayout()
        
        download_btn = QPushButton("📥 Download CV")
        download_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #10b981, stop:0.5 #059669, stop:1 #047857);
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
                    stop:0 #059669, stop:0.5 #047857, stop:1 #065f46);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
            }
            QPushButton:pressed {
                transform: translateY(0px);
            }
        """)
        
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
        
        button_layout.addWidget(download_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addWidget(header_frame)
        layout.addWidget(content_frame)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_cv_data(self, cv_data):
        """Load CV data into the viewer"""
        self.cv_data = cv_data
        
        self.name_label.setText(f"👤 {cv_data.get('name', 'Unknown')}")
        self.experience_label.setText(f"⏱️ {cv_data.get('experience', 'N/A')} experience")
        self.match_label.setText(f"🎯 {cv_data.get('matches', 0)} matches")
        self.skills_text.setText(f"💼 {cv_data.get('skills', 'No skills listed')}")
        
        # Generate sample summary and contact info
        summary = f"Experienced professional with {cv_data.get('experience', 'several years')} in the field. Skilled in {cv_data.get('skills', 'various technologies')}. Proven track record of delivering high-quality solutions and working effectively in team environments."
        self.summary_text.setPlainText(summary)
        
        contact = f"📧 Email: {cv_data.get('name', 'unknown').lower().replace(' ', '.')}@email.com\n📱 Phone: +1 (555) 123-4567\n📍 Location: City, State"
        self.contact_text.setText(contact)