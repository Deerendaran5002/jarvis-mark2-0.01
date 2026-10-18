from flask import Flask, request, jsonify
from flask_cors import CORS
import webbrowser
import subprocess

app = Flask(__name__)
CORS(app)  # Allows your HTML browser page to send requests to Python

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.get_json()
    command = data.get('command', '').strip().lower()

    if not command:
        return jsonify({'ok': False, 'reply': 'Empty command received.'})

    # Ping check when HTML loads
    if command == 'ping':
        return jsonify({'ok': True, 'reply': 'Mac Bridge connected.'})

    # Web & App Launcher Logic
    if command.startswith("open "):
        target = command.replace("open ", "", 1).strip()

        # Web Shortcuts
        websites = {
            "spotify": "https://open.spotify.com",
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://www.github.com",
            "gmail": "https://mail.google.com"
        }

        if target in websites:
            webbrowser.open(websites[target])
            return jsonify({'ok': True, 'reply': f'Opening {target} in web browser.'})

        # Try opening as a Mac Desktop App
        result = subprocess.run(["open", "-a", target.title()], capture_output=True)
        if result.returncode == 0:
            return jsonify({'ok': True, 'reply': f'Opening {target.title()} application.'})

        # Fallback to web search
        webbrowser.open(f"https://www.google.com/search?q={target}")
        return jsonify({'ok': True, 'reply': f'Searching for {target}.'})

    return jsonify({'ok': False, 'reply': 'Command not recognized.'})

if __name__ == '__main__':
    print("JARVIS Mac Bridge running on http://127.0.0.1:5050")
    app.run(port=5050)