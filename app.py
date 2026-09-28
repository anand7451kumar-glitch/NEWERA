from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return"<h1>hello Anand <h1><p>My first Python web app!</p>"

@app.route("/about")
def about():
    return "<h1>About</h1><p>Built with Python and Flask.</p>"

app.run(debug=True)

