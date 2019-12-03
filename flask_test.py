from cache_module import Cache
from flask import Flask, request, Response
import requests

app = Flask(__name__)

cache = Cache(size_of_cache=1000)  #Ideally figure out from average request rate etc, and need to check when to flush
@app.route("/<path:path>", methods=["GET", "POST", "HEAD", "DELETE"])
@app.route("/", methods=["GET","POST", "HEAD", "DELETE"])
def proxy(path=""):
    #  DEBUG
    # print(f"Proxy Running successfully")
    SCHEME_PREFIX = "https://"
    url_bits = request.url.split("?", 1)
    qs = "?" + url_bits[1] if len(url_bits) > 1 else ""  # queries

    host = [h[1] for h in request.headers if h[0].lower() == 'host'][0]
    # req.headers => list of tuples [('Host', 'www.ezoic.com'), ('User-Agent', 'curl/7.64.1'), ('Accept', '*/*')]

    recreated_request = SCHEME_PREFIX + host + "/" + str(path) + qs  # TODO Not ideal, not safe
    # recreated_request => https://www.ezoic.com/ad-tester-details/

    cache_key = (recreated_request, request.method)

    if request.method in {"GET", 'HEAD'}:
        if cache_key not in cache.main_cache:
            # # DEBUG
            # print("From Server, moving to Cache")
            if request.method == "HEAD":
                resp = requests.head(recreated_request, headers=dict(request.headers))
            else:
                resp = requests.get(recreated_request, headers=dict(request.headers))

            response = Response(resp.content, resp.status_code)
            cache[cache_key] = response
        return cache.main_cache[cache_key]

    # TODO
    elif request.method == 'POST':
        req_data = request.get_data()
        resp = requests.post(recreated_request, headers=dict(request.headers), data=req_data)
        response = Response(resp.content, resp.status_code)
        return response


    elif request.method == "DELETE":
        # Delete or PUT
        resp = requests.delete(recreated_request, headers=dict(request.headers))
        response = Response(resp.content, resp.status_code)
        return response


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=7000)  # Change to a different port so that you needn't run as root

