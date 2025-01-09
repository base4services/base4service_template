from base4.utilities.service.base import CRUDAPIHandler, BaseAPIHandler, api, route
from fastapi import APIRouter, Request


@route(router=APIRouter(), prefix='/api/__SERVICE_NAME__')
class APIHandler(CRUDAPIHandler):
    def __init__(self, router):
        super().__init__(router, service='example', schema='example', model='example')

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
        # is_public=False,
    )
    async def example(self, request: Request) -> dict:
        return {"hello": "world"}
