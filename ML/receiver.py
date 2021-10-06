import os
from flask import Flask, request
import json
from flask_cors import CORS
import base64
import matplotlib.pyplot as plt
import numpy as np
import onnxruntime as ort
from PIL import Image

app = Flask(__name__)
datasetPath = 'dataset'
playPath = 'play'
CORS(app)

classes = ['Bird', 'Flower', 'Hand', 'House', 'Mug', 'Pencil', 'Spoon', 'Sun', 'Tree', 'Umbrella']
ort_session = ort.InferenceSession('model.onnx')


@app.route('/api/dataset', methods=['POST'])
def canvasUpload():
	data = json.loads(request.data.decode('utf-8'))
	image_data = data['image'].split(',')[1].encode('utf-8')
	filename = data['filename']
	className = data['className']
	os.makedirs(f'{datasetPath}/{className}', exist_ok=True)
	with open(f'{datasetPath}/{className}/{filename}', 'wb') as fh:
		fh.write(base64.decodebytes(image_data))

	return {'res': 'Class Name is ' + className}


@app.route('/api/play', methods=['POST'])
def play():
	data = json.loads(request.data.decode('utf-8'))
	image = data['image'].split(',')[1].encode('utf-8')
	filename = data['filename']
	os.makedirs(f'{playPath}', exist_ok=True)
	with open(f'{playPath}/{filename}', 'wb') as fh:
		fh.write(base64.decodebytes(image))
	image = processImage(f'{playPath}/{filename}')
	output = ort_session.run(None, {'data': image})[0].argmax()
	# print(classes[output])
	return {'status': True, 'className': classes[output]}


def processImage(path):
	image = plt.imread(path)[:, :, 3]
	image = resizeImage(image)
	image = (np.array(image) > 0.1).astype(np.float32)[None, :, :]
	return image[None]


def resizeImage(image):
	image = (image * 255).astype(np.uint8)

	# Cropping Image
	y, x = np.where(image != 0)
	minX, maxX, minY, maxY = np.min(x), np.max(x), np.min(y), np.max(y)
	image = image[minY:maxY, minX:maxX]

	# Resizing and thresholding Image
	size = 64
	aspectRatio = image.shape[1] / image.shape[0]
	resizedImage = np.zeros([size, size], dtype=np.uint8)
	if aspectRatio >= 1:
		image = np.array(Image.fromarray(image).resize((size, max(10, int(size / aspectRatio)))))
	else:
		image = np.array(Image.fromarray(image).resize((max(10, int(size * aspectRatio)), size)))

	startRow = (size - image.shape[0]) // 2
	endRow = (startRow + image.shape[0])
	startCol = (size - image.shape[1]) // 2
	endCol = startCol + image.shape[1]
	resizedImage[startRow:endRow, startCol:endCol] = image
	resizedImage = np.array(resizedImage > 0, dtype=np.uint8) * 255
	# plt.imshow(resizedImage)
	# plt.show()
	# exit(0)
	# plt.imshow(resizedImage)
	# plt.show()
	return resizedImage
