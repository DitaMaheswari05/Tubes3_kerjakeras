from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout

class InfoWindow(QDialog):
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(self)
        text = QTextEdit()
        text.setReadOnly(True)
        if isinstance(content, dict):
            formatted = ""
            for section in ["skills", "job", "education"]:
                items = content.get(section, [])
                if items:
                    formatted += f"{section.capitalize()}:\n"
                    formatted += "\n".join(f"• {item}" for item in items)
                    formatted += "\n\n"
            text.setPlainText(formatted.strip())
        else:
            text.setPlainText(str(content))
        layout.addWidget(text)