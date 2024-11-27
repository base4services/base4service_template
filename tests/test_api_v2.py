import os
import time

import requests

current_file_path = os.path.abspath(os.path.dirname(__file__))
from .test_base_tenants import TestBase, TestBaseTenants
import uuid
from base4.utilities.service.startup import service as app
from fastapi.testclient import TestClient
from io import BytesIO

client = TestClient(app)


class TestSVC(TestBaseTenants):
	services = ['tenants', '__SERVICE_NAME__']
	
	async def setup(self):
		await super().setup()
	
	async def test_option_by_key_multi_handler(self):
		key = str(uuid.uuid4())
		response = client.post('/api/v2/__SERVICE_NAME__/by-key/%s' % key)
		assert response.status_code == 200
		json: dict = response.json()
		assert json == {'status': 'ok'}
		
		response = client.get('/api/v2/__SERVICE_NAME__/by-key/%s' % key)
		assert response.status_code == 200
		json: dict = response.json()
		assert json == key
		
		response = client.delete('/api/v2/__SERVICE_NAME__/by-key/%s' % key)
		assert response.status_code == 200
		json: dict = response.json()
		assert json == {'status': 'ok'}
		
		response = client.get('/api/v2/__SERVICE_NAME__/by-key/%s' % key)
		assert response.status_code == 200
		json: dict = response.json()
		assert json == {'status': 'not_found'}
	
	async def test_option_get_from_cache(self):
		
		response = client.get("/api/v2/__SERVICE_NAME__/cached-datetime")
		
		assert response.status_code == 200
		json_1: dict = response.json()
		
		response = client.get("/api/v2/__SERVICE_NAME__/cached-datetime")
		assert response.status_code == 200
		json_2: dict = response.json()
		assert json_1 == json_2
	
	async def test_option_if_cache_expired(self):
		
		response = client.get("/api/v2/__SERVICE_NAME__/cached-datetime")
		assert response.status_code == 200
		json_1: dict = response.json()
		
		time.sleep(3)
		response = client.get("/api/v2/__SERVICE_NAME__/cached-datetime")
		assert response.status_code == 200
		json_2: dict = response.json()
		assert json_1 != json_2
	
	async def test_option_by_key_1_on_1_handler(self):
		key = str(uuid.uuid4())
		response = client.get('/api/v2/__SERVICE_NAME__/1on1/by-key/%s' % key)
		assert response.status_code == 200
		json: dict = response.json()
		assert json == key
	
	async def test_option_no_key_bug(self):
		response = client.get('/api/v2/__SERVICE_NAME__/no-key-bug')
		assert response.status_code == 200
		json: dict = response.json()
		assert json == {'status': 'ok'}

	
	async def test_option_single_upload(self):
		url = "https://cdn.prod.website-files.com/634fe37f7bef5774d03a854d/642d457d480f67449142b775_Loader.svg"
		ext = url.split('/')[-1].split('.')[-1]
		
		response = requests.get(url)
		assert response.status_code == 200
		
		file_data = BytesIO(response.content)  # Create a file-like object
		files = {"files": (f"img1.{ext}", file_data, f"image/{ext}")}
		upload_response = client.post("/api/v2/__SERVICE_NAME__/upload", files=files)
		
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
		upload_response = client.post(
			"/api/v2/__SERVICE_NAME__/upload", files=files, data={"description": "This is a test description"}
		)
		
		assert upload_response.status_code == 200
		assert upload_response.json()[f"img1.{ext}"]['content_type'] == f'image/{ext}'
		assert upload_response.json()[f"img1.{ext}"]['size'] >= 0
		assert upload_response.json()[f"img1.{ext}"]['description'] == "This is a test description"
	
	async def test_option_multi_upload(self):
		files = []
		for idx, img in enumerate(
				[
					"https://cdn.prod.website-files.com/634fe37f7bef5774d03a854d/642d457d480f67449142b775_Loader.svg",
					"https://cdn.prod.website-files.com/634fe37f7bef5774d03a854d/642d409c651b714dd373fe33_Favicon-Digitalcube.png"
				], start=1
		):
			ext = img.split('/')[-1].split('.')[-1]
			response = requests.get(img)
			assert response.status_code == 200
			
			file_data = BytesIO(response.content)  # Create a file-like object
			files.append(("files", (f"img{idx}.{ext}", file_data, f"image/{ext}")))
		
		upload_response = client.post("/api/v2/__SERVICE_NAME__/upload", files=files)
		
		assert upload_response.status_code == 200
		for idx, img in enumerate(
				[
					"https://cdn.prod.website-files.com/634fe37f7bef5774d03a854d/642d457d480f67449142b775_Loader.svg",
					"https://cdn.prod.website-files.com/634fe37f7bef5774d03a854d/642d409c651b714dd373fe33_Favicon-Digitalcube.png"
				], start=1
		):
			ext = img.split('/')[-1].split('.')[-1]
			assert upload_response.json()[f"img{idx}.{ext}"]['content_type'] == f'image/{ext}'
			assert upload_response.json()[f"img{idx}.{ext}"]['size'] >= 0
	
	async def test_max_files_over_limit(self):
		files = [
			("files", ("img1.svg", BytesIO(b"Fake content 1"), "image/svg")),
			("files", ("img2.svg", BytesIO(b"Fake content 2"), "image/svg")),
			("files", ("img3.svg", BytesIO(b"Fake content 3"), "image/svg")),
			("files", ("img4.svg", BytesIO(b"Fake content 4"), "image/svg")),
			("files", ("img4.svg", BytesIO(b"Fake content 4"), "image/svg")),
			("files", ("img4.svg", BytesIO(b"Fake content 4"), "image/svg")),
		]
		upload_response = client.post("/api/v2/__SERVICE_NAME__/upload", files=files)
		
		assert upload_response.status_code == 400
	
	async def test_max_files_in_limit(self):
		files = [
			("files", ("img1.svg", BytesIO(b"Fake content 1"), "image/svg")),
			("files", ("img2.svg", BytesIO(b"Fake content 2"), "image/svg")),
			("files", ("img3.svg", BytesIO(b"Fake content 3"), "image/svg")),
			("files", ("img4.svg", BytesIO(b"Fake content 4"), "image/svg")),
		]
		upload_response = client.post("/api/v2/__SERVICE_NAME__/upload", files=files)
		
		assert upload_response.status_code == 200
