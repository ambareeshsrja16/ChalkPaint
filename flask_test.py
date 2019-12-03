from Cache_Module import Cache
from flask import Flask, request, Response
import requests

app = Flask(__name__)

cache = Cache(100)
SITE_NAME = "http://localhost:7000"


@app.route("/<path:path>")
@app.route("/")
def proxy(path=""):
    global SITE_NAME
    print(f"Proxy Serving at - {SITE_NAME}")

    url_bits = request.url.split("?", 1)
    qs = "?" + url_bits[1] if len(url_bits) > 1 else ""

    host = [h[1] for h in request.headers if h[0].lower() == 'host'][0]
    recreated_request = "https://" + host + "/" + str(path) + qs
    cache_key = (recreated_request, request.method)

    if request.method in {"GET", "HEAD"}:
        if cache_key not in cache.main_cache:
            # # DEBUG
            print("NOT FROM CACHE")
            resp = requests.get(recreated_request, headers=dict(request.headers))
            response = Response(resp.content, resp.status_code)
            cache[cache_key] = response
        return cache.main_cache[cache_key]
    else:
        resp = requests.get(recreated_request, headers=dict(request.headers))
        response = Response(resp.content, resp.status_code)
        return response


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=7000)  # Change to a different port so that you needn't run as root

