import os
import time

import requests

current_file_path = os.path.abspath(os.path.dirname(__file__))
from .test_base_tenants import TestBaseTenantsAPIV2
import uuid
from base4.utilities.service.startup import service as app
from fastapi.testclient import TestClient
from io import BytesIO
import ujson as json

test_json = {
	'a': 'test',
	'b': 1,
	'c': {'a': {'b': 'c'}},
	'd': [1, 2, 3],
}


class TestSVC(TestBaseTenantsAPIV2):
	services = ['tenants', '__SERVICE_NAME__']
	
	async def setup(self):
		await super().setup()
	#
	# async def test_option_by_key_multi_handler(self):
	# 	key = str(uuid.uuid4())
	# 	response = await self.request(method='post', url='/api/__SERVICE_NAME__/by-key/%s' % key)
	# 	assert response.status_code == 200
	# 	json: dict = response.json()
	# 	assert json == {'status': 'ok'}
	#
	# 	response = await self.request(method='get', url='/api/__SERVICE_NAME__/by-key/%s' % key)
	# 	assert response.status_code == 200
	# 	json: dict = response.json()
	# 	assert json == key
	#
	# 	response = await self.request(method='delete', url='/api/__SERVICE_NAME__/by-key/%s' % key)
	# 	assert response.status_code == 200
	# 	json: dict = response.json()
	# 	assert json == {'status': 'ok'}
	#
	# 	response = await self.request(method='get', url='/api/__SERVICE_NAME__/by-key/%s' % key)
	# 	assert response.status_code == 200
	# 	json: dict = response.json()
	# 	assert json == {'status': 'not_found'}
	#
	# async def test_option_get_from_cache(self):
	# 	response = await self.request(method='get', url="/api/__SERVICE_NAME__/cached-datetime")
	#
	# 	assert response.status_code == 200
	# 	json_1: dict = response.json()
	#
	# 	response = await self.request(method='get', url="/api/__SERVICE_NAME__/cached-datetime")
	# 	assert response.status_code == 200
	# 	json_2: dict = response.json()
	# 	assert json_1 == json_2
	#
	# async def test_option_if_cache_expired(self):
	# 	response = await self.request(method='get', url="/api/__SERVICE_NAME__/cached-datetime")
	# 	assert response.status_code == 200
	# 	json_1: dict = response.json()
	#
	# 	time.sleep(3)
	# 	response = await self.request(method='get', url="/api/__SERVICE_NAME__/cached-datetime")
	# 	assert response.status_code == 200
	# 	json_2: dict = response.json()
	# 	assert json_1 != json_2
	#
	# async def test_option_by_key_1_on_1_handler(self):
	# 	key = str(uuid.uuid4())
	# 	response = await self.request(method='get', url='/api/__SERVICE_NAME__/1on1/by-key/%s' % key)
	# 	assert response.status_code == 200
	# 	json: dict = response.json()
	# 	assert json == key
	#
	# async def test_option_no_key_bug(self):
	# 	response = await self.request(method='get', url='/api/__SERVICE_NAME__/no-key-bug')
	# 	assert response.status_code == 200
	# 	json: dict = response.json()
	# 	assert json == {'status': 'ok'}
	#
	# async def test_pydantic(self):
	# 	response = await self.request(
	# 		method='post', url=
	# 		"/api/__SERVICE_NAME__/pydantic",
	# 		json=test_json
	# 		)
	# 	assert response.status_code == 200
	# 	assert response.json() == test_json
	
	async def test_option_single_upload(self):
		url = "https://cdn.prod.website-files.com/634fe37f7bef5774d03a854d/642d457d480f67449142b775_Loader.svg"
		ext = url.split('/')[-1].split('.')[-1]
		
		response = requests.get(url)
		assert response.status_code == 200
		
		file_data = BytesIO(response.content)  # Create a file-like object
		files = {"files": (f"img1.{ext}", file_data, f"image/{ext}")}
		upload_response = await self.request(method='post', url="/api/__SERVICE_NAME__/upload", files=files)
		
		assert upload_response.status_code == 200
		assert upload_response.json()[f"img1.{ext}"]['content_type'] == f'image/{ext}'
		assert upload_response.json()[f"img1.{ext}"]['size'] >= 0
	
	async def test_option_single_upload_with_additional_description(self):
		url = "https://cdn.prod.website-files.com/634fe37f7bef5774d03a854d/642d457d480f67449142b775_Loader.svg"
		ext = url.split('/')[-1].split('.')[-1]
		
		response = requests.get(url)
		assert response.status_code == 200
		
		file_data = BytesIO(response.content)  # Create a file-like object
		files = {"files": (f"img1.{ext}", file_data, f"image/{ext}")}
		upload_response = await self.request(
			method='post', url=
			"/api/__SERVICE_NAME__/upload", files=files, data={"metadata": json.dumps(test_json)}
		)
		assert upload_response.status_code == 200
		j = upload_response.json()
		assert j[f"img1.{ext}"]['content_type'] == f'image/{ext}'
		assert j[f"img1.{ext}"]['size'] >= 0
		assert j[f"img1.{ext}"]['description'] == test_json
	
	async def test_max_files_over_limit(self):
		files = [
			("files", ("img1.svg", BytesIO(b"Fake content 1"), "image/svg")),
			("files", ("img2.svg", BytesIO(b"Fake content 2"), "image/svg")),
			("files", ("img3.svg", BytesIO(b"Fake content 3"), "image/svg")),
			("files", ("img4.svg", BytesIO(b"Fake content 4"), "image/svg")),
			("files", ("img4.svg", BytesIO(b"Fake content 4"), "image/svg")),
			("files", ("img4.svg", BytesIO(b"Fake content 4"), "image/svg")),
		]
		upload_response = await self.request(method='post', url="/api/__SERVICE_NAME__/upload", files=files)
		assert upload_response.status_code == 400
	
	async def test_max_files_in_limit(self):
		files = [
			("files", ("img1.svg", BytesIO(b"Fake content 1"), "image/svg")),
			("files", ("img2.svg", BytesIO(b"Fake content 2"), "image/svg")),
			("files", ("img3.svg", BytesIO(b"Fake content 3"), "image/svg")),
			("files", ("img4.svg", BytesIO(b"Fake content 4"), "image/svg")),
		]
		upload_response = await self.request(method='post', url="/api/__SERVICE_NAME__/upload", files=files)
		assert upload_response.status_code == 200
	
	
	async def test_is___SERVICE_NAME___healthy(self):
		response = await self.request(method='get', url="/api/__SERVICE_NAME__/healthy")
		assert response.status_code == 200
