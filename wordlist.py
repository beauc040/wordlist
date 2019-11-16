from flask import Flask
from markupsafe import escape

wordlist = Flask(__name__)

name = "Ethan"

@wordlist.route("/")
def hello_world():
    return f"<p>Hello, {escape(name)}!</p>"
