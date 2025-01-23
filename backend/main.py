import http.server
import socketserver
import requests
import xml.etree.ElementTree as ET
import json

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/rss':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            feed_url = "https://techxplore.com/rss-feed/breaking/machine-learning-ai-news/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }

            try:
                response = requests.get(feed_url, headers=headers)
                response.raise_for_status()
            except requests.RequestException as e:
                self.send_error(500, f"Error fetching RSS feed: {e}")
                return

            try:
                root = ET.fromstring(response.content)
            except ET.ParseError as e:
                self.send_error(500, f"Error parsing XML: {e}")
                return

            articles = []
            for item in root.findall(".//item"):
                article = {
                    "title": item.findtext("title"),
                    "description": item.findtext("description"),
                    "link": item.findtext("link"),
                    "category": item.findtext("category"),
                    "pubDate": item.findtext("pubDate"),
                    "thumbnail": item.find(".//thumbnail").attrib.get("url") if item.find(".//thumbnail") is not None else None
                }
                articles.append(article)

            self.wfile.write(json.dumps(articles).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server runs at http://localhost:{PORT}/api/rss")
    httpd.serve_forever()
