# JARVIS Lite - Offline Assistant with Text + Voice
# Save this file as jarvis.py and run with: python jarvis.py

import datetime
import os
import webbrowser
import random

# ---------- OPTIONAL VOICE LIBRARIES ----------
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


# ---------- TEXT TO SPEECH ----------
if TTS_AVAILABLE:
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)   # speaking speed
    # You can customize voice if you want:
    # voices = engine.getProperty("voices")
    # engine.setProperty("voice", voices[1].id)  # try female/male
else:
    engine = None

def speak(text):
    """Print to screen and speak using TTS if available."""
    print(f"\nJARVIS: {text}")
    if TTS_AVAILABLE and engine is not None:
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            # If any issue with audio, just ignore and continue
            pass


# ---------- BASIC UTILITIES ----------
def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.datetime.now().strftime("%d %B %Y")

def google_search(query):
    if query.strip() == "":
        speak("Please tell me what to search.")
        return
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak("Searching on Google.")

def play_youtube(query):
    if query.strip() == "":
        speak("Please tell me what to play on YouTube.")
        return
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    speak("Opening YouTube.")

def open_app(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe"
    }
    app_name = app_name.strip().lower()
    if app_name in apps:
        os.system(apps[app_name])
        speak(f"Opening {app_name}.")
    else:
        speak("App not found. Try 'open notepad' or 'open calculator'.")


# ---------- NOTES ----------
def write_note():
    speak("What should I write in the note?")
    text = input("Note: ")
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    speak("Note saved.")

def read_notes():
    try:
        with open("notes.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                speak("Here are your notes:")
                print("\n----- NOTES -----")
                print(content)
                print("-----------------")
            else:
                speak("Your notes file is empty.")
    except FileNotFoundError:
        speak("No notes found yet.")


# ---------- TO-DO MANAGER ----------
def todo_manager():
    speak("To-do manager: 1. Add task  2. View tasks  3. Clear tasks")
    choice = input("Choose an option (1/2/3): ").strip()

    if choice == "1":
        task = input("Enter task: ")
        with open("todo.txt", "a", encoding="utf-8") as f:
            f.write(task + "\n")
        speak("Task added to your list.")

    elif choice == "2":
        try:
            with open("todo.txt", "r", encoding="utf-8") as f:
                tasks = f.read().strip()
                if tasks:
                    speak("Here are your tasks:")
                    print("\n----- TO-DO LIST -----")
                    print(tasks)
                    print("----------------------")
                else:
                    speak("Your to-do list is empty.")
        except FileNotFoundError:
            speak("No tasks found yet.")

    elif choice == "3":
        open("todo.txt", "w", encoding="utf-8").close()
        speak("All tasks cleared.")

    else:
        speak("Invalid choice in to-do manager.")


# ---------- JOKES ----------
def crack_joke():
    jokes = [
        "Why don't programmers like nature? Too many bugs.",
        "Why do Java developers wear glasses? Because they don't C sharp.",
        "Debugging: being the detective in a crime movie where you are also the murderer.",
        "Why was the computer cold? It forgot to close its Windows.",
        "I would tell you a UDP joke, but you might not get it."
    ]
    speak(random.choice(jokes))


# ---------- COMMAND HISTORY ----------
def save_history(command):
    try:
        with open("history.txt", "a", encoding="utf-8") as f:
            f.write(command + "\n")
    except:
        # Don't crash if file can't be written
        pass


# ---------- VOICE INPUT ----------
def take_voice_command():
    """Listen from microphone and return recognized text."""
    if not SR_AVAILABLE:
        speak("Speech Recognition is not available. Please use text mode.")
        return ""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You (voice): {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand. Please say it again.")
    except sr.RequestError:
        speak("Network error for voice recognition. Please check internet.")
    except Exception:
        speak("Some error occurred while recognizing your voice.")

    return ""


# ---------- HELP MENU ----------
def show_help():
    help_text = """
Available Commands:
- time               -> show current time
- date               -> show today's date
- google <query>     -> search on Google
- youtube <query>    -> search on YouTube
- open notepad       -> open Notepad
- open calculator    -> open Calculator
- note               -> create a note
- read notes         -> display saved notes
- todo               -> open to-do manager
- joke               -> tell a programming joke
- help               -> show this help message
- exit / quit        -> close JARVIS
"""
    print(help_text)
    speak("These are the commands you can use.")


# ---------- MAIN ----------
def handle_command(command: str):
    """Process a single user command string."""
    command = command.lower().strip()
    save_history(command)

    if command == "":
        return

    if "time" in command:
        speak(f"The time is {get_time()}.")

    elif "date" in command:
        speak(f"Today's date is {get_date()}.")

    elif command.startswith("google "):
        query = command.replace("google ", "", 1)
        google_search(query)

    elif command.startswith("youtube "):
        query = command.replace("youtube ", "", 1)
        play_youtube(query)

    elif command.startswith("open "):
        app = command.replace("open ", "", 1)
        open_app(app)

    elif "read notes" in command:
        read_notes()

    elif "note" in command:
        write_note()

    elif "todo" in command:
        todo_manager()

    elif "joke" in command:
        crack_joke()

    elif "help" in command:
        show_help()

    elif "exit" in command or "quit" in command:
        speak("Goodbye! Have a great day.")
        return "EXIT"

    else:
        speak("Command not recognized. Type 'help' to see available commands.")


def main():
    speak("Hello! I am your JARVIS assistant.")

    # Choose mode
    print("\nChoose mode:")
    print("1. Text mode")
    print("2. Voice + Text mode (requires microphone and extra libraries)")
    mode = input("Enter 1 or 2: ").strip()

    voice_mode = (mode == "2" and SR_AVAILABLE)

    if mode == "2" and not SR_AVAILABLE:
        speak("Voice libraries not available. Switching to text mode.")
        voice_mode = False

    if voice_mode:
        speak("Voice mode activated. Say 'exit' or 'quit' to stop.")
    else:
        speak("Text mode activated. Type 'help' to see what I can do.")

    while True:
        if voice_mode:
            command = take_voice_command()
            if command == "":
                continue
        else:
            command = input("\nYou: ")

        result = handle_command(command)
        if result == "EXIT":
            break


if __name__ == "__main__":
    main()
