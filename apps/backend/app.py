from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.get("/api/hello")
def hello_world():
  return "Hello, World!"


if __name__ == "__main__":
  app.run(host="127.0.0.1", port=5000)
