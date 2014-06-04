from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import dbConnection as db


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        o = urlparse.urlparse(self.path)
        param = urlparse.parse_qs(o.query)
        if 'hash' in param.keys():
            db.validate_session(param['name'][0], param['hash'][0])
        try:
            f = open('webbrowser.html')

            self.send_response(200)
            self.send_header(('Content-type'), 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        pass


def main():
    server = HTTPServer(('', 8080), MyHandler)
    try:
        print 'Http server up and running!'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down Server!'
        server.socket.close()

if __name__ == '__main__':

    main()