from flask import Flask, jsonify

app = Flask(__name__)
command = "none"

@app.route('/')
def home():
    return "Gesture Server is Running!"

@app.route('/command')
def get_command():
    global command
    temp = command
    command = "none"
    return jsonify({"command": temp})

@app.route('/set/<cmd>')
def set_command(cmd):
    global command
    command = cmd
    return f"Command set to {cmd}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
