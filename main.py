import sys
import os
import psutil
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow
from PyQt6.QtCore import Qt, QTimer

class GUISensors(QMainWindow):
    def __init__(self, file_path=None):
        super().__init__()
        self.setWindowTitle("GUI Sensors")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_monitor)
        self.timer.start(1000)

    def update_monitor(self):
        usage = psutil.cpu_percent(interval=1)
        status_text = f"Current CPU usage: {usage}%\n\n"
        if os.name == 'posix':  # Linux/Unix
            try:
                temp_output = os.popen("sensors").read()
                temp = None
                for line in temp_output.split('\n'):
                    if 'Tdie' in line or 'Package id 0:' in line:
                        temp = line.split()[-2].strip('+°C')
                        break
                if temp:
                    status_text += f"{temp_output}"
                else:
                    status_text += f"{temp_output}"
            except Exception as e:
                status_text += f"\nFailed to get temperature: {e}"
        
        self.label.setText(status_text)
        self.label.adjustSize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUISensors()
    window.show()
    sys.exit(app.exec())

