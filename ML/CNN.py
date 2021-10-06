import torch
import torch.nn as nn
from torch.nn import functional as F


class Net(nn.Module):
	def __init__(self):
		super(Net, self).__init__()

		self.conv1 = nn.Conv2d(1, 16, 3, 1)
		self.conv2 = nn.Conv2d(16, 64, 3, 1)
		self.conv3 = nn.Conv2d(64, 128, 3, 1)
		self.conv4 = nn.Conv2d(128, 128, 3, 1)
		self.conv5 = nn.Conv2d(128, 128, 3, 1)
		self.conv6 = nn.Conv2d(128, 128, 3, 1)
		# self.dropout1 = nn.Dropout(0.25)
		# self.dropout2 = nn.Dropout(0.5)

		self.fc1 = nn.Linear(15488, 512)
		self.fc2 = nn.Linear(512, 128)
		self.fc3 = nn.Linear(128, 10)

	def forward(self, x):
		x = self.conv1(x)
		x = F.relu(x)
		x = self.conv2(x)
		x = F.relu(x)
		x = F.max_pool2d(x, 2)
		x = self.conv3(x)
		x = F.relu(x)
		x = self.conv4(x)
		x = F.relu(x)
		x = self.conv5(x)
		x = F.relu(x)
		x = self.conv6(x)
		x = F.relu(x)
		x = F.max_pool2d(x, 2)
		x = torch.flatten(x, 1)
		x = self.fc1(x)
		x = F.relu(x)
		x = self.fc2(x)
		x = F.relu(x)
		x = self.fc3(x)
		return x
