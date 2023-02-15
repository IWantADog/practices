import time
import logging

from flask import Flask

_LOGGER = logging.getLogger()

app = Flask(__name__)

@app.route("/")
def index():
    _LOGGER.info("test")
    return f"is't works! now at {time.time()}"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80)