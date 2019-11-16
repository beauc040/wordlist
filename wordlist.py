from flask import Flask
from markupsafe import escape

app = Flask(__name__)

name = "Ethan"

@app.route("/")
def hello_world():
    return f"<p>Hello, {escape(name)}!</p>"
