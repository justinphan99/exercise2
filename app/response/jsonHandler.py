import json
from app.response.requestHandler import RequestHandler

class JsonHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = 'application/json'

    def jsonParse(self, data):
        try:
            self.contents = json.dumps(data)
            self.setStatus(200)
            return True
        except:
            self.setStatus(404)
            return False