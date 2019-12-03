
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHandler(BaseHTTPRequestHandler):
    """This class will handles any incoming request from the browser"""
    
    def do_GET(self):
        """Handler for the GET requests"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        
        
        return

PORT = 80
cache_obj = Cache(1000)

with HTTPServer(("", PORT), MyHandler) as httpd:  # TODO Configure this to work for only specific addresses
    print("Serving at port", PORT)
    httpd.serve_forever()
