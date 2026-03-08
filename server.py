from flask import Flask, request, jsonify
from collections import deque
import time
import secrets

app = Flask(__name__)

TOKEN = "123456"
CLIENT_TOKEN = "123456"
commands = deque(maxlen=100)

def bad_token(token: str, expected: str) -> bool:
    return token != expected

@app.route("/")
def home():
    return "PC Remote Server Online"

@app.route("/health")
def health():
    return jsonify({"ok": True, "pending": len(commands)})

# Phone/app sends commands here
@app.route("/send")
def send():
    token = request.args.get("token", "")
    if bad_token(token, TOKEN):
        return "Forbidden", 403

    cmd = request.args.get("cmd", "").strip()
    if not cmd:
        return "cmd is required", 400

    item = {
        "id": secrets.token_hex(4),
        "cmd": cmd,
        "time": int(time.time())
    }
    commands.append(item)
    return jsonify({"ok": True, "queued": item})

# Laptop client polls here
@app.route("/get")
def get():
    token = request.args.get("token", "")
    if bad_token(token, CLIENT_TOKEN):
        return "Forbidden", 403

    if commands:
        return jsonify(commands.popleft())

    return jsonify({"cmd": None})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
