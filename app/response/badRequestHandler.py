from app.response.requestHandler import RequestHandler

class BadRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = 'application/json'
        self.contents = {
                "status": 404,
                "message": "404 Not Found"
            }
        self.setStatus(404)