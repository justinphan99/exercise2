from http.server import BaseHTTPRequestHandler
from app.response.unauthorizedRequestHandler import UnauthorizedRequestHandler
from app.routes.main import routes
from app.response.jsonHandler import JsonHandler
from app.response.badRequestHandler import BadRequestHandler
import json
from app.utils.uuid import isValidUUID
import re

class Server(BaseHTTPRequestHandler):

    def do_HEAD(self):
        return

    def do_GET(self):
        token = str(self.headers['Authorization'])
        param = None
        for i in self.path.split('/'):
            if (isValidUUID(i)):
                param = i
        if (param == None):
            if self.path in routes:
                temp = routes[self.path]
                temp.method = 'GET'
                data = temp.operation(token,'', '', '')
                if data == 401:
                    handler = UnauthorizedRequestHandler()
                elif data == 404:
                    handler = BadRequestHandler()
                else:
                    handler = JsonHandler()
                    handler.jsonParse(data)
            else:
                handler = BadRequestHandler()
        elif (param != None):
            tempRoutes = {}
            handler = BadRequestHandler()
            for key in routes.keys():
                tempRoutes[re.sub('{.*}', param, key)] = routes[key]
            if self.path in tempRoutes:
                temp = tempRoutes[self.path]
                temp.method = 'GET'
                data = temp.operation(token,'', param, '')
                print(data)
                if data == 401:
                    handler = UnauthorizedRequestHandler()
                elif data == 404:
                    handler = BadRequestHandler()
                else:
                    handler = JsonHandler()
                    handler.jsonParse(data)
            
        else:
            handler = BadRequestHandler()
        self.respond({
            'handler': handler
        })

    def do_POST(self):
        token = str(self.headers['Authorization'])
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length) 
        post_data = json.loads(post_data.decode().replace("'", '"'))
        param = None
        for i in self.path.split('/'):
            if (isValidUUID(i)):
                param = i
        if param == None:
            if self.path in routes:
                temp = routes[self.path]
                temp.method = 'POST'
                data = temp.operation(token, post_data, '', '')

                if data == 401:
                    handler = UnauthorizedRequestHandler()
                elif data == 404:
                    handler = BadRequestHandler()
                else:
                    handler = JsonHandler()
                    handler.jsonParse(data)
            else:
                handler = BadRequestHandler()
        elif (param != None):
            tempRoutes = {}
            handler = BadRequestHandler()
            for key in routes.keys():
                tempRoutes[re.sub('{.*}', param, key)] = routes[key]
            if self.path in tempRoutes:
                temp = tempRoutes[self.path]
                temp.method = 'POST'
                data = temp.operation(token,post_data, param, '')
                if data == 401:
                    handler = UnauthorizedRequestHandler()
                elif data == 404:
                    handler = BadRequestHandler()
                else:
                    handler = JsonHandler()
                    handler.jsonParse(data)
            else:
                handler = BadRequestHandler()
        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()
        self.send_response(status_code)
        self.send_header('Content-type', handler.getContentType())

        if status_code == 200:
            content = handler.getContents()
        else:
            content = json.dumps(handler.getContents())
        self.end_headers()

        return content.encode()

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)