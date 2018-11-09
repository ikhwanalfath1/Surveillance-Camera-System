import numpy as np
import cv2, sys, urllib2, urllib, MySQLdb, time
from datetime import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tootls
from threading import Thread

class UploadGoogleDrive(object):
	def __init__(self):
		self.SCOPE = 'https://www.googleapis.com/auth/drive.file'
		self.store = file.Storage('storage.json')
		self.creds = self.store.get()

	def start(self):
		p4 = Thread(target = self.argumen, args=())
		p4.start()

		p5 = Thread(target = self.upload, args = ())
		p5.daemon=True
		p5.start()
		return self

	def argumen(self):
		try : 
			import argparse
			self.flags = argparse.ArgumenParser(parents=[tools.argparse].parse_args())
		except ImportError:
			self.flags = None

	def upload(self):
		if not self.creds or self.creds.invalid:
			print("Create new storage data")
			flow = client.flow_from_clientsecrets('client_secret.json', self.SCOPES)
			self.creds = tools.run_flow (Flow, store, self.flags)	\
							if self.flags else tools.run(flow, self.store)

		DRIVE = build('deive', 'v3', http=self.creds.autorize(Http()))
		tmp = 0