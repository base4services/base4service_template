
from base4.service.base_service_v2 import BaseServiceV2
from base4.utilities.logging.setup import get_logger
from fastapi.requests import Request

from ._db_conn import get_conn_name

logger = get_logger()


class __SERVICE_NAME__Service(BaseServiceV2['PROVIDE SCHEMA MODEL HERE']):
    def __init__(self, request: Request):
        self.me = getattr(request, 'me', None)
        super().__init__(schema=None, model=None, conn_name=get_conn_name(), c11=None, c1n=None,
                         uid_prefix='?', uid_total_length=10, uid_alphabet='WERTYUPASFGHJKLZXCVNM2345679')