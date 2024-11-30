import datetime

from base4.utilities.service.base import api
from . import router
from base4.utilities.service.startup import service as app
from base4.utilities.service.base import BaseAPIController
from fastapi import FastAPI, APIRouter, Request, HTTPException, status
from typing import Dict, Callable, Optional, List
from fastapi import File, UploadFile, Form
from base4.utilities.files import get_project_root
from base4.utilities.db.redis import RedisClientHandler
import os

rdb = RedisClientHandler().redis_client


class APIV2(BaseAPIController):
	def __init__(self, router: APIRouter):
		self.service = ''
		super().__init__(router)
	
	@api(
		permissions=[],
		path='/by-key/{key}',
		methods=['GET', 'POST', 'DELETE'],
	)
	async def multi_handler_option_by_key(self, key: str, request: Request):
		if request.method == 'POST':
			rdb.sadd('test_option_by_key', key)
			return {'status': 'ok'}
		elif request.method == 'GET':
			if rdb.sismember('test_option_by_key', key):
				return key
			return {'status': 'not_found'}
		
		elif request.method == 'DELETE':
			rdb.srem('test_option_by_key', key)
			return {'status': 'ok'}
		return {}
	
	@api(
		permissions=[],
		path='/no-key-bug',
		methods=['GET', 'POST'],
	)
	async def no_key_bug(self, request: Request):
		return {'status': 'ok'}
	
	@api(
		permissions=[],
		cache=2,
		path='/cached-datetime',
		methods=['GET'],
	)
	async def cached_datetime(self, request: Request):
		return {'datetime': datetime.datetime.now().isoformat()}
	
	@api(
		permissions=[],
		path='/1on1/by-key/{key}',
		methods=['GET'],
	)
	async def _1on1_handler(self, key: str, request: Request):
		return key
	
	@api(
		permissions=[],
		path='/upload',
		methods=['POST'],
		upload_allowed_file_types=["image/jpeg", "image/png", "image/svg"],
		upload_max_file_size=5 * 1024 * 1024,  # 5 MB
		upload_max_files=5,
	)
	async def upload(self, request: Request, description: Optional[str] = Form(None),files: List[UploadFile] = File(...)):
		project_root = str(get_project_root())
		
		os.makedirs(f"{project_root}/tests/uploads", exist_ok=True)
		
		results = {}
		for file in files:
			content = await file.read()
			# todo: save file to disk
			save_path = f"{project_root}/tests/uploads/{file.filename}"
			with open(save_path, "wb") as buffer:
				buffer.write(content)

			results[file.filename] = {
				"content_type": file.content_type,
				"size":         len(content),
				"description":  description,
			}

		return results

	@api(
		permissions=['ROOT'],
		path='/tenants',
		methods=['GET'],
	)
	async def tenants(self, request: Request):
		return {'status': 'ok'}
	
	
APIV2(router)
app.include_router(router, prefix='/api/v2/__SERVICE_NAME__')
