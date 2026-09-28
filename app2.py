from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    name = ""

    if request.method == "POST":
        name = request.form["name"]

    return f"""
    <h1>Hello {name}</h1>

    <form method="POST">
        <input name="name" placeholder="Enter your name">
        <button>Submit</button>
    </form>
    """


app.run(debug=True)