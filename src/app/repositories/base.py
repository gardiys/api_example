class HTTPRepository:
    def __init__(self, host):
        self.host = host

    async def get(self, url, *args, **kwargs):
        return {"description": "my awesome description"}

    async def post(self, url, *args, **kwargs):
        pass

    async def put(self, url, *args, **kwargs):
        pass

    async def delete(self, url, *args, **kwargs):
        pass
