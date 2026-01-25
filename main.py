import os

from identify_document import identify_document_type
from converter_document import img_to_text, pdf_to_text_pagewise, word_to_txt
from clean_txt import clean_and_save_text
from language_dection import detect_language
from sentence_segmentation import segment_and_save_sentences
from high_end_low_end_clasification import classify_device


# ---------------- Utility ----------------
def run_audio_reader():
    os.system("python store_and_speak.py")


def run_eye_tracking(file_path):
    cmd = f'python "{os.path.join(os.getcwd(), "eye_tracking_scroll.py")}" "{file_path}"'
    result = os.system(cmd)
    return result >> 8  # Windows exit code fix


def process_new_document():
    file_path = input("Enter document path: ").strip()

    doc_type = identify_document_type(file_path)
    print("📄 Document Type:", doc_type)

    if doc_type == "Image Document":
        img_to_text(file_path, "output.txt")

    elif doc_type == "PDF Document":
        pdf_to_text_pagewise(file_path, "output.txt")

    elif doc_type == "Word Document":
        word_to_txt(file_path, "output.txt")

    elif doc_type == "Text Document":
        os.system(f'copy "{file_path}" output.txt')

    else:
        print("❌ Unsupported document")
        return False

    raw_text = open("output.txt", "r", encoding="utf-8").read()
    clean_text = clean_and_save_text(raw_text, "cleaned_output.txt")

    lang = detect_language(clean_text)
    print("🌐 Language Detected:", lang)

    segment_and_save_sentences(clean_text, "sentences.txt")

    if os.path.exists("progress.txt"):
        os.remove("progress.txt")

    return True


# ================= MAIN MENU =================
while True:
    print("\n===================================")
    print("   HANDS-FREE DOCUMENT AI SYSTEM")
    print("===================================")
    print("Device Type:", classify_device())
    print("\n1. Hands-Free Audio Reader")
    print("2. Eye-Tracking Document Viewer")
    print("3. Exit")

    choice = input("Enter choice: ").strip()

    # ==================================================
    # OPTION 1 : AUDIO READER
    # ==================================================
    if choice == "1":
        print("\n🎧 Hands-Free Audio Reader")

        has_previous = os.path.exists("sentences.txt") and os.path.exists("progress.txt")

        if has_previous:
            print("\n1. Continue reading SAME document")
            print("2. Read a NEW document")
            sub_choice = input("Enter choice (1/2): ").strip()
        else:
            sub_choice = "2"

        # ---- Continue same document ----
        if sub_choice == "1" and has_previous:
            print("▶ Continuing previous document...")
            run_audio_reader()

        # ---- Read new document ----
        elif sub_choice == "2":
            print("\n📄 Processing new document...")
            success = process_new_document()
            if success:
                run_audio_reader()

        else:
            print("❌ Invalid choice")

    # ==================================================
    # OPTION 2 : EYE-TRACKING SCROLL
    # ==================================================
    elif choice == "2":
        print("\n👀 Eye-Tracking Document Viewer")

        file_path = input("Enter PDF or Word file path: ").strip()

        if not os.path.exists(file_path):
            print("❌ File not found")
            continue

        exit_code = run_eye_tracking(file_path)

        if exit_code == 2:
            print("🔁 Returned to main menu (Blink detected)")
            continue

        elif exit_code == 1:
            print("👋 Program terminated by eye gesture")
            break

    # ==================================================
    # EXIT
    # ==================================================
    elif choice == "3":
        print("👋 Exiting program")
        break

    else:
        print("❌ Invalid choice")
