from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import time
from jinja2 import Environment, FileSystemLoader

HOST = "192.168.1.104"
PORT = 9999

class simpleHTTP(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Log messages to a file or console"""
        log_message = "%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args)
        logging.info(log_message)

    def render_template(self, template_name, context=None):
        """Render HTML templates using Jinja2"""
        templates_dir = 'templates'
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template(template_name)
        return template.render(context or {})

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            page_content = self.render_template('index.html', {'message': 'Hello World!'})
            self.wfile.write(bytes(page_content, "utf-8"))
        else:
            self.send_error(404, "Not Found", "Resource not found")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.wfile.write(bytes(f'{{"time": "{date}"}}', "utf-8"))

if __name__ == '__main__':
    logging.basicConfig(filename='server.log', level=logging.INFO)
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, simpleHTTP)
    print(f"Server now running at http://{HOST}:{PORT}")
    httpd.serve_forever()
