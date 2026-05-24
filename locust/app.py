# app.py — A tiny fake website we'll use as our "target" to load test
# This uses Flask, a simple Python web framework

from flask import Flask  # Import Flask to create our mini web server

app = Flask(__name__)   # Create the web app; __name__ just means "this file"


# This creates a page at http://localhost:5000/
# When someone visits it, they get back "Hello, World!"
@app.route("/")
def home():
    return "Hello, World!"


# This creates a page at http://localhost:5000/about
@app.route("/about")
def about():
    return "About page"


# This creates a page at http://localhost:5000/items
@app.route("/items")
def items():
    return "Here are your items: apple, banana, cherry"


# This runs the web server when you execute: python app.py
# debug=True means it will show helpful errors in the browser
if __name__ == "__main__":
    app.run(debug=True, port=5000)
