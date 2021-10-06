import os

import torchvision
from torch.utils.data import Dataset
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


class customDatasetClass(Dataset):

	def __init__(self, path):

		self.path = path
		self.allImagePaths = []
		self.allTargets = []
		self.targetToClass = sorted(os.listdir(self.path))

		for targetNo, targetI in enumerate(self.targetToClass):
			for imageI in sorted(os.listdir(self.path + '/' + targetI)):
				self.allImagePaths.append(self.path + '/' + targetI + '/' + imageI)
				self.allTargets.append(targetNo)

		self.transforms = torchvision.transforms.Compose([
			torchvision.transforms.ToTensor()
		])

	def __getitem__(self, item):

		image = plt.imread(self.allImagePaths[item])[:, :, 3]
		# image = image.resize((64, 64))
		image = resizeImage(image)
		target = self.allTargets[item]

		image = self.transforms(image)
		return image, target

	def __len__(self):

		return len(self.allImagePaths)


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
		image = np.array(Image.fromarray(image).resize((size, max(10,int(size / aspectRatio)))))
	else:
		image = np.array(Image.fromarray(image).resize((max(10, int(size*aspectRatio)), size)))

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