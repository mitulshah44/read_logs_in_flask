import os
import unittest
import requests
import app
import collections
import json

class MyTestCase(unittest.TestCase):
	"""
		Written cases to check responses are expected.

	"""

	def setUp(self):
		self.app = app.app.test_client()

	def tearDown(self):
		pass
        
	def test_main(self):
		r = self.app.get('/')
		self.assertEqual(r.status_code, 200)

	def test_page_not_found(self):
		r = self.app.get('/test')
		self.assertEqual(r.status_code, 404)

	def test_get_content_ok(self):
		"""
		To make function success, setup the log path accordingly.
		"""
		r = self.app.post('/api/getcontent',
						  data=json.dumps({
								'path': "/home/mitul/projects/interview/logs/log.txt",
							}),
						  content_type='application/json'
			)
		t = json.loads(r.data)
		self.assertGreaterEqual(len(t), 1)
		self.assertEqual(r.status_code, 200)

	def test_get_content_failed(self):
		"""
		To make function failed, setup wrong log path.
		"""
		r = self.app.post('/api/getcontent',
						  data=json.dumps({
								'path': "fake",
							}),
						  content_type='application/json'
			)
		t = json.loads(r.data)
		self.assertEqual(len(t), 0)
		self.assertEqual(r.status_code, 200)

	def test_get_content_failed_2(self):
		"""
		passed wrong key in data/content_type
		"""
		r = self.app.post('/api/getcontent',
						  data=json.dumps({
								'fake_key': "/home/log.txt",
							})
			)

		t = json.loads(r.data)
		self.assertEqual(len(t), 0)
		self.assertEqual(r.status_code, 200)


	def test_getlogs(self):
		"""
		Test get_logs function written in APP.py
		"""
		r = app.get_logs()		
		self.assertEqual(collections.defaultdict, type(r))


if __name__ == '__main__':
    unittest.main()
