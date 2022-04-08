from app.response.requestHandler import RequestHandler

class SuccessResponse(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = 'application/json'
        self.contents = {
                "status": 200
            }
        self.setStatus(200)