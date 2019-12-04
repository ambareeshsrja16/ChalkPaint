from cache_module import Cache
from flask import Flask, request, Response
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

cache = Cache(size_of_cache=1000)  #TODO Ideally figure out from average request rate etc, and need to check when to flush
@app.route("/<path:path>", methods=["GET", "POST", "HEAD", "DELETE"])
@app.route("/", methods=["GET","POST", "HEAD", "DELETE"])
def proxy(path=""):

    SCHEME_PREFIX = "https://"
    EXPIRY_LIMIT = 10000
    url_bits = request.url.split("?", 1)
    qs = "?" + url_bits[1] if len(url_bits) > 1 else ""  # queries

    expiry_time = datetime.now()+ timedelta(seconds =EXPIRY_LIMIT)
    # Extract host
    host = [h[1] for h in request.headers if h[0].lower() == 'host'][0]

    # Extract custom header
    # print("custom")
    # print("HEADER",request.headers)  # NOT PRINTING
    # print([h[1] for h in request.headers]) # ['www.ezoic.com', 'curl/7.64.1', '*/*', 'True']
    # print([h[0] for h in request.headers])  # ['www.ezoic.com', 'curl/7.64.1', '*/*', 'True']

    # print("remove",  [ h[1] for h in request.headers if h[0].lower() == 'remove-from-cache' ])  # NOT PRINTING
    remove_from_cache = [ h[1] for h in request.headers if h[0].lower() == 'remove-from-cache']

    if not remove_from_cache:
        remove_from_cache = False

    recreated_request = SCHEME_PREFIX + host + "/" + str(path) + qs  # TODO Not ideal, not safe
    # recreated_request => https://www.ezoic.com/ad-tester-details/

    cache_key = (recreated_request, request.method)

    if remove_from_cache: # header is true
        if cache_key not in cache.main_cache or cache[cache_key][1] < datetime.now():
            # Construct response saying element wasn not present to begin with
            response = Response("Element not present in cache", 200)  #Make response content
        else:
            cache.main_cache.pop(cache_key, None)
            # Construct appropriate response converying element was found and removed
            response = Response("Element present in cache, Deleted", 200)
        return response


    if request.method in {"GET", 'HEAD'}:
        # print("Cache check functional")
        if cache_key not in cache.main_cache or cache[cache_key][1] < datetime.now():   # namedTuple   # try catches TEST Case
            print("From Server, moving to Cache")
            if request.method == "HEAD":
                resp = requests.head(recreated_request, headers=dict(request.headers))
            else:
                resp = requests.get(recreated_request, headers=dict(request.headers))

            if "cache-control" in resp.headers:
                value = resp.headers["cache-control"]
                if "max-age" in value:
                    expiry_time = datetime.now() + timedelta(seconds = int(value.split('max-age=')[1].split(",")[0]))  # check
                    # expiry_time = datetime.now() - datetime.now()  + timedelta(seconds = 100)   # hack chage later, cast
                    # expiry_time =  datetime.now() - timedelta(seconds = int(value.split('max-age=')[1].split(",")[0]))
                    print("Expiry time",expiry_time)

            # 'Cache-Control': 'public, max-age=60, s-maxage=60'
            response = Response(resp.content, resp.status_code)
            cache[cache_key] = response, expiry_time  # Need to add expiry_time absolute  #syntax

        return cache.main_cache[cache_key][0]

    elif request.method == 'POST':
        req_data = request.get_data()
        resp = requests.post(recreated_request, headers=dict(request.headers), data=req_data)
        response = Response(resp.content, resp.status_code)
        return response

    elif request.method == "DELETE":
        resp = requests.delete(recreated_request, headers=dict(request.headers))
        response = Response(resp.content, resp.status_code)
        return response

    #TODO Do other methods


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=7000)  # Change to a different port so that you needn't run as root
