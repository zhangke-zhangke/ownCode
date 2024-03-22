import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/index")
def index_test():
    print("index test,sleep for 15 second")
    time.sleep(15)
    return "index test for non-block"

if __name__ == '__main__':
    print(__name__)
    app.run(host="0.0.0.0", port=8088, debug=True)