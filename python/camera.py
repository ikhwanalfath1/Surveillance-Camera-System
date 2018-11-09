import numpy as np
import cv2, sys, time
#import urllib2, urllib
from datetime import datetime
from threading import Thread

class VideoCamera(object):
	def __init__(self):
		global t0, t1, t2

		self.cam = cv2.VideoCapture(0)
		self.cam.set(3, 960)
		self.cam.set(4, 720)

		(self.grabbed, self.frame) = self.cam.read()
		self.stopped = False
		self.exeption = None

		self.fTime = datetime.now().strftime("%d-%m-%y %H:%M:%S")

	def __del__(self):
		self.cam.release()

	def start(self):
		p1 = Thread(target=self.update, args=())
		p1.daemon = True
		p1.start()

		p2 = Thread(target=self.motion, args=())
		p2.daemon = True
		p2.start()

		p3 = Thread(target=self.recorder, args=())
		p3.daemon = True
		p3.start()

		return self

	def update(self):
		time.sleep(2)
		while True:
			if self.stopped:
				return
				(self.grabbed, self.frame) = self.cam.read()
				self.q.append(self.frame)

	def readStreaming(self):
		ret, jpeg = cv2.imencode('.jpg', self.frame)
		return jpeg.tobytes()

	def diffImg(self, t0, t1, t2):
		d1 = cv2.absdiff(t2, t1)
		d2 = cv2.absdiff(t1, t0)
		return cv2.bitwise_and(d1, d2)

	def motion(self):
		# winName = "Movement Indicator"
		# cv2.namedWindow(winName)
		time.sleep(.1)

		threshold = 239000
		sTime = datetime.now().strftime('%Ss')
		tMinus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
		t = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
		tPlus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)

		while True:
			totalDiff = cv2.countNonZero(self.diffImg(tMinus, t, tPlus))
			text = "threshold: " + str(totalDiff)
			cv2.putText(self.frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
			print(text)

			if totalDiff > threshold and sTime != datetime.now().strftime('%Ss'):
				dimg = self.cam.read()[1]
				cv2.imwrite(('../storage/pictures/' + str(self.fTime) + '.jpg'), dimg)
				pictures = (str(self.fTime) + '.jpg')
				print(pictures)
				# cv2.imshow(winName, self.frame)
				# cv2.imshow(winName, self.diffImg(tMinus, t, tPlus))

			sTime = datetime.now().strftime('%Ss')
			tMinus = t
			t = tPlus
			tPlus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)

			key = cv2.waitKey(10)
			if key == ord('q'):
				cv2.destroyAllWindows()
				break

		return self

	def recorder(self):
		fourcc = cv2.VideoWriter_fourcc(*'DIVX')
		out = cv2.VideoWriter('../storage/recorder/' + str(self.fTime) + '.avi' , fourcc, 20.0, (int(self.cam.get(3)), int(self.cam.get(4))))
		video = (str(self.fTime) + '.avi')
		print(video)

		while(self.cam.isOpened()):
			ret, self.frame = self.cam.read()
			if ret == True:
				out.write(self.frame)
				key = cv2.waitKey(10)
				if key == ord('q'):
					break

		self.cam.release()
		out.release()
		cv2.destroyAllWindows()
		return self