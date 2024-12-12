import os
import datetime
from typing import Dict
from base4.utilities.service.base import api, route
from base4.utilities.service.base import BaseAPIHandler
from fastapi import Request, APIRouter

router = APIRouter()


@route(router=router, prefix='/api/__SERVICE_NAME__')
class APIHandler(BaseAPIHandler):
    @api(
        path='/healthy',
    )
    async def healthy(self, request: Request):
        return {'status': 'ok'}
    
    @api(
        methods=['GET'],
        path='/options/by-key/{key}',
        response_model=Dict[str, str]
    )
    async def get_by_key(self, request: Request, key: str) -> dict:
        service = self.service.OptionService()
        return await service.get_option_by_key(key)
