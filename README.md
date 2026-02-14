📘 VaaniRead – Offline Hands-Free AI Book Reader

VaaniRead is an offline, hands-free AI-powered book reader designed to improve accessibility for visually impaired users and enable hands-free reading for everyone.
It converts documents and images into speech and allows users to control reading using voice commands, all without internet access.

✨ Key Features

📄 Supports PDF, DOC, DOCX, TXT

📷 Reads physical books via camera images

✍️ Recognizes printed and handwritten text

🎤 Hands-free voice control (start, pause, resume, next, stop)

🔊 Offline Text-to-Speech

💾 Progress save & resume

🌍 Multilingual support

⚙️ Optimized for low-end devices

🔒 100% offline & privacy-preserving

🧠 How It Works

User provides an input (image or document)

Offline OCR extracts text

Text is cleaned and split into sentences

Sentences are stored locally

Voice commands control reading

Progress is saved automatically



🖥️ Installation (Linux)

    py -3.11 -m venv my1
    my1\Scripts\activate
    pip install --upgrade pip
    pip install PyAudio
    pip install pytesseract
    pip install opencv-python
    pip install pdfplumber
    pip install python-docx
    pip install langdetect
    pip install psutil
    pip install vosk
    pip install mediapipe==0.10.9
    pip install PyAutoGUI


This installs:

OCR tools

Audio & speech dependencies

Required Python libraries



▶️ Running the Application

        python main.py


The application starts listening for voice commands.

🎙️ Supported Voice Commands
Command	Action
start	Begin reading
pause	Pause reading
resume	Resume reading
next	Skip to next sentence
stop	Stop and save progress
exit	Exit the application
💾 Progress Save & Resume

Reading position is saved automatically

On restart, the app resumes from the last sentence

Progress is stored locally

🔐 Offline & Privacy

No internet connection required

No data sent to external servers

All processing is done locally on the device

⚙️ Device Compatibility

Low-end laptops

Raspberry Pi

Standard desktops

Works without GPU

🎯 Use Cases

Visually impaired users

Hands-free reading

Offline learning environments

Low-connectivity regions

Assistive technology demonstrations

📦 Dependencies

All Python dependencies are listed in requirements.txt.
System dependencies are installed via setup.sh.

📄 License

This project uses open-source libraries and is intended for educational and assistive purposes.

⭐ Final Note

VaaniRead demonstrates how offline AI can be used responsibly to improve accessibility, privacy, and inclusivity.
