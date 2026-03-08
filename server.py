from flask import Flask, request, jsonify

app = Flask(__name__)

command = None

TOKEN = "123456"

@app.route("/")
def home():
    return "PC Remote Server Online"

@app.route("/send")
def send():
    global command
    token = request.args.get("token")

    if token != TOKEN:
        return "Forbidden", 403

    cmd = request.args.get("cmd")
    command = cmd
    return "OK"

@app.route("/get")
def get():
    global command
    token = request.args.get("token")

    if token != TOKEN:
        return "Forbidden", 403

    if command:
        c = command
        command = None
        return jsonify({"cmd": c})

    return jsonify({"cmd": None})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
