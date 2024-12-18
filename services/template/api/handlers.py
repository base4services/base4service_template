from base4.utilities.service.base import BaseAPIHandler, api, route
from fastapi import APIRouter, Request


@route(router=APIRouter(), prefix='/api/__SERVICE_NAME__')
class APIHandler(BaseAPIHandler):
    def __init__(self, router):
        self.service = 'example service module path'
        self.schema = 'example service schema path'
        self.model = 'example service model path'
        super().__init__(router)
    
    @api(
        method='GET',
        path='/example',
        # response_model = Dict[str, str],
        # cache: int = 0,
        # is_accesslog: bool = True,
        # upload_allowed_file_types: Optional[List[str]] = None,
        # upload_max_file_size: Optional[int] = None,
        # upload_max_files: Optional[int] = None
        # is_authorized: bool = False,
    )
    async def example(self, request: Request) -> dict:
        return {"hello": "world"}
