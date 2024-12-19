import os
import time

import requests

current_file_path = os.path.abspath(os.path.dirname(__file__))
from .test_base_tenants import TestBaseTenantsAPIV2


class TestSVC(TestBaseTenantsAPIV2):
	services = ['tenants', '__SERVICE_NAME__']
	
	async def setup(self):
		await super().setup()
	
	async def test_is___SERVICE_NAME___healthy(self):
		response = await self.request(method='get', url="/api/__SERVICE_NAME__/healthy", headers={'X-Tenant-ID': 'pass'})
		assert response.status_code == 200
