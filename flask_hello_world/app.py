import os
import time
from flask import Flask

app = Flask(__name__)
version = 'v4'

@app.route("/")
def index():
	return f"this is {version}: {get_pod_name()} === {str(time.time())}"

@app.route("/health_check")
def health_check():
	return "all is ok"

def get_pod_name():
	return os.environ.get("POD_NAME", "empty")


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)