from Cache_Module import Cache
from flask import Flask, request, Response
import requests

app = Flask(__name__)
cache = Cache(100)
SITE_NAME = "http://localhost:7000"

@app.route("/<path:path>")  #,  methods=["GET", "POST", "DELETE", "HEAD"]
@app.route("/")
def proxy(path=""):
    global SITE_NAME
    print(f"Serving at- {SITE_NAME}")
    if request.method in "GET":
        print("DEBUG")
        print("path: ",path)
        print("url: ",request.url)
        print("REQ args: ",request.args)

        url_bits = request.url.split("?", 1)
        qs = "?" + url_bits[1] if len(url_bits) > 1 else ""

        host = [h[1] for h in request.headers if h[0].lower() == 'host'][0]
        recreated_request = "https://"+host+"/"+str(path)+qs
        resp = requests.get(recreated_request, headers=dict(request.headers))
        cache_key = (recreated_request, request.method)

        response = Response(resp.content, resp.status_code)
        return response

    else:
        return ""


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=7000)  # Change to a different port so that you needn't run as root
    # #DEBUG
    # from pprint import pprint
    # pprint(vars(request))
    # print(request.data)
