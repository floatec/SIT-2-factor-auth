import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pro
import urlparse
import dbConnection as db


class MyHandler(BaseHTTPRequestHandler):
    def do_get(self):
        o = urlparse.urlparse(self.path)
        param = urlparse.parse_qs(o.query)
        if 'hash' in param.keys():
            db.validate(param['user'], param['hash'])
        try:
            if self.path.endswitch(".html"):
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_post(self):
        pass


def main():
    try:
        server = HTTPServer(('', 80), MyHandler)
        print 'started httpserver... hell Yeah!'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down Server, Baby!'
        server.socket.close()

if __name__ == '__main__':

    main()