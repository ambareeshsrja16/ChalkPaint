from cache_module import Cache
from flask import Flask, request, Response
import requests

PORT_NO = 7200
app = Flask(__name__)

cache = Cache(100)

@app.route("/<path:path>", methods=["GET", "POST"])
@app.route("/")
def proxy(path=""):
    #  DEBUG
    # print(f"Proxy Running successfully")
    resp_str = ""
    resp_str += "request_url" + str(request.url) + "\n"
    resp_str += "request.method" + str(request.method) + "\n"
    resp_str += "request.form" + str([(x, request.form[x]) for x in request.form]) + "\n"
    response = Response(resp_str.encode('utf-8'), 200)

    return response


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=PORT_NO)  # Change to a different port so that you needn't run as root