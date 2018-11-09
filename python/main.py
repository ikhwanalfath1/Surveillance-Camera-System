import cv2, atexit, logging, sys, time
from datetime import datetime
from flask import Flask, render_template, Response
from threading import Thread
from camera import VideoCamera

app = Flask(__name__)
cameraStart = VideoCamera().start()

@app.route('/')
def index():
	return render_template('index.html')

def readCamera(camera):
	while True:
		frame = cameraStart.readStreaming()
		time.sleep(1)
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/videoFeed')
def videoFeed():
	return Response(readCamera(VideoCamera()),
					mimetype='multipart/x-mixed-replace; boundary-frame')

if __name__ == '__main__':
	 logging.basicConfig(format='%(asctime)s %(message)s', filename='surveillance-camera-system.log', level=logging.INFO)
	 app.run(host='0.0.0.0', port=8081)