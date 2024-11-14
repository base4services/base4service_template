from fastapi import APIRouter

router = APIRouter()

from base4.utilities.service.startup import service as app

from .health import *
from .options import *

app.include_router(router, prefix="/api/__SERVICE_NAME__")
