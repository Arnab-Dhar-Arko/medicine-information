import pytesseract
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget, QTextEdit
from gtts import gTTS
import sqlite3
import os
from pydub import AudioSegment
from pydub.playback import play

# Manually set the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set the path to ffmpeg directly in your code
ffmpeg_path = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
AudioSegment.converter = ffmpeg_path  # Corrected attribute name

# Database query for medicine information
def get_medicine_info(medicine_name):
    try:
        conn = sqlite3.connect("medicine.db")
        cursor = conn.cursor()
        cursor.execute("SELECT info FROM medicines WHERE name LIKE ?", (f"%{medicine_name}%",))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "No information available for this medicine."
    except sqlite3.Error as e:
        return f"Database error: {e}"

# Extract text from image
def extract_text(image_path):
    try:
        return pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        return f"Error extracting text: {e}"

# Generate text-to-speech and play the audio
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang="en")
        audio_file = "medicine_info.mp3"
        tts.save(audio_file)
        
        # Using pydub to play the audio
        sound = AudioSegment.from_mp3(audio_file)
        play(sound)
        os.remove(audio_file)  # Clean up the temporary file
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

# Main App Class
class MedicineApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Medicine Info App")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.label = QLabel("Upload an image of a medicine label or document")
        self.layout.addWidget(self.label)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.layout.addWidget(self.result)

        self.upload_btn = QPushButton("Select Image")
        self.upload_btn.clicked.connect(self.open_image)
        self.layout.addWidget(self.upload_btn)

        self.setLayout(self.layout)

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)", options=options
        )
        
        if file_path:
            extracted_text = extract_text(file_path)
            self.result.setText(f"Extracted Text:\n{extracted_text}")

            # Get the first line as medicine name
            medicine_name = extracted_text.split("\n")[0].strip()
            if medicine_name:
                info = get_medicine_info(medicine_name)
                self.result.append(f"\nMedicine Info:\n{info}")
                text_to_speech(info)
            else:
                self.result.append("\nNo valid text detected for medicine name.")

# Run the app
if __name__ == "__main__":
    app = QApplication([])
    window = MedicineApp()
    window.show()
    app.exec_()
