import subprocess
import os
import datetime
import webbrowser
import requests
from ddgs import DDGS

try:
    import wikipedia
except ImportError:
    wikipedia = None

# --- 1. SPEAK & PRINT FUNCTION ---
def speak(text):
    print(f"JARVIS: {text}")
    # Uses macOS built-in voice (safely escapes quotes)
    safe_text = text.replace('"', '')
    os.system(f'say "{safe_text}"')

# --- 2. COMMAND HANDLER ---
def execute_command(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}.")

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}.")

    elif "weather" in command:
        try:
            response = requests.get("https://wttr.in/?format=%C+and+%t", timeout=5)
            if response.status_code == 200:
                speak(f"The current weather is {response.text.strip()}.")
            else:
                speak("Sorry, I couldn't fetch the weather right now.")
        except Exception:
            speak("I am having trouble connecting to the weather service.")

    elif command.startswith("open "):
        target = command.replace("open ", "", 1).strip().lower()

        # Common website shortcuts
        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://www.github.com",
            "gmail": "https://mail.google.com",
            "instagram": "https://www.instagram.com",
            "chatgpt": "https://chatgpt.com",
            "spotify": "https://open.spotify.com",
            "whatsapp": "https://web.whatsapp.com"
        }

        # Common macOS app aliases
        mac_app_aliases = {
            "settings": "System Settings",
            "system settings": "System Settings",
            "vscode": "Visual Studio Code",
            "vs code": "Visual Studio Code",
            "files": "Finder",
            "finder": "Finder",
            "browser": "Safari",
            "terminal": "Terminal"
        }

        # 1. Check if it's a known website shortcut
        if target in websites:
            speak(f"Opening {target}...")
            webbrowser.open(websites[target])

        # 2. Try opening it as a macOS Application
        elif target in mac_app_aliases or subprocess.run(["open", "-a", mac_app_aliases.get(target, target.title())], capture_output=True).returncode == 0:
            app_name = mac_app_aliases.get(target, target.title())
            speak(f"Opening {app_name}.")

        # 3. If it looks like a URL (e.g. "reddit.com")
        elif "." in target:
            speak(f"Opening {target}.")
            webbrowser.open(f"https://{target}")

        # 4. Fallback search
        else:
            speak(f"Opening Google Search for {target}.")
            webbrowser.open(f"https://www.google.com/search?q={target}")

    elif "who is" in command or "what is" in command or "wikipedia" in command:
        if wikipedia is None:
            speak("Wikipedia module is not installed. Run 'pip install wikipedia' in your terminal.")
            return

        query = command.replace("who is", "").replace("what is", "").replace("wikipedia", "").strip()
        speak(f"Searching Wikipedia for {query}...")
        try:
            summary = wikipedia.summary(query, sentences=2)
            speak(summary)
        except Exception:
            speak("I could not find any information on that topic on Wikipedia.")

    elif "what can you do" in command or "what can u do" in command:
        speak("I can tell you the time, date, live weather, open apps/websites, search Wikipedia, and query the internet for any topic.")

    elif command in ["exit", "quit", "bye", "stop"]:
        speak("Shutting down. Goodbye!")
        exit()

    # --- 3. INTERNET SEARCH FOR ANY OTHER QUESTION ---
    else:
        print("JARVIS: Searching the internet...")
        try:
            results = DDGS().text(command, max_results=1)
            if results:
                answer = results[0].get("body", "")
                speak(answer)
            else:
                speak("I searched the internet, but couldn't find a clear answer.")
        except Exception:
            speak("I am having trouble connecting to the internet right now.")

# --- 4. MAIN LOOP (KEYBOARD INPUT ONLY, NO MIC) ---
if __name__ == "__main__":
    speak("All systems online. How can I help?")
    while True:
        try:
            user_input = input("\nYou: ").strip().lower()
            if user_input:
                execute_command(user_input)
        except KeyboardInterrupt:
            print("\n")
            speak("Shutting down. Goodbye!")
            break