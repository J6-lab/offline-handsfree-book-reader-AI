import subprocess
import threading
import time
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# ===================== FILES =====================
TEXT_FILE = "sentences.txt"
PROGRESS_FILE = "progress.txt"

# ===================== FLAGS & STATE =====================
stop_flag = False
pause_flag = False
next_flag = False

reader_thread = None
current_line_index = 0
lines = []

# ===================== LOAD SENTENCES =====================
with open(TEXT_FILE, "r", encoding="utf-8") as f:
    lines = [line.strip().replace('"', '') for line in f if line.strip()]

# ===================== LOAD PROGRESS =====================
if os.path.exists(PROGRESS_FILE):
    try:
        with open(PROGRESS_FILE, "r") as f:
            current_line_index = int(f.read().strip())
    except:
        current_line_index = 0
else:
    current_line_index = 0

# ===================== SAVE PROGRESS =====================
def save_progress():
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(current_line_index))

# ===================== SPEECH FUNCTION =====================
def speak_line(text):
    command = f'''
    Add-Type -AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.Speak("{text}");
    '''
    subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True
    )

# ===================== NUMBER EXTRACTION =====================
def extract_number(text):
    words_to_numbers = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
        "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
        "nineteen": 19, "twenty": 20
    }

    for word, num in words_to_numbers.items():
        if word in text:
            return num

    for token in text.split():
        if token.isdigit():
            return int(token)

    return None

# ===================== READER THREAD =====================
def reader():
    global stop_flag, pause_flag, next_flag, current_line_index

    print(f"\n📖 Reading from sentence {current_line_index + 1}/{len(lines)}")

    while current_line_index < len(lines):

        if stop_flag:
            save_progress()
            print("⏹ Reader stopped.")
            return

        if pause_flag:
            time.sleep(0.1)
            continue

        text = lines[current_line_index]
        speak_line(text)

        current_line_index += 1
        save_progress()

        if next_flag:
            next_flag = False

    print("✅ Finished all sentences.")

# ===================== VOICE SETUP =====================
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()
stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=4096
)

stream.start_stream()

print("\n🎤 Voice Commands:")
print(" start | pause | resume | next | stop")
print(" restart | go to <number> | exit")
print(" Speak clearly...")

# ===================== VOICE COMMAND LOOP =====================
while True:
    data = stream.read(4096, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        cmd = result.get("text", "").lower().strip()

        if not cmd:
            continue

        print("🗣 Heard:", cmd)

        if "start" in cmd:
            if reader_thread is None or not reader_thread.is_alive():
                stop_flag = False
                pause_flag = False
                reader_thread = threading.Thread(target=reader)
                reader_thread.start()
            else:
                print("Already reading.")

        elif "pause" in cmd:
            pause_flag = True
            print("⏸ Paused.")

        elif "resume" in cmd:
            pause_flag = False
            print("▶ Resumed.")

        elif "next" in cmd:
            next_flag = True
            print("⏭ Next sentence.")

        elif "stop" in cmd:
            stop_flag = True
            pause_flag = False

        elif "restart" in cmd:
            stop_flag = True
            pause_flag = False
            current_line_index = 0
            save_progress()
            print("🔁 Restarted from beginning.")

        elif "go to" in cmd:
            number = extract_number(cmd)
            if number and 1 <= number <= len(lines):
                stop_flag = True
                pause_flag = False
                current_line_index = number - 1
                save_progress()
                print(f"➡ Jumped to sentence {number}.")
            else:
                print("❌ Invalid sentence number.")

        elif "exit" in cmd:
            stop_flag = True
            save_progress()
            print("👋 Exiting.")
            break
