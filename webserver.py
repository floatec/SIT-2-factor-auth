import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pro

class MyHandler(BaseHTTPRequestHandler):

    def do_Get(self):
        try:
            if self.path.endswitch(".html"):
                f = open(curdir + sep + self.path)

                self.send_response(200)
                self.send_header(('Content-type'), 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_Post(self):
        pass


def main():
    try:
        server = HTTPServer(('',80),MyHandler)
        print 'started httpserver... hell Yeah!'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down Server, Baby!'
        server.socket.close()

if __name__ == '__main__':

    main()